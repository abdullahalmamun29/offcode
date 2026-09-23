"""
Phase 9 — generation_provenance.py

GenerationProvenance binds a candidate source file to the authoritative
plan that generated it. The repair gate rejects any source whose hash
does not match the recorded provenance.

This prevents:
    VALID_OPTIMAL_PLAN + manually modified source + failure
    → Phase 9 incorrectly accepting responsibility for repair.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GenerationProvenance:
    """
    Cryptographic binding from authoritative plan to generated source.

    plan → generator → source is auditable end-to-end.
    """
    plan_hash: str                  # SHA-256 of the Phase 5 authoritative plan
    candidate_source_hash: str      # SHA-256 of the generated source bytes
    generator_version: str          # e.g. "codeForge-cpSolver-v1.0"
    generation_timestamp_utc: str
    generation_contract_hash: str   # SHA-256 of the generator contract / template

    def fingerprint(self) -> str:
        """Stable compound fingerprint for all provenance fields."""
        fields = {
            "plan_hash": self.plan_hash,
            "candidate_source_hash": self.candidate_source_hash,
            "generator_version": self.generator_version,
            "generation_timestamp_utc": self.generation_timestamp_utc,
            "generation_contract_hash": self.generation_contract_hash,
        }
        canonical = json.dumps(fields, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def verify(self, plan_hash: str, candidate_source_hash: str) -> bool:
        """
        Returns True iff both hashes match what was recorded at generation time.
        The repair gate calls this before any repair is attempted.
        """
        return (self.plan_hash == plan_hash
                and self.candidate_source_hash == candidate_source_hash)


class ProvenanceVerificationResult:
    """Result of a provenance check."""
    __slots__ = ("verified", "reason")

    def __init__(self, verified: bool, reason: str = "") -> None:
        self.verified = verified
        self.reason = reason

    def __bool__(self) -> bool:
        return self.verified


def verify_generation_provenance(
    provenance: GenerationProvenance,
    plan_hash: str,
    candidate_source_hash: str,
) -> ProvenanceVerificationResult:
    """
    Verify candidate source was generated from the specified plan.

    Returns a failed result (→ UNRESOLVED, no repair) if either hash mismatches.
    """
    if provenance.plan_hash != plan_hash:
        return ProvenanceVerificationResult(
            False,
            f"Plan hash mismatch: recorded={provenance.plan_hash[:16]}… "
            f"current={plan_hash[:16]}…"
        )
    if provenance.candidate_source_hash != candidate_source_hash:
        return ProvenanceVerificationResult(
            False,
            f"Source hash mismatch: recorded={provenance.candidate_source_hash[:16]}… "
            f"current={candidate_source_hash[:16]}…"
        )
    return ProvenanceVerificationResult(True)


def build_source_hash(source_bytes: bytes) -> str:
    """Canonical SHA-256 of C++ source bytes."""
    return hashlib.sha256(source_bytes).hexdigest()


def build_plan_hash(plan_dict: dict) -> str:
    """Canonical SHA-256 of the Phase 5 plan serialized deterministically."""
    canonical = json.dumps(plan_dict, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()
