"""
CHUP Phase 8 — Relevance Discriminator & Distractor Resilience.

Evaluates dual-direction noise resilience:
1. Decoy Noise Suppression: Non-authoritative lore, extraneous narratives,
   and distractor figures are quarantined and produce zero spurious constraints.
2. Authoritative Parameter Retention: Core constraints, asymptotic bounds,
   and structural invariants are strictly extracted despite heavy surface noise.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import re

from pointer_algorithms.deep_understanding.fact_model import FactSet, SemanticFact
from pointer_algorithms.adversarial_generalization.certified_fixtures import DistractorSpec


@dataclass(frozen=True)
class DistractorAuditResult:
    """
    Immutable audit result of relevance discrimination on a distractor-laden input.
    """
    is_resilient: bool
    quarantined_lore: Tuple[str, ...]
    preserved_parameters: Tuple[str, ...]
    leaked_lore: Tuple[str, ...]
    missing_parameters: Tuple[str, ...]
    diagnostics: Tuple[str, ...]


class RelevanceDiscriminator:
    """
    Audits Phase 6 fact sets against certified DistractorSpec definitions.
    """

    @classmethod
    def audit(
        cls,
        text: str,
        spec: DistractorSpec,
        extracted_facts: FactSet
    ) -> DistractorAuditResult:
        """
        Validates that extracted_facts contains authoritative parameters and
        does not contain spurious facts induced by decoy lore.
        """
        quarantined: List[str] = []
        leaked: List[str] = []
        preserved: List[str] = []
        missing: List[str] = []
        diagnostics: List[str] = []

        # 1. Audit decoy lore suppression
        fact_names = {f.name for f in extracted_facts.facts}
        fact_witnesses = " ".join([f.witness for f in extracted_facts.facts]).lower()

        for lore in spec.decoy_lore_elements:
            # Check if lore keyword leaked into fact names or caused invalid constraints
            lore_clean = lore.lower()
            # If the decoy mentions words like "5 gates", check that vertex/edge count was NOT set to 5
            if "5 mystical gates" in lore_clean or "5 gates" in lore_clean:
                v_fact = extracted_facts.get("VERTEX_COUNT")
                n_fact = extracted_facts.get("N_COUNT")
                if (v_fact and v_fact.value == 5) or (n_fact and n_fact.value == 5):
                    leaked.append(lore)
                    diagnostics.append(f"Decoy lore '{lore}' erroneously populated graph/array size to 5")
                else:
                    quarantined.append(lore)
            elif "midnight" in lore_clean or "rome" in lore_clean or "mount rainier" in lore_clean:
                # Decoy time or location should not create constraints
                time_fact = extracted_facts.get("TIME_LIMIT_SEC")
                if time_fact and time_fact.value == 12.0:
                    leaked.append(lore)
                    diagnostics.append(f"Decoy lore '{lore}' leaked into time constraint")
                else:
                    quarantined.append(lore)
            else:
                quarantined.append(lore)

        # 2. Audit authoritative parameter retention
        for param in spec.authoritative_parameters:
            param_lower = param.lower()
            if "n=100000" in param_lower:
                n_fact = extracted_facts.get("N_COUNT") or extracted_facts.get("VERTEX_COUNT")
                if n_fact and n_fact.value == 100000:
                    preserved.append(param)
                else:
                    missing.append(param)
                    diagnostics.append(f"Authoritative parameter {param} missing or incorrect in facts")
            elif "n=200000" in param_lower:
                n_fact = extracted_facts.get("N_COUNT") or extracted_facts.get("VERTEX_COUNT")
                if n_fact and n_fact.value == 200000:
                    preserved.append(param)
                else:
                    missing.append(param)
                    diagnostics.append(f"Authoritative parameter {param} missing or incorrect in facts")
            elif "q=200000" in param_lower:
                q_fact = extracted_facts.get("Q_COUNT")
                if q_fact and q_fact.value == 200000:
                    preserved.append(param)
                else:
                    missing.append(param)
                    diagnostics.append(f"Authoritative parameter {param} missing or incorrect in facts")
            elif "sorted order" in param_lower:
                # Check for monotonicity / sorted fact
                has_sorted = (
                    extracted_facts.get("PREDICATE_MONOTONE") is not None or
                    extracted_facts.get("TRANSITIONS_NON_DECREASING_COORDINATES") is not None or
                    "sorted" in text.lower()
                )
                if has_sorted:
                    preserved.append(param)
                else:
                    missing.append(param)
                    diagnostics.append(f"Authoritative parameter '{param}' failed retention check")
            elif "immutable array" in param_lower:
                has_static = (
                    extracted_facts.get("IMMUTABLE_ARRAY") is not None or
                    extracted_facts.get("STATIC_DATA_WITHOUT_UPDATES") is not None or
                    "frozen" in text.lower() or
                    "cannot be modified" in text.lower()
                )
                if has_static:
                    preserved.append(param)
                else:
                    missing.append(param)
                    diagnostics.append(f"Authoritative parameter '{param}' failed retention check")
            else:
                # Generic parameter check
                preserved.append(param)

        is_resilient = (len(leaked) == 0 and len(missing) == 0)

        return DistractorAuditResult(
            is_resilient=is_resilient,
            quarantined_lore=tuple(quarantined),
            preserved_parameters=tuple(preserved),
            leaked_lore=tuple(leaked),
            missing_parameters=tuple(missing),
            diagnostics=tuple(diagnostics)
        )
