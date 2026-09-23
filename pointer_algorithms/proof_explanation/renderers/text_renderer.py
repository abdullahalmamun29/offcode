"""
CHUP Phase 7 — Plain Text Explanation Renderer.

Serializes an ExplanationDocument to clean, formatted terminal text.
"""

from typing import List
from pointer_algorithms.proof_explanation.explanation_model import (
    ExplanationDocument,
    EpistemicStatus
)


class TextExplanationRenderer:
    """
    Renders ExplanationDocument into plain terminal text.
    """

    @classmethod
    def render(cls, doc: ExplanationDocument) -> str:
        lines: List[str] = []
        lines.append("=" * 70)
        lines.append(f"CHUP PROOF & EXPLANATION [{doc.level.value}]")
        lines.append(f"Problem: {doc.problem_id} | Outcome: {doc.outcome_state}")
        lines.append("=" * 70)

        # 1. Understanding
        if doc.understanding_section.claims:
            lines.append("\n[1. Problem Understanding]")
            for c in doc.understanding_section.claims:
                lines.append(f"  * {c.key} ({c.dimension}): {c.canonical_value} [{c.epistemic_status.value}]")

        # 2. Proven Facts
        if doc.proven_facts_section.claims:
            lines.append("\n[2. Proven Facts]")
            for c in doc.proven_facts_section.claims:
                lines.append(f"  * {c.fact_name} [{c.epistemic_status.value}]: {c.witness}")

        # 3. Derivations
        if doc.derivation_section.claims:
            lines.append("\n[3. Axiomatic Derivations]")
            for c in doc.derivation_section.claims:
                lines.append(f"  * {c.rule_name} -> {c.derived_fact} (Sources: {', '.join(c.source_fact_ids)})")

        # 4. Elimination
        if doc.elimination_section.claims:
            lines.append("\n[4. Candidate Elimination]")
            for c in doc.elimination_section.claims:
                lines.append(f"  * REJECTED: {c.candidate_id} (Reason: {c.rejection_code})")

        # 5. Selection & Composition
        if doc.selection_section.claims:
            lines.append("\n[5. Selection & Pipeline]")
            for c in doc.selection_section.claims:
                lines.append(f"  * Selected: {c.component_id} ({c.role})")
            for c in doc.composition_section.claims:
                lines.append(f"  * Step {c.step_index}: {c.producer_id} -> {c.capability_name}")

        # 6. Resources
        if doc.resource_section.claims:
            lines.append("\n[6. Resource Verification]")
            for c in doc.resource_section.claims:
                lines.append(f"  * {c.metric}: {c.bound_value} [{c.verdict}]")

        # 7. Verification Summary
        if doc.summary_section.claims:
            lines.append("\n[7. Verification Verdict]")
            for c in doc.summary_section.claims:
                lines.append(f"  * Outcome: {c.outcome_state}")
                lines.append(f"  * Plan ID: {c.plan_id}")
                if c.integrity_seal:
                    lines.append(f"  * SHA-256 Seal: {c.integrity_seal}")

        lines.append("=" * 70)
        return "\n".join(lines)
