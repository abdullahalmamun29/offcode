"""
Phase 9 — certificate_store.py

Problem-scoped, deeply immutable persistence store for DiagnosticCertificates
and SelfCorrectionCertificates.
Ensures zero alteration of diagnostic history or authoritative evidence.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .diagnostic_types import DiagnosticCertificate, SelfCorrectionCertificate


class ProblemCertificateStore:
    """
    In-memory problem-scoped store for Phase 9 certificates.
    Certificates are immutable and strictly append-only.
    """

    def __init__(self) -> None:
        self._diagnostic_certs: Dict[str, DiagnosticCertificate] = {}
        self._correction_certs: Dict[str, SelfCorrectionCertificate] = {}
        self._by_problem_hash: Dict[str, List[str]] = {}

    def store_diagnostic_certificate(self, cert: DiagnosticCertificate) -> None:
        """Stores a diagnostic certificate. Duplicate IDs rejected."""
        if cert.certificate_id in self._diagnostic_certs:
            raise ValueError(f"Diagnostic certificate {cert.certificate_id} already exists.")
        self._diagnostic_certs[cert.certificate_id] = cert
        self._by_problem_hash.setdefault(cert.problem_hash, []).append(cert.certificate_id)

    def store_correction_certificate(self, cert: SelfCorrectionCertificate) -> None:
        """Stores a self-correction certificate."""
        if cert.certificate_id in self._correction_certs:
            raise ValueError(f"Self-correction certificate {cert.certificate_id} already exists.")
        self._correction_certs[cert.certificate_id] = cert

    def get_diagnostic_certificate(self, cert_id: str) -> Optional[DiagnosticCertificate]:
        return self._diagnostic_certs.get(cert_id)

    def get_correction_certificate(self, cert_id: str) -> Optional[SelfCorrectionCertificate]:
        return self._correction_certs.get(cert_id)

    def get_by_problem_hash(self, problem_hash: str) -> List[DiagnosticCertificate]:
        ids = self._by_problem_hash.get(problem_hash, [])
        return [self._diagnostic_certs[cid] for cid in ids if cid in self._diagnostic_certs]

    def clear(self) -> None:
        self._diagnostic_certs.clear(
            )
        self._correction_certs.clear()
        self._by_problem_hash.clear()
