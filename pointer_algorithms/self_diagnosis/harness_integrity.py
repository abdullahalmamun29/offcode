"""
Phase 9 — harness_integrity.py

Priority 1 in the 7-tier decision table: Test Harness Integrity Gate.
Evaluates whether the test harness itself, compiler, runtime environment,
or sandbox failed, rather than the candidate implementation or problem logic.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from typing import Optional, Tuple

from .diagnostic_types import HarnessStatus
from .failure_evidence import FailureEvidence


@dataclass(frozen=True)
class HarnessIntegrityResult:
    status: HarnessStatus
    reason: str = ""
    defect_details: Optional[str] = None

    def is_healthy(self) -> bool:
        return self.status == HarnessStatus.HEALTHY


class HarnessIntegrityGate:
    """
    Evaluates execution environment integrity.
    If the harness fails, execution stops immediately as TEST_HARNESS_DEFECT.
    No code or reasoning mutation is permitted.
    """

    KNOWN_HARNESS_ERROR_PATTERNS: Tuple[str, ...] = (
        "No space left on device",
        "Permission denied: '/tmp",
        "cannot execute: required file not found",
        "fatal error: killed by out-of-memory",
        "Operating system error",
        "Segmentation fault in compiler",
        "internal compiler error:",
        "g++: fatal error: Killed signal terminated program",
        "Failed to spawn child process",
        "Broken pipe",
    )

    @classmethod
    def evaluate(
        cls,
        evidence: FailureEvidence,
        compiler_path: Optional[str] = "g++",
    ) -> HarnessIntegrityResult:
        # 1. Compiler binary availability check
        if compiler_path and not shutil.which(compiler_path) and not os.path.exists(compiler_path):
            return HarnessIntegrityResult(
                status=HarnessStatus.DEFECT_CONFIRMED,
                reason="Compiler binary not found or not executable",
                defect_details=f"Missing compiler at: {compiler_path}",
            )

        # 2. Check for known compiler crashes / internal errors / OS failures
        combined_stderr = evidence.stderr_excerpt
        for pattern in cls.KNOWN_HARNESS_ERROR_PATTERNS:
            if pattern.lower() in combined_stderr.lower():
                return HarnessIntegrityResult(
                    status=HarnessStatus.DEFECT_CONFIRMED,
                    reason=f"Harness/OS defect pattern detected: {pattern}",
                    defect_details=evidence.stderr_excerpt[:500],
                )

        # 3. Check for external harness timeouts / killed execution by judge harness
        # If exit_code indicates fatal OS or sandbox restriction unrelated to binary execution
        if evidence.exit_code == 127:
            # Command not found or shell wrapper error
            return HarnessIntegrityResult(
                status=HarnessStatus.DEFECT_CONFIRMED,
                reason="Subprocess command not found (exit code 127)",
                defect_details="Shell failed to locate command or shared library missing",
            )

        return HarnessIntegrityResult(status=HarnessStatus.HEALTHY)
