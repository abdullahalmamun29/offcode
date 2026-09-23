"""
CHUP Phase 7 — Markdown Explanation Renderer.

Transforms ExplanationDocument into structured, human-readable Markdown with:
- GitHub-style alert blocks
- Structured tables for constraints and candidate eliminations
- Collapsible details sections for proof traces and derivations
- Exact epistemic status indicators
"""

from typing import List
from pointer_algorithms.proof_explanation.explanation_model import (
    ExplanationDocument,
    ExplanationLevel,
    EpistemicStatus
)


class MarkdownExplanationRenderer:
    """
    Renders ExplanationDocument into GitHub-flavored Markdown.
    """

    @classmethod
    def render(cls, doc: ExplanationDocument) -> str:
        lines: List[str] = []

        # Header & Status
        lines.append(f"# CHUP Proof & Verification Explanation")
        lines.append(f"**Problem ID:** `{doc.problem_id}` | **Level:** `{doc.level.value}` | **Outcome:** `{doc.outcome_state}`\n")

        # High-level Alert
        if "SATISFIABLE" in doc.outcome_state:
            lines.append("> [!TIP]")
            lines.append(f"> **Verified Solution Synthesized**: Outcome state `{doc.outcome_state}` established with all proof obligations discharged.\n")
        elif "UNSATISFIABLE" in doc.outcome_state:
            lines.append("> [!CAUTION]")
            lines.append(f"> **Contradictory / Unsatisfiable Constraints**: Input contains conflicting requirements ({doc.outcome_state}).\n")
        else:
            lines.append("> [!WARNING]")
            lines.append(f"> **Unresolved by Current Ontology**: Semantics could not be proven with the current verified ruleset.\n")

        # 1. Problem Understanding
        if doc.understanding_section.claims:
            lines.append("## 1. Problem Understanding")
            lines.append("| Dimension | Key | Value | Epistemic Status |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for c in doc.understanding_section.claims:
                status_icon = "✓ PROVEN" if c.epistemic_status == EpistemicStatus.PROVEN else f"? {c.epistemic_status.value}"
                lines.append(f"| {c.dimension} | `{c.key}` | `{c.canonical_value}` | {status_icon} |")
            lines.append("")

        # 2. Proven Mathematical Facts
        if doc.proven_facts_section.claims:
            lines.append("## 2. Proven Mathematical Facts")
            for c in doc.proven_facts_section.claims:
                icon = "✓" if c.epistemic_status == EpistemicStatus.PROVEN else "?"
                lines.append(f"- **{icon} `{c.fact_name}`** (`{c.tier}`): {c.epistemic_status.value}")
                if c.witness:
                    lines.append(f"  *Witness: {c.witness}*")
            lines.append("")

        # 3. Axiomatic Derivations & Invariants
        if doc.derivation_section.claims:
            lines.append("## 3. Axiomatic Derivations & Invariants")
            for c in doc.derivation_section.claims:
                sources = ", ".join(f"`{s}`" for s in c.source_fact_ids)
                lines.append(f"### Rule: `{c.rule_name}` $\\to$ `{c.derived_fact}`")
                lines.append(f"- **Sources:** {sources}")
                if c.witness:
                    lines.append(f"- **Witness:** {c.witness}")
            lines.append("")

        # 4. Enriched Constraints
        if doc.constraint_section.claims:
            lines.append("## 4. Enriched Constraints (Phase 5 Boundary)")
            for c in doc.constraint_section.claims:
                lines.append(f"- `{c.constraint_name}`: `{c.polarity}` in lattice `{c.lattice_dimension}`")
            lines.append("")

        # 5. Candidate Elimination Analysis
        if doc.elimination_section.claims:
            lines.append("## 5. Closed-World Candidate Elimination")
            lines.append("| Candidate | Status | Rejection Reason | Violated Constraint | Certificate |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for c in doc.elimination_section.claims:
                lines.append(f"| `{c.candidate_id}` | ELIMINATED | {c.rejection_code} | `{c.violated_constraint}` | `{c.certificate_id}` |")
            lines.append("")

        # 6. Selected Components & Composition
        if doc.selection_section.claims or doc.composition_section.claims:
            lines.append("## 6. Synthesized Composition & Capability Contracts")
            for c in doc.selection_section.claims:
                lines.append(f"- **Selected Component:** `{c.component_id}` (Role: `{c.role}`)")
            for c in doc.composition_section.claims:
                lines.append(f"- **Pipeline Step {c.step_index}:** `{c.producer_id}` $\\to$ `{c.capability_name}` (`{c.contract_status}`)")
            lines.append("")

        # 7. Resource & Complexity Verification
        if doc.resource_section.claims:
            lines.append("## 7. Resource & Complexity Verification")
            for c in doc.resource_section.claims:
                lines.append(f"- **{c.metric}:** `{c.bound_value}` — `{c.verdict}`")
            lines.append("")

        # 8. Correctness & Proof Obligations
        if doc.correctness_section.claims:
            lines.append("## 8. Correctness & Proof Obligations")
            for c in doc.correctness_section.claims:
                if hasattr(c, "obligation_id"):
                    lines.append(f"- **Obligation `{c.obligation_id}`:** {c.description} [{c.discharge_status}]")
                elif hasattr(c, "invariant_name"):
                    lines.append(f"- **Invariant `{c.invariant_name}`:** {c.argument}")
            lines.append("")

        # 9. Verification Summary
        if doc.summary_section.claims:
            lines.append("## 9. Verification Summary")
            for c in doc.summary_section.claims:
                lines.append(f"- **Outcome State:** `{c.outcome_state}`")
                lines.append(f"- **Plan ID:** `{c.plan_id}`")
                lines.append(f"- **Verification Artifact ID:** `{c.verification_artifact_id}`")
                if c.integrity_seal:
                    lines.append(f"- **SHA-256 Integrity Seal:** `{c.integrity_seal}`")
            lines.append("")

        return "\n".join(lines)
