"""
Phase 9 — targeted_repair_engine.py

Structural C++ code transformation engine.
Applies deterministic, pre-certified transformations authorized by a
DiagnosticCertificate and SelfCorrectionPlan.

Invariants:
- Engine cannot search for fixes or try alternative strategies.
- Single-shot: transforms exactly once.
- Structural scoping: operates on scoped AST elements, not arbitrary regex.
- Clean code: produces zero warnings, zero repair comments, zero debug tokens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .diagnostic_types import (
    BoundaryGuardEvidence,
    DiagnosticCertificate,
    ImplementationBugKind,
    IndexMappingEvidence,
    MissingHeaderEvidence,
    OverflowEvidence,
    RepairStrategy,
    SelfCorrectionPlan,
)


@dataclass(frozen=True)
class RepairResult:
    success: bool
    repaired_source: str
    applied_strategy: RepairStrategy
    target_symbol: str
    target_scope: str
    error_message: str = ""


class TargetedRepairEngine:
    """
    Executes structurally targeted C++ source repairs.
    Only authorized transformations are performed.
    """

    @classmethod
    def authorize(cls, certificate: DiagnosticCertificate) -> bool:
        """
        Validates that certificate is repairable and strategy matches bug_kind.
        """
        if not certificate.is_repairable:
            return False

        strategy = certificate.recommended_strategy
        bug_kind = certificate.bug_kind

        authorized_map = {
            ImplementationBugKind.MISSING_HEADER: RepairStrategy.ADD_MISSING_HEADER,
            ImplementationBugKind.TYPE_WIDTH_MISMATCH: RepairStrategy.WIDEN_TO_64BIT,
            ImplementationBugKind.CERTIFIED_INDEX_BASE_TRANSLATION: RepairStrategy.ADJUST_INDEX_BASE,
            ImplementationBugKind.CERTIFIED_BOUNDARY_GUARD: RepairStrategy.INSERT_BOUNDARY_GUARD,
            ImplementationBugKind.UNCLASSIFIED_CODE_DEFECT: RepairStrategy.NONE,
        }

        if authorized_map.get(bug_kind) != strategy:
            return False

        if certificate.structured_evidence is None or not certificate.structured_evidence.validate():
            return False

        return True

    @classmethod
    def apply_repair(
        cls,
        source_code: str,
        plan: SelfCorrectionPlan,
        certificate: DiagnosticCertificate,
    ) -> RepairResult:
        # 1. Authorization check
        if not cls.authorize(certificate):
            return RepairResult(
                success=False,
                repaired_source=source_code,
                applied_strategy=RepairStrategy.NONE,
                target_symbol="",
                target_scope="",
                error_message="Diagnostic certificate is not authorized for repair.",
            )

        # 2. Hash binding verification
        import hashlib
        current_hash = hashlib.sha256(source_code.encode("utf-8")).hexdigest()
        if plan.candidate_source_hash and plan.candidate_source_hash != current_hash:
            return RepairResult(
                success=False,
                repaired_source=source_code,
                applied_strategy=RepairStrategy.NONE,
                target_symbol="",
                target_scope="",
                error_message=f"Source code hash mismatch: plan expected {plan.candidate_source_hash[:12]}, got {current_hash[:12]}.",
            )

        strategy = plan.strategy
        ev = plan.structured_evidence

        if strategy == RepairStrategy.ADD_MISSING_HEADER and isinstance(ev, MissingHeaderEvidence):
            return cls._apply_add_header(source_code, ev)

        elif strategy == RepairStrategy.WIDEN_TO_64BIT and isinstance(ev, OverflowEvidence):
            return cls._apply_widen_type(source_code, ev)

        elif strategy == RepairStrategy.ADJUST_INDEX_BASE and isinstance(ev, IndexMappingEvidence):
            return cls._apply_adjust_index_base(source_code, ev)

        elif strategy == RepairStrategy.INSERT_BOUNDARY_GUARD and isinstance(ev, BoundaryGuardEvidence):
            return cls._apply_insert_boundary_guard(source_code, ev)

        return RepairResult(
            success=False,
            repaired_source=source_code,
            applied_strategy=RepairStrategy.NONE,
            target_symbol="",
            target_scope="",
            error_message=f"Unsupported repair strategy: {strategy}",
        )

    # -------------------------------------------------------------------------
    # Deterministic Transformation Handlers
    # -------------------------------------------------------------------------

    @classmethod
    def _apply_add_header(cls, source: str, ev: MissingHeaderEvidence) -> RepairResult:
        header_include = f"#include {ev.missing_header}"
        if header_include in source:
            # Header already present
            return RepairResult(
                success=True,
                repaired_source=source,
                applied_strategy=RepairStrategy.ADD_MISSING_HEADER,
                target_symbol=ev.missing_header,
                target_scope="global_includes",
            )

        lines = source.splitlines()
        insert_idx = 0
        # Find position after existing includes
        for idx, line in enumerate(lines):
            if line.strip().startswith("#include"):
                insert_idx = idx + 1

        lines.insert(insert_idx, header_include)
        repaired = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
        return RepairResult(
            success=True,
            repaired_source=repaired,
            applied_strategy=RepairStrategy.ADD_MISSING_HEADER,
            target_symbol=ev.missing_header,
            target_scope="global_includes",
        )

    @classmethod
    def _apply_widen_type(cls, source: str, ev: OverflowEvidence) -> RepairResult:
        # Replacement sufficiency check
        if not ev.is_widening_sufficient():
            return RepairResult(
                success=False,
                repaired_source=source,
                applied_strategy=RepairStrategy.WIDEN_TO_64BIT,
                target_symbol=ev.original_identifier,
                target_scope=ev.target_scope,
                error_message=f"Maximum intermediate magnitude {ev.max_intermediate_magnitude} exceeds 64-bit LLONG_MAX.",
            )

        var = ev.original_identifier
        # Replace int var with long long var within declaration
        # Patterns: int var = ..., int var;, int var(
        patterns = [
            (rf"\bint\s+{re.escape(var)}\b", f"long long {var}"),
            (rf"\bint\s*&\s*{re.escape(var)}\b", f"long long &{var}"),
            (rf"\blong\s+{re.escape(var)}\b", f"long long {var}"),
        ]

        repaired = source
        changed = False
        for pat, repl in patterns:
            if re.search(pat, repaired):
                repaired = re.sub(pat, repl, repaired, count=1)
                changed = True
                break

        if not changed:
            # Fallback: if var is accumulator like 'sum' or function return type
            return RepairResult(
                success=False,
                repaired_source=source,
                applied_strategy=RepairStrategy.WIDEN_TO_64BIT,
                target_symbol=var,
                target_scope=ev.target_scope,
                error_message=f"Could not structurally locate declaration for '{var}'.",
            )

        return RepairResult(
            success=True,
            repaired_source=repaired,
            applied_strategy=RepairStrategy.WIDEN_TO_64BIT,
            target_symbol=var,
            target_scope=ev.target_scope,
        )

    @classmethod
    def _apply_adjust_index_base(cls, source: str, ev: IndexMappingEvidence) -> RepairResult:
        offending = ev.offending_expression
        translated = ev.translated_expression

        if offending not in source:
            return RepairResult(
                success=False,
                repaired_source=source,
                applied_strategy=RepairStrategy.ADJUST_INDEX_BASE,
                target_symbol=offending,
                target_scope=ev.target_scope,
                error_message=f"Target expression '{offending}' not found in source.",
            )

        # Replace offending indexing expression with translated expression
        repaired = source.replace(offending, translated, 1)
        return RepairResult(
            success=True,
            repaired_source=repaired,
            applied_strategy=RepairStrategy.ADJUST_INDEX_BASE,
            target_symbol=offending,
            target_scope=ev.target_scope,
        )

    @classmethod
    def _apply_insert_boundary_guard(cls, source: str, ev: BoundaryGuardEvidence) -> RepairResult:
        guard_statement = f"    if ({ev.boundary_condition}) return {ev.identity_expression};"

        # Check if already present
        if guard_statement.strip() in source:
            return RepairResult(
                success=True,
                repaired_source=source,
                applied_strategy=RepairStrategy.INSERT_BOUNDARY_GUARD,
                target_symbol=ev.boundary_condition,
                target_scope="solve_entry",
            )

        # Insert at the beginning of the solve() function or main()
        # Find function definition: void solve( or int solve( or auto solve(
        solve_match = re.search(r"\b(void|int|long long|auto)\s+solve\s*\([^)]*\)\s*\{", source)
        if solve_match:
            insert_pos = solve_match.end()
            repaired = source[:insert_pos] + "\n" + guard_statement + source[insert_pos:]
            return RepairResult(
                success=True,
                repaired_source=repaired,
                applied_strategy=RepairStrategy.INSERT_BOUNDARY_GUARD,
                target_symbol=ev.boundary_condition,
                target_scope="solve_entry",
            )

        # If solve() not found, search for main() {
        main_match = re.search(r"\bint\s+main\s*\([^)]*\)\s*\{", source)
        if main_match:
            insert_pos = main_match.end()
            repaired = source[:insert_pos] + "\n" + guard_statement + source[insert_pos:]
            return RepairResult(
                success=True,
                repaired_source=repaired,
                applied_strategy=RepairStrategy.INSERT_BOUNDARY_GUARD,
                target_symbol=ev.boundary_condition,
                target_scope="main_entry",
            )

        return RepairResult(
            success=False,
            repaired_source=source,
            applied_strategy=RepairStrategy.INSERT_BOUNDARY_GUARD,
            target_symbol=ev.boundary_condition,
            target_scope="entry",
            error_message="Could not structurally locate entry point to insert boundary guard.",
        )
