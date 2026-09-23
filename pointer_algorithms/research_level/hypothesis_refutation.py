"""
Phase 10 — hypothesis_refutation.py

Pillar II: Inductive Hypothesis Refutation Engine.
Constrains hypothesis formulation to registered schemas.
Executes finite-envelope exhaustive falsification search against reference oracles.
Strictly inherits Phase 9 OracleIntegrityGate and HarnessIntegrityGate.
Enforces Law 2 (counterexample => REFUTED), Law 3 (exhaustion => SUPPORTED),
and Law 4 (no search-to-proof laundering).
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Callable, Iterator, Mapping, Optional, Sequence, Tuple

from pointer_algorithms.self_diagnosis.diagnostic_types import HarnessStatus, OracleStatus
from pointer_algorithms.self_diagnosis.harness_integrity import HarnessIntegrityGate
from pointer_algorithms.self_diagnosis.oracle_integrity import OracleExecutionEvidence, OracleIntegrityGate

from .research_types import (
    CorroborationCertificate,
    EpistemicStatus,
    FiniteSearchEnvelope,
    HypothesisSchema,
    RefutationCertificate,
)


class InductiveRefutationEngine:
    """
    Automates controlled falsification of algorithmic hypotheses.
    """

    @classmethod
    def evaluate_hypothesis(
        cls,
        hypothesis_id: str,
        schema: HypothesisSchema,
        envelope: FiniteSearchEnvelope,
        instance_generator: Callable[[FiniteSearchEnvelope], Iterator[Any]],
        hypothesis_solver: Callable[[Any], Any],
        reference_oracle: Callable[[Any], Any],
        oracle_runs: Sequence[OracleExecutionEvidence],
        metamorphic_check_passed: Optional[bool] = None,
        secondary_oracle_agreement: Optional[bool] = None,
    ) -> Tuple[Optional[RefutationCertificate], Optional[CorroborationCertificate], EpistemicStatus, str]:
        """
        Evaluates an algorithmic hypothesis within the specified FiniteSearchEnvelope.

        Returns: (refutation_cert, corroboration_cert, status, reason)
        """
        # 1. Inherit Phase 9 Oracle Integrity Gate
        oracle_res = OracleIntegrityGate.evaluate(
            oracle_runs=oracle_runs,
            metamorphic_check_passed=metamorphic_check_passed,
            secondary_oracle_agreement=secondary_oracle_agreement,
        )

        if not oracle_res.is_healthy():
            # Anti-guessing: Defective or inconsistent oracle cannot refute or corroborate!
            return (
                None,
                None,
                EpistemicStatus.UNRESOLVED,
                f"Oracle integrity check failed ({oracle_res.status.value}): {oracle_res.reason}",
            )

        # 2. Exhaustive Exploration within FiniteSearchEnvelope
        states_evaluated = 0
        start_time = time.monotonic()
        timeout_sec = envelope.timeout_ms_budget / 1000.0

        for instance in instance_generator(envelope):
            states_evaluated += 1

            # Time and state budget checks
            if time.monotonic() - start_time > timeout_sec or states_evaluated > envelope.max_states_budget:
                return (
                    None,
                    None,
                    EpistemicStatus.UNRESOLVED,
                    f"Search envelope budget exhausted after {states_evaluated} states ({envelope.max_states_budget} limit).",
                )

            # Evaluate hypothesis against oracle
            try:
                hyp_out = hypothesis_solver(instance)
            except Exception as ex:
                # Runtime crash in hypothesis solver is a definitive witness
                cert_id = f"ref_{uuid.uuid4().hex[:10]}"
                ref_cert = RefutationCertificate(
                    certificate_id=cert_id,
                    hypothesis_id=hypothesis_id,
                    schema=schema,
                    counterexample_witness={"instance": str(instance), "exception": str(ex)},
                    hypothesis_output=f"CRASH: {str(ex)}",
                    oracle_output="VALID_EXECUTION",
                    envelope_fingerprint=envelope.fingerprint(),
                    status=EpistemicStatus.REFUTED,
                )
                return (ref_cert, None, EpistemicStatus.REFUTED, f"Hypothesis crashed on witness instance: {str(ex)}")

            try:
                oracle_out = reference_oracle(instance)
            except Exception as ex:
                # Oracle failure during search halts as UNRESOLVED
                return (
                    None,
                    None,
                    EpistemicStatus.UNRESOLVED,
                    f"Reference oracle threw error during exploration on instance: {str(ex)}",
                )

            # Law 2: Single counterexample is sufficient for definitive rejection
            if hyp_out != oracle_out:
                cert_id = f"ref_{uuid.uuid4().hex[:10]}"
                ref_cert = RefutationCertificate(
                    certificate_id=cert_id,
                    hypothesis_id=hypothesis_id,
                    schema=schema,
                    counterexample_witness={"instance": str(instance)},
                    hypothesis_output=str(hyp_out),
                    oracle_output=str(oracle_out),
                    envelope_fingerprint=envelope.fingerprint(),
                    status=EpistemicStatus.REFUTED,
                )
                return (
                    ref_cert,
                    None,
                    EpistemicStatus.REFUTED,
                    f"Hypothesis falsified by counterexample witness: got {hyp_out}, oracle expected {oracle_out}.",
                )

        # 3. Exhaustive Search Completed with Zero Counterexamples
        # Law 3: Finite exhaustive testing corroborates strictly within envelope (SUPPORTED)
        # Law 4: No search-to-proof laundering (never PROVEN)
        cert_id = f"corrob_{uuid.uuid4().hex[:10]}"
        corrob_cert = CorroborationCertificate(
            certificate_id=cert_id,
            hypothesis_id=hypothesis_id,
            schema=schema,
            envelope_fingerprint=envelope.fingerprint(),
            states_evaluated=states_evaluated,
            exhaustive_within_envelope=True,
            status=EpistemicStatus.SUPPORTED,
        )

        return (
            None,
            corrob_cert,
            EpistemicStatus.SUPPORTED,
            f"Exhaustive search across {states_evaluated} states completed with zero counterexamples.",
        )
