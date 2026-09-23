"""
Phase 9 — failure_evidence.py

FailureEvidence captures all raw execution artifacts for a failed
candidate run. This is the boundary between the verifier and the
diagnostic pipeline — it carries facts, not conclusions.
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class FailureEvidence:
    """
    Raw execution evidence for one failed candidate run.

    All fields are measurements, not interpretations. The diagnostic
    pipeline draws conclusions; this type only records what happened.
    """
    # Identity
    candidate_source_hash: str
    test_vector_hash: str
    compiler_identity_hash: str
    compiler_flags: Tuple[str, ...]

    # Execution outcome
    exit_code: int
    signal_received: Optional[int]      # e.g. 11 for SIGSEGV, 8 for SIGFPE
    stdout_hash: str
    stderr_hash: str
    stderr_excerpt: str                  # First 2000 chars of stderr (for diagnostics)
    wall_time_ms: float
    peak_rss_kb: int

    # Compiler-specific
    compiler_diagnostic_lines: Tuple[str, ...]

    # Timing context
    execution_timestamp_utc: str

    def is_compiler_failure(self) -> bool:
        """Exit code from compilation step, not execution."""
        return any("error:" in line or "fatal error:" in line
                   for line in self.compiler_diagnostic_lines)

    def is_runtime_signal(self) -> bool:
        return self.signal_received is not None and self.signal_received > 0

    def is_tle(self) -> bool:
        """Heuristic: process killed by SIGKILL (9) typically indicates TLE in contest judges."""
        return self.signal_received == 9 or self.exit_code == 124

    def fingerprint(self) -> str:
        """Stable identifier for this failure instance (used in reproducibility comparison)."""
        parts = [
            self.candidate_source_hash,
            self.test_vector_hash,
            self.compiler_identity_hash,
            str(self.exit_code),
            str(self.signal_received),
            self.stdout_hash,
            self.stderr_hash,
        ]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()


def capture_failure_evidence(
    *,
    candidate_source_hash: str,
    test_vector_hash: str,
    compiler_identity_hash: str,
    compiler_flags: Tuple[str, ...],
    completed_process: "subprocess.CompletedProcess[str]",
    wall_time_ms: float,
    peak_rss_kb: int,
    execution_timestamp_utc: str,
    signal_received: Optional[int] = None,
) -> FailureEvidence:
    """
    Build a FailureEvidence from a completed subprocess.

    Callers supply measured values; this function hashes outputs and
    extracts compiler diagnostics.
    """
    stderr_text = completed_process.stderr or ""
    stdout_text = completed_process.stdout or ""

    stderr_hash = hashlib.sha256(stderr_text.encode()).hexdigest()
    stdout_hash = hashlib.sha256(stdout_text.encode()).hexdigest()

    # Extract compiler diagnostic lines (lines containing "error:" or "warning:")
    compiler_diagnostic_lines = tuple(
        line for line in stderr_text.splitlines()
        if "error:" in line or "warning:" in line or "note:" in line
    )

    return FailureEvidence(
        candidate_source_hash=candidate_source_hash,
        test_vector_hash=test_vector_hash,
        compiler_identity_hash=compiler_identity_hash,
        compiler_flags=compiler_flags,
        exit_code=completed_process.returncode,
        signal_received=signal_received,
        stdout_hash=stdout_hash,
        stderr_hash=stderr_hash,
        stderr_excerpt=stderr_text[:2000],
        wall_time_ms=wall_time_ms,
        peak_rss_kb=peak_rss_kb,
        compiler_diagnostic_lines=compiler_diagnostic_lines,
        execution_timestamp_utc=execution_timestamp_utc,
    )
