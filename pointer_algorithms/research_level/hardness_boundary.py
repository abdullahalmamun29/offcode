"""
Phase 10 — hardness_boundary.py

Pillar IV: Parameterized Complexity & Hardness Boundary.
- NP-Hardness established via certified reverse polynomial reduction H <=_p P (Law 6).
- Exact Exponential and FPT algorithms (Bitmask DP, Meet-in-the-Middle).
- Budget guards enforcing Law 7 (budget exceeded != problem unsatisfiable).
"""

from __future__ import annotations

import math
import uuid
from typing import Mapping, Optional, Tuple

from .research_types import (
    EpistemicStatus,
    HardnessCertificate,
    ReductionCertificate,
    ResourceFeasibilityCertificate,
)


class HardnessBoundaryEngine:
    """
    Evaluates computational complexity barriers and parameterized feasibility.
    """

    KNOWN_NP_HARD_CORES: Tuple[str, ...] = (
        "3SAT",
        "VERTEX_COVER",
        "HAMILTONIAN_CYCLE",
        "TSP",
        "SUBSET_SUM",
        "EXACT_COVER",
    )

    MAX_OPERATIONS_BUDGET: int = 100_000_000  # Contest standard ~ 10^8 operations / sec

    @classmethod
    def certify_hardness_via_reduction(
        cls,
        user_problem_id: str,
        known_hard_core_id: str,
        reduction_cert: ReductionCertificate,
    ) -> Tuple[Optional[HardnessCertificate], EpistemicStatus, str]:
        """
        Law 6: NP-hardness requires a certified reverse reduction H <=_p P from a known hard core.
        Superficial resemblance without a reduction certificate is strictly rejected.
        """
        if known_hard_core_id not in cls.KNOWN_NP_HARD_CORES:
            return (
                None,
                EpistemicStatus.UNRESOLVED,
                f"Core '{known_hard_core_id}' is not in certified known NP-hard core registry.",
            )

        # The reduction must map known_hard_core -> user_problem_id
        if not reduction_cert.is_valid():
            return (
                None,
                EpistemicStatus.UNRESOLVED,
                "Reduction certificate failed mathematical validity gates.",
            )

        cert_id = f"hard_{uuid.uuid4().hex[:10]}"
        cert = HardnessCertificate(
            certificate_id=cert_id,
            user_problem_id=user_problem_id,
            known_hard_core_id=known_hard_core_id,
            reduction_proof=reduction_cert,
            is_np_hard=True,
            status=EpistemicStatus.PROVEN,
        )
        return (cert, EpistemicStatus.PROVEN, f"NP-hardness mathematically proven via reduction {known_hard_core_id} <=_p {user_problem_id}.")

    @classmethod
    def evaluate_exact_exponential_feasibility(
        cls,
        algorithm_name: str,
        parameter_name: str,
        n_val: int,
    ) -> ResourceFeasibilityCertificate:
        """
        Evaluates exact exponential algorithms:
        - Bitmask DP (e.g. TSP): O(2^N * N^2)
        - Meet-in-the-Middle (e.g. Subset Sum): O(2^(N/2) * log(N))
        Enforces Law 7: Exceeding budget yields PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY (never UNSATISFIABLE).
        """
        cert_id = f"feas_{uuid.uuid4().hex[:10]}"

        if algorithm_name == "bitmask_dp_tsp":
            formula = "O(2^N * N^2)"
            if n_val > 60:
                est_ops = 10**25
            else:
                est_ops = (2 ** n_val) * (n_val ** 2)
            feasible = est_ops <= cls.MAX_OPERATIONS_BUDGET
        elif algorithm_name == "meet_in_the_middle":
            formula = "O(2^(N/2) * log(2^(N/2)))"
            half_n = n_val // 2
            if half_n > 60:
                est_ops = 10**25
            else:
                est_ops = int((2 ** half_n) * max(1, half_n))
            feasible = est_ops <= cls.MAX_OPERATIONS_BUDGET
        else:
            formula = "O(2^N)"
            est_ops = 2 ** min(n_val, 60)
            feasible = est_ops <= cls.MAX_OPERATIONS_BUDGET

        status_label = (
            "FEASIBLE"
            if feasible
            else "PARAMETER_EXCEEDS_CERTIFIED_FEASIBILITY"
        )

        return ResourceFeasibilityCertificate(
            certificate_id=cert_id,
            algorithm_name=algorithm_name,
            parameter_name=parameter_name,
            parameter_value=n_val,
            complexity_formula=formula,
            estimated_operations=est_ops,
            max_operations_budget=cls.MAX_OPERATIONS_BUDGET,
            is_feasible=feasible,
            status_label=status_label,
        )
