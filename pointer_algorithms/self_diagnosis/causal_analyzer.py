"""
Phase 9 — causal_analyzer.py

Causal failure attribution and controlled reproducibility analysis.
Proves that a failure is genuinely attributable to the generated implementation,
rather than environment, timing, or external anomalies.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Tuple

from .diagnostic_types import (
    BoundaryGuardEvidence,
    ImplementationBugKind,
    IndexMappingEvidence,
    MissingHeaderEvidence,
    OverflowEvidence,
    RepairStrategy,
    ReproducibilityStatus,
    StructuredEvidence,
)
from .failure_evidence import FailureEvidence


@dataclass(frozen=True)
class ControlledReproductionReport:
    status: ReproducibilityStatus
    reproduction_runs: int
    identical_signatures: bool
    controlled_envelope_hash: str
    failure_signatures: Tuple[str, ...]
    details: str = ""

    def is_controlled_reproducible(self) -> bool:
        return (
            self.status == ReproducibilityStatus.CONTROLLED_REPRODUCIBLE
            and self.reproduction_runs >= 3
            and self.identical_signatures
        )


class CausalAnalyzer:
    """
    Performs causal attribution of failure to implementation.
    Requires:
    1. Controlled empirical reproducibility across >=3 runs under identical envelope.
    2. Explicit structured proof linking defect to code behavior.
    """

    @classmethod
    def evaluate_controlled_reproducibility(
        cls,
        evidence_runs: Sequence[FailureEvidence],
        controlled_envelope_info: Mapping[str, Any],
    ) -> ControlledReproductionReport:
        if len(evidence_runs) < 3:
            return ControlledReproductionReport(
                status=ReproducibilityStatus.UNVERIFIED,
                reproduction_runs=len(evidence_runs),
                identical_signatures=False,
                controlled_envelope_hash="",
                failure_signatures=(),
                details=f"Insufficient runs: {len(evidence_runs)} < 3 required.",
            )

        envelope_canonical = json.dumps(controlled_envelope_info, sort_keys=True)
        envelope_hash = hashlib.sha256(envelope_canonical.encode()).hexdigest()

        signatures = tuple(ev.fingerprint() for ev in evidence_runs)
        first_sig = signatures[0]
        identical = all(sig == first_sig for sig in signatures)

        if not identical:
            return ControlledReproductionReport(
                status=ReproducibilityStatus.NOT_REPRODUCIBLE,
                reproduction_runs=len(evidence_runs),
                identical_signatures=False,
                controlled_envelope_hash=envelope_hash,
                failure_signatures=signatures,
                details="Failure signatures differed across runs under identical envelope.",
            )

        return ControlledReproductionReport(
            status=ReproducibilityStatus.CONTROLLED_REPRODUCIBLE,
            reproduction_runs=len(evidence_runs),
            identical_signatures=True,
            controlled_envelope_hash=envelope_hash,
            failure_signatures=signatures,
            details="Controlled reproducibility confirmed across all runs.",
        )

    @classmethod
    def match_certified_defect(
        cls,
        evidence: FailureEvidence,
        ast_context: Mapping[str, Any],
        phase5_plan: Mapping[str, Any],
        phase6_facts: Sequence[Mapping[str, Any]],
    ) -> Tuple[Optional[ImplementationBugKind], Optional[RepairStrategy], Optional[StructuredEvidence], str]:
        """
        Analyzes evidence and problem context to determine if the failure matches
        a pre-certified repairable defect class.
        Returns: (bug_kind, strategy, structured_evidence, reasoning)
        """
        # 1. Missing Header check (compiler error matching AST identifiers)
        if evidence.is_compiler_failure():
            compiler_text = "\n".join(evidence.compiler_diagnostic_lines) + "\n" + evidence.stderr_excerpt
            from .stl_header_registry import STL_HEADER_REGISTRY
            for ident, header in STL_HEADER_REGISTRY.items():
                short_ident = ident.split("::")[-1]
                if (short_ident in compiler_text or ident in compiler_text) and (
                    "was not declared in this scope" in compiler_text
                    or "is not a member of 'std'" in compiler_text
                    or "unknown type name" in compiler_text
                ):
                    # Check if identifier is actually present in AST context
                    identifiers_in_source = ast_context.get("identifiers", [])
                    includes_in_source = ast_context.get("includes", [])
                    if short_ident in identifiers_in_source or ident in identifiers_in_source:
                        if header not in includes_in_source:
                            ev = MissingHeaderEvidence(
                                missing_header=header,
                                required_by_identifier=ident,
                                compiler_diagnostic_excerpt=compiler_text[:400],
                                stl_registry_entry_verified=True,
                                ast_identifier_confirmed=True,
                            )
                            return (
                                ImplementationBugKind.MISSING_HEADER,
                                RepairStrategy.ADD_MISSING_HEADER,
                                ev,
                                f"Identifier '{ident}' requires header '{header}' which is missing from source.",
                            )

        # 2. Integer Overflow / Type Width Mismatch
        # Requires proven range calculation from Phase 5/6 facts
        constraints = phase5_plan.get("constraints", {})
        proven_overflow = False
        n_bound = constraints.get("N_max", 0)
        v_bound = constraints.get("value_max", 0)
        # Check if phase6 has derived an intermediate magnitude fact
        for fact in phase6_facts:
            if fact.get("fact_type") == "INTERMEDIATE_ACCUMULATOR_MAGNITUDE":
                mag = fact.get("max_magnitude", 0)
                if mag > 2_147_483_647:
                    target_var = fact.get("target_variable", "sum")
                    scope = fact.get("target_scope", "solve")
                    ev = OverflowEvidence(
                        constraint_n_bound=n_bound,
                        constraint_value_bound=v_bound,
                        max_intermediate_magnitude=mag,
                        original_type="int",
                        required_type="long long",
                        original_identifier=target_var,
                        target_scope=scope,
                    )
                    if ev.validate():
                        return (
                            ImplementationBugKind.TYPE_WIDTH_MISMATCH,
                            RepairStrategy.WIDEN_TO_64BIT,
                            ev,
                            f"Accumulator '{target_var}' requires 64-bit width: magnitude {mag} exceeds INT_MAX.",
                        )
                    else:
                        # Required magnitude exceeds LLONG_MAX -> fail closed!
                        return (
                            ImplementationBugKind.UNCLASSIFIED_CODE_DEFECT,
                            RepairStrategy.NONE,
                            None,
                            f"Required intermediate magnitude {mag} exceeds LLONG_MAX; widening to 64-bit is insufficient.",
                        )

        # 3. Certified Index Base Translation (1-based input to 0-based internal)
        # Requires explicit IndexMappingEvidence from AST & plan
        for fact in phase6_facts:
            if fact.get("fact_type") == "INDEXING_BASE_DISCREPANCY":
                ev = IndexMappingEvidence(
                    external_base=fact.get("external_base", 1),
                    external_lower_bound=fact.get("external_lower_bound", 1),
                    external_upper_bound_var=fact.get("external_upper_bound_var", "N"),
                    internal_base=fact.get("internal_base", 0),
                    internal_lower_bound=fact.get("internal_lower_bound", 0),
                    internal_upper_bound_expr=fact.get("internal_upper_bound_expr", "N - 1"),
                    offending_expression=fact.get("offending_expression", ""),
                    translated_expression=fact.get("translated_expression", ""),
                    target_scope=fact.get("target_scope", ""),
                )
                if ev.validate():
                    return (
                        ImplementationBugKind.CERTIFIED_INDEX_BASE_TRANSLATION,
                        RepairStrategy.ADJUST_INDEX_BASE,
                        ev,
                        f"Certified index base translation from 1-based to 0-based for {ev.offending_expression}.",
                    )

        # 4. Certified Boundary Guard (Empty or zero-size boundary with proven algebraic identity)
        for fact in phase6_facts:
            if fact.get("fact_type") == "BOUNDARY_ALGEBRAIC_IDENTITY":
                cond = fact.get("boundary_condition", "")
                ident_val = fact.get("identity_expression", "")
                proof_ref = fact.get("proof_reference", "")
                ev = BoundaryGuardEvidence(
                    boundary_condition=cond,
                    identity_expression=ident_val,
                    proof_reference=proof_ref,
                    authoritative_source_layer=fact.get("source_layer", "PHASE6_DERIVED_FACT"),
                )
                if ev.validate():
                    return (
                        ImplementationBugKind.CERTIFIED_BOUNDARY_GUARD,
                        RepairStrategy.INSERT_BOUNDARY_GUARD,
                        ev,
                        f"Certified boundary guard for '{cond}' with proven identity '{ident_val}'.",
                    )

        # Unclassified defect
        return (
            ImplementationBugKind.UNCLASSIFIED_CODE_DEFECT,
            RepairStrategy.NONE,
            None,
            "Failure does not match any certified deterministic repair pattern.",
        )
