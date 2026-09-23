"""
Phase 9 — oracle_integrity.py

Priority 2 in the 7-tier decision table: Oracle Integrity Gate.
Independently verifies reference oracle behavior.

OracleStatus distinctions:
- DEFECT_CONFIRMED: Oracle crashed, raised unhandled exception, or returned
  divergent outputs on identical inputs across runs. Maps to ORACLE_DEFECT.
- INCONSISTENT: Metamorphic violation or soft mismatch where oracle correctness
  cannot be conclusively disproven without proof. Maps to UNRESOLVED (Priority 7).
- UNRESOLVED: Oracle gave no output or ambiguous response for non-crash reason.
- HEALTHY: Oracle verified healthy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence

from .diagnostic_types import OracleStatus


@dataclass(frozen=True)
class OracleExecutionEvidence:
    """Execution evidence for reference oracle on a specific test vector."""
    exit_code: int
    stdout: str
    stderr: str
    crashed: bool
    exception_name: Optional[str] = None
    wall_time_ms: float = 0.0


@dataclass(frozen=True)
class OracleIntegrityResult:
    status: OracleStatus
    reason: str = ""
    witness: Optional[str] = None

    def is_healthy(self) -> bool:
        return self.status == OracleStatus.HEALTHY


class OracleIntegrityGate:
    """
    Evaluates oracle correctness independently of candidate outputs.
    Follows strict anti-guessing rules: only definitive crashes or multi-run
    divergences produce DEFECT_CONFIRMED. Metamorphic anomalies produce INCONSISTENT.
    """

    @classmethod
    def evaluate(
        cls,
        oracle_runs: Sequence[OracleExecutionEvidence],
        metamorphic_check_passed: Optional[bool] = None,
        secondary_oracle_agreement: Optional[bool] = None,
    ) -> OracleIntegrityResult:
        if not oracle_runs:
            return OracleIntegrityResult(
                status=OracleStatus.UNRESOLVED,
                reason="No oracle execution evidence provided.",
            )

        # 1. Crash or non-zero exit in oracle
        for idx, run in enumerate(oracle_runs):
            if run.crashed or run.exit_code != 0:
                return OracleIntegrityResult(
                    status=OracleStatus.DEFECT_CONFIRMED,
                    reason=f"Oracle crashed or exited with non-zero code {run.exit_code} on run {idx}",
                    witness=run.stderr[:400] if run.stderr else f"Exit code {run.exit_code}",
                )
            if run.exception_name:
                return OracleIntegrityResult(
                    status=OracleStatus.DEFECT_CONFIRMED,
                    reason=f"Oracle threw unhandled exception {run.exception_name}",
                    witness=run.stderr[:400],
                )

        # 2. Non-deterministic oracle behavior across identical runs
        if len(oracle_runs) >= 2:
            first_out = oracle_runs[0].stdout.strip()
            for idx, run in enumerate(oracle_runs[1:], start=1):
                if run.stdout.strip() != first_out:
                    return OracleIntegrityResult(
                        status=OracleStatus.DEFECT_CONFIRMED,
                        reason=f"Oracle produced non-deterministic outputs across identical runs: run 0 vs run {idx}",
                        witness=f"Run 0: {first_out[:100]} vs Run {idx}: {run.stdout.strip()[:100]}",
                    )

        # 3. Metamorphic inconsistency check
        # A metamorphic property failure does NOT prove oracle is defective;
        # it proves INCONSISTENCY (e.g., metamorphic relation might be invalid for problem)
        if metamorphic_check_passed is False:
            return OracleIntegrityResult(
                status=OracleStatus.INCONSISTENT,
                reason="Metamorphic consistency property violated; oracle cannot be certified sound.",
                witness="Metamorphic test failed",
            )

        # 4. Secondary oracle disagreement
        if secondary_oracle_agreement is False:
            return OracleIntegrityResult(
                status=OracleStatus.INCONSISTENT,
                reason="Disagreement between primary and secondary reference oracles.",
                witness="Multi-oracle consensus failure",
            )

        return OracleIntegrityResult(
            status=OracleStatus.HEALTHY,
            reason="Oracle executed cleanly and deterministically.",
        )
