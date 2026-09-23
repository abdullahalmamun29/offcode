"""
Auditable Diagnostic Trace Generator for Architecture V2.

Produces structured, human- and machine-readable reasoning traces matching Section 45/49.
Answers:
- Why was a candidate considered?
- Why were alternatives rejected?
- What requirements were satisfied?
- Which constraints were violated?
- What proof obligations remain?
- What implementation strategy was selected?
"""

from typing import List, Dict, Any, Optional
from architecture_v2.semantic_model import ProblemModel
from architecture_v2.planner import AlgorithmPlan, PlanStatus
from architecture_v2.candidate_eliminator import CandidateDecision


class DiagnosticTracer:
    """
    Formats the complete reasoning lifecycle into an auditable diagnostic report.
    """

    @classmethod
    def generate_trace(
        cls,
        model: ProblemModel,
        plan: AlgorithmPlan,
        decisions: Optional[List[CandidateDecision]] = None
    ) -> str:
        lines: List[str] = []

        # ── 1. Problem Understanding ──
        lines.append("PROBLEM UNDERSTANDING")
        lines.append("---------------------")
        lines.append(f"entities: {', '.join(model.entities) if model.entities else 'sequence / array'}")
        lines.append(f"objective: {model.objective.kind.value} (target: {model.objective.target_property or 'none'})")
        lines.append(f"selection: {model.selection}")
        lines.append(f"output: {model.output_spec.get('type', 'DEFAULT')}")
        lines.append("")

        # ── 2. Constraint Model ──
        lines.append("CONSTRAINT MODEL")
        lines.append("----------------")
        lines.append(f"n: {model.constraints.n or 'unknown'}")
        lines.append(f"target_value: {model.constraints.target_value or 'none'}")
        lines.append(f"time_limit: {model.constraints.time_limit_ms} ms")
        lines.append(f"memory_limit: {model.constraints.memory_limit_mb} MB")
        lines.append("")

        # ── 3. Semantic Evidence ──
        lines.append("SEMANTIC EVIDENCE")
        lines.append("-----------------")
        if model.evidence:
            for ev in model.evidence:
                lines.append(f"- [{ev.status.value}] {ev.fact} (source: \"{ev.source}\", conf: {ev.confidence:.2f})")
        else:
            lines.append("None")
        lines.append("")

        # ── 4. Derived Facts & Trace ──
        lines.append("DERIVED FACTS & TRACE")
        lines.append("---------------------")
        if model.facts:
            for name, fact in model.facts.items():
                if fact.derivation_rule:
                    deps = ", ".join(fact.dependencies)
                    lines.append(f"- {name} = {fact.value} [Rule: {fact.derivation_rule}, Dependencies: ({deps})]")
                else:
                    lines.append(f"- {name} = {fact.value} [Explicit]")
        else:
            lines.append("None")
        lines.append("")

        # ── 5. Required Operations ──
        lines.append("REQUIRED OPERATIONS")
        lines.append("-------------------")
        if model.operations:
            for op in sorted(model.operations, key=lambda x: x.value):
                lines.append(f"- {op.value}")
        else:
            lines.append("None")
        lines.append("")

        # ── 6. Structural Properties ──
        lines.append("STRUCTURAL PROPERTIES")
        lines.append("---------------------")
        if model.structural_properties:
            for prop in sorted(model.structural_properties, key=lambda x: x.value):
                lines.append(f"- {prop.value}")
        else:
            lines.append("None")
        lines.append("")

        # ── 7. Candidates & Decisions ──
        lines.append("CANDIDATES")
        lines.append("----------")
        if plan.diagnostic_trace:
            for item in plan.diagnostic_trace:
                lines.append(f"candidate: {item.get('candidate')}")
                lines.append(f"    status: {item.get('status')}")
                reasons = item.get('reasons', [])
                if reasons:
                    lines.append(f"    reasons: {', '.join(reasons)}")
                violated = item.get('violated', [])
                if violated:
                    lines.append(f"    violated: {', '.join(violated)}")
                lines.append("")
        else:
            lines.append("No candidates evaluated.")
            lines.append("")

        # ── 8. Composition ──
        lines.append("COMPOSITION")
        lines.append("-----------")
        if plan.composed_capabilities:
            lines.append(f"status: {plan.status.value}")
            lines.append(f"composed capabilities: {', '.join(plan.composed_capabilities)}")
        else:
            lines.append("Single capability strategy (no cross-family composition required).")
        lines.append("")

        # ── 9. Proof Obligations ──
        lines.append("PROOF OBLIGATIONS")
        lines.append("-----------------")
        if plan.established_obligations:
            lines.append("Established obligations:")
            for obl in plan.established_obligations:
                lines.append(f"  ✓ {obl}: PROVEN")
        if plan.unresolved_obligations:
            lines.append("Unresolved obligations:")
            for obl in plan.unresolved_obligations:
                lines.append(f"  ✗ {obl}: UNPROVEN")
        if not plan.established_obligations and not plan.unresolved_obligations:
            lines.append("None")
        lines.append("")

        # ── 10. Implementation Plan ──
        lines.append("IMPLEMENTATION PLAN")
        lines.append("-------------------")
        lines.append(f"strategy: {plan.strategy_name or 'None'}")
        lines.append(f"backend: {plan.implementation_backend or 'None'}")
        if plan.invariant:
            lines.append(f"invariant: {plan.invariant}")
        lines.append("")

        # ── 11. Final Decision ──
        lines.append("FINAL DECISION")
        lines.append("--------------")
        lines.append(f"status: {plan.status.value}")
        if plan.rejection_reasons:
            lines.append(f"diagnostic: {'; '.join(plan.rejection_reasons)}")
        lines.append("")

        return "\n".join(lines)
