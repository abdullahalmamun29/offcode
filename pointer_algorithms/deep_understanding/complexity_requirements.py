"""
CHUP Phase 6 — Complexity Requirements & Resource Envelope.

Deduces a Complexity Requirement Envelope from problem parameters and time/memory limits.

Authoritative Architecture Separation:
- Phase 6 asks: "What complexity envelope does the statement and parameter scale imply?"
- Phase 5 evaluates: "Which candidate algorithmic structure satisfies that envelope?"
Phase 6 does NOT duplicate Phase 5's ResourceEvaluator or claim universal algorithms.

Distinguishes:
1. HARD_NUMERIC bounds (N <= 2e5, Q <= 2e5, T <= 2.0s, M <= 256MB)
2. HARD_ASYMPTOTIC upper envelopes (e.g. approximately O((N+Q) log N))
3. ESTIMATED_MACHINE models (configurable ops/sec and safety margins)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
import math
from pointer_algorithms.deep_understanding.fact_model import FactSet
from pointer_algorithms.multi_constraint.resource_evaluator import SymbolicBudget


class ComplexityBoundKind(Enum):
    HARD_NUMERIC = "HARD_NUMERIC"
    HARD_ASYMPTOTIC = "HARD_ASYMPTOTIC"
    ESTIMATED_MACHINE = "ESTIMATED_MACHINE"


@dataclass(frozen=True)
class MachineModel:
    """
    Configurable engineering resource estimates.
    Explicitly designated as empirical estimation, never mathematical law.
    """
    scalar_ops_per_sec: float = 2.0e8
    safety_margin: float = 1.5
    bytes_per_int64: int = 8


@dataclass(frozen=True)
class ComplexityRequirementEnvelope:
    """
    Immutable specification of the required complexity envelope.
    """
    numeric_bounds: Dict[str, int]
    time_limit_sec: float
    memory_limit_mb: float
    max_estimated_operations: float
    max_estimated_bytes: float
    target_asymptotic_class: str
    machine_model: MachineModel

    def to_symbolic_budget(self) -> SymbolicBudget:
        """
        Translates envelope into Phase 5 SymbolicBudget for candidate evaluation.
        """
        return SymbolicBudget(
            N=self.numeric_bounds.get("n", 100_000),
            Q=self.numeric_bounds.get("q", 100_000),
            V=self.numeric_bounds.get("v", 100_000),
            E=self.numeric_bounds.get("e", 200_000),
            time_limit_ms=int(self.time_limit_sec * 1000),
            memory_limit_mb=int(self.memory_limit_mb),
            ops_per_second=int(self.machine_model.scalar_ops_per_sec / self.machine_model.safety_margin)
        )


class ComplexityRequirementEngine:
    """
    Formulates complexity requirement envelopes from facts and input specifications.
    """

    @classmethod
    def derive_envelope(
        cls,
        facts: FactSet,
        machine_model: Optional[MachineModel] = None
    ) -> ComplexityRequirementEnvelope:
        model = machine_model or MachineModel()

        # Extract numeric bounds from facts
        bounds: Dict[str, int] = {}
        for f in facts:
            if f.name.endswith("_BOUND") or f.name.endswith("_COUNT"):
                key = f.name.split("_")[0].lower()
                if isinstance(f.value, int):
                    bounds[key] = f.value

        n = bounds.get("n") or bounds.get("vertex")
        q = bounds.get("q") or bounds.get("query")

        t_sec = 2.0
        t_fact = facts.get("TIME_LIMIT_SEC")
        if t_fact and isinstance(t_fact.value, (int, float)):
            t_sec = float(t_fact.value)

        m_mb = 256.0
        m_fact = facts.get("MEMORY_LIMIT_MB")
        if m_fact and isinstance(m_fact.value, (int, float)):
            m_mb = float(m_fact.value)

        max_ops = (t_sec * model.scalar_ops_per_sec) / model.safety_margin
        max_bytes = m_mb * 1024 * 1024

        # Deduce required asymptotic envelope from scale
        # (This is an upper envelope constraint, NOT an algorithm selection)
        if n is None:
            asymp = "UNSPECIFIED"
        elif n <= 20:
            asymp = "O(2^N)"
        elif n <= 500:
            asymp = "O(N^3)"
        elif n <= 5000:
            asymp = "O(N^2)"
        elif n <= 300_000:
            asymp = "O((N+Q) log N)" if q else "O(N log N)"
        elif n <= 10_000_000:
            asymp = "O(N)"
        else:
            asymp = "O(log N)"

        return ComplexityRequirementEnvelope(
            numeric_bounds=bounds,
            time_limit_sec=t_sec,
            memory_limit_mb=m_mb,
            max_estimated_operations=max_ops,
            max_estimated_bytes=max_bytes,
            target_asymptotic_class=asymp,
            machine_model=model
        )
