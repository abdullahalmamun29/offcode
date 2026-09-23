"""
Bridge V2: Entry point for Architecture V2 reasoning, planning, and code generation.

Provides both programmatic Python API and JSON-IPC interface compatible with TypeScript pipeline.
Enforces the fail-closed policy: unsupported compositions or unproven candidates produce
auditable diagnostics and never emit unrelated code.
"""

from typing import Dict, Any, Optional
from architecture_v2.semantic_adapter import SemanticAdapter
from architecture_v2.capability_registry import CapabilityRegistry
from architecture_v2.planner import AlgorithmPlannerV2, PlanStatus, AlgorithmPlan
from architecture_v2.diagnostics import DiagnosticTracer


class BridgeV2:
    """
    Main orchestrator for Architecture V2 problem understanding, reasoning, and planning.
    """
    def __init__(self, registry: Optional[CapabilityRegistry] = None):
        self.registry = registry or CapabilityRegistry()

    def solve(self, problem_text: str, constraints_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # 1. Semantic parsing & derivation
        model = SemanticAdapter.parse(problem_text, constraints_override)

        # 2. Algorithm planning & candidate reasoning
        plan = AlgorithmPlannerV2.create_plan(model, self.registry)

        # 3. Diagnostic trace generation
        trace = DiagnosticTracer.generate_trace(model, plan)

        # 4. Result construction
        if plan.status == PlanStatus.PROVEN and plan.code:
            return {
                "status": "success",
                "domain": "architecture_v2",
                "selectedPattern": plan.strategy_name,
                "capability": plan.primary_capability,
                "code": plan.code,
                "invariant": plan.invariant,
                "proofObligations": plan.established_obligations,
                "reasoning": trace,
                "diagnosticTrace": plan.diagnostic_trace,
                "limitationMessage": None
            }
        elif plan.status == PlanStatus.COMPOSITION_UNSUPPORTED:
            return {
                "status": "unsupported",
                "domain": "architecture_v2",
                "selectedPattern": None,
                "capability": None,
                "code": None,
                "invariant": None,
                "proofObligations": [],
                "reasoning": trace,
                "diagnosticTrace": plan.diagnostic_trace,
                "limitationMessage": plan.rejection_reasons[0] if plan.rejection_reasons else "COMPOSITION_UNSUPPORTED"
            }
        elif plan.status == PlanStatus.UNPROVEN:
            return {
                "status": "unsupported",
                "domain": "architecture_v2",
                "selectedPattern": None,
                "capability": plan.primary_capability,
                "code": None,
                "invariant": None,
                "proofObligations": [],
                "reasoning": trace,
                "diagnosticTrace": plan.diagnostic_trace,
                "limitationMessage": plan.rejection_reasons[0] if plan.rejection_reasons else "CANDIDATE_UNPROVEN"
            }
        else:
            return {
                "status": "unsupported",
                "domain": "architecture_v2",
                "selectedPattern": None,
                "capability": None,
                "code": None,
                "invariant": None,
                "proofObligations": [],
                "reasoning": trace,
                "diagnosticTrace": plan.diagnostic_trace,
                "limitationMessage": plan.rejection_reasons[0] if plan.rejection_reasons else "UNSUPPORTED"
            }

    def explain(self, problem_text: str, constraints_override: Optional[Dict[str, Any]] = None) -> str:
        res = self.solve(problem_text, constraints_override)
        return res["reasoning"]

    def why_not(self, problem_text: str, candidate_name: str, constraints_override: Optional[Dict[str, Any]] = None) -> str:
        """
        Explains why a specific candidate algorithm was rejected or unproven for the given problem.
        """
        model = SemanticAdapter.parse(problem_text, constraints_override)
        capability = self.registry.get(candidate_name)
        if not capability:
            return f"Candidate '{candidate_name}' is not registered in the CapabilityRegistry."

        from architecture_v2.candidate_eliminator import CandidateEliminatorV2, CandidateStatus
        from architecture_v2.semantic_model import RelationKind
        decision = CandidateEliminatorV2.evaluate(capability, model)

        lines = [
            f"Candidate: {candidate_name}",
            f"Status: {decision.status.value}",
            ""
        ]

        if decision.status == CandidateStatus.REJECTED:
            lines.append("Rejection Reasons:")
            for r in decision.reasons:
                lines.append(f"  - {r}")
            lines.append("")
            if decision.violated_constraints:
                lines.append("Violated Constraints:")
                for v in decision.violated_constraints:
                    lines.append(f"  - {v}")
                lines.append("")
            if decision.missing_requirements:
                lines.append("Missing Requirements:")
                for m in decision.missing_requirements:
                    lines.append(f"  - {m}")
                lines.append("")
            if candidate_name in ("two_pointer_pair_sum", "hash_pair_sum") and model.selection.cardinality is not None and model.selection.cardinality > 2 and any(r.kind == RelationKind.SUM for r in model.relations):
                lines.append("Composition Note:")
                lines.append("  - This capability cannot solve the complete problem because the problem requires cardinality "
                             f"{model.selection.cardinality} while the capability solves cardinality 2.")
                lines.append("  - However, the same pair-sum capability can serve as a residual component after one anchor is selected.")
                lines.append("")
        elif decision.status == CandidateStatus.UNPROVEN:
            lines.append("Unresolved Proof Obligations:")
            for obl, st in decision.proof_status.items():
                if st != "PROVEN":
                    lines.append(f"  - {obl}: {st}")
            lines.append("")
        elif decision.status == CandidateStatus.ACCEPTED:
            lines.append("Candidate satisfies all preconditions and proof obligations:")
            for s in decision.satisfied_requirements:
                lines.append(f"  - {s}")
            lines.append("")

        return "\n".join(lines).strip()


def handle_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    JSON-IPC handler for Bridge V2.
    """
    problem_text = req.get("problemText") or req.get("problem") or ""
    constraints_override = req.get("constraints") or {}
    bridge = BridgeV2()
    action = req.get("action")
    if action == "why_not":
        candidate = req.get("candidate") or ""
        return {"explanation": bridge.why_not(problem_text, candidate, constraints_override)}
    return bridge.solve(problem_text, constraints_override)
