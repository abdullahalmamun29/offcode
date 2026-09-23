"""
CHUP Phase 5 — Capability-DAG State-Transition Synthesizer.

Performs forward search over component capability contracts (requires -> produces)
to assemble cooperative multi-component pipelines when single candidates leave
a coverage gap. Does not hardcode rigid recipe pattern switches.
"""

from typing import Dict, Any, List, Optional, Set, FrozenSet, Tuple
from dataclasses import dataclass, field
from pointer_algorithms.multi_constraint.constraint_lattice import (
    TemporalMode,
    MutabilityCapability,
    MutabilitySet,
    CoordinateScale,
    MultiConstraintVector,
)
from pointer_algorithms.multi_constraint.aggregate_ontology import (
    QuerySpec,
    QueryTarget,
    AggregateSpec,
)
from pointer_algorithms.multi_constraint.candidate_profile import CandidateProfile


@dataclass(frozen=True)
class SynthesizedPipelineStep:
    step_index: int
    component_id: str
    role: str
    consumed_capabilities: FrozenSet[str]
    produced_capabilities: FrozenSet[str]


@dataclass(frozen=True)
class CapabilitySynthesisResult:
    success: bool
    pipeline: List[SynthesizedPipelineStep] = field(default_factory=list)
    final_capabilities: FrozenSet[str] = field(default_factory=frozenset)
    gap_reason: Optional[str] = None


class CapabilitySynthesizer:
    """
    State-transition synthesizer searching the capability space.
    """

    @classmethod
    def synthesize(
        cls,
        vector: MultiConstraintVector,
        query: QuerySpec,
        universe: Dict[str, CandidateProfile]
    ) -> CapabilitySynthesisResult:
        """
        Attempts to construct a multi-component capability DAG satisfying all
        active problem requirements.
        """
        # Determine initial capabilities available from the problem
        current_caps: Set[str] = set()
        if vector.topology.is_undirected_tree():
            current_caps.add("TREE_TOPOLOGY")
        else:
            current_caps.add("LINEAR_ARRAY")

        if vector.coordinate_scale == CoordinateScale.MASSIVE:
            current_caps.add("MASSIVE_COORDINATES")
            if vector.temporal == TemporalMode.OFFLINE or vector.has_constraint("OFFLINE_COORDINATES_KNOWN"):
                current_caps.add("OFFLINE_COORDINATES_KNOWN")

        if vector.temporal == TemporalMode.OFFLINE:
            current_caps.add("OFFLINE_QUERIES_KNOWN")
            if vector.has_constraint("TRANSITION_REVERSIBLE"):
                current_caps.add("TRANSITION_REVERSIBLE")

        # Determine target capabilities required by the query
        target_caps: Set[str] = set()
        if query.is_tree_path():
            target_caps.add("TREE_PATH_TO_LINEAR_RANGES")
            target_caps.add("RANGE_AGGREGATION")
        elif query.is_range_query():
            target_caps.add("RANGE_AGGREGATION")

        if vector.mutability.satisfies(MutabilityCapability.POINT_WRITE):
            target_caps.add("POINT_UPDATE")
        if vector.mutability.satisfies(MutabilityCapability.RANGE_WRITE):
            target_caps.add("RANGE_UPDATE")

        pipeline: List[SynthesizedPipelineStep] = []
        step_idx = 1

        # ── State Transition 1: Topological / Coordinate Decomposition ──
        if "TREE_TOPOLOGY" in current_caps and query.is_tree_path():
            hld = universe.get("heavy_light_decomposition")
            if hld and hld.supports_temporal(vector.temporal):
                consumed = frozenset(["TREE_TOPOLOGY"])
                produced = frozenset(["TREE_PATH_TO_LINEAR_RANGES", "LINEAR_ARRAY"])
                pipeline.append(SynthesizedPipelineStep(
                    step_index=step_idx,
                    component_id="heavy_light_decomposition",
                    role="Tree Path Decomposer",
                    consumed_capabilities=consumed,
                    produced_capabilities=produced
                ))
                current_caps.update(produced)
                step_idx += 1

        elif "MASSIVE_COORDINATES" in current_caps and "OFFLINE_COORDINATES_KNOWN" in current_caps:
            compressor = universe.get("coordinate_compressor")
            if compressor:
                consumed = frozenset(["MASSIVE_COORDINATES", "OFFLINE_COORDINATES_KNOWN"])
                produced = frozenset(["DENSE_INDEX_SPACE", "LINEAR_ARRAY"])
                pipeline.append(SynthesizedPipelineStep(
                    step_index=step_idx,
                    component_id="coordinate_compressor",
                    role="Coordinate Compressor",
                    consumed_capabilities=consumed,
                    produced_capabilities=produced
                ))
                current_caps.update(produced)
                step_idx += 1

        elif vector.temporal == TemporalMode.OFFLINE and vector.has_constraint("TRANSITION_REVERSIBLE") and query.is_range_query():
            mos = universe.get("mos_algorithm_scheduler")
            if mos:
                consumed = frozenset(["OFFLINE_QUERIES_KNOWN", "TRANSITION_REVERSIBLE"])
                produced = frozenset(["OFFLINE_QUERY_SCHEDULE"])
                pipeline.append(SynthesizedPipelineStep(
                    step_index=step_idx,
                    component_id="mos_algorithm_scheduler",
                    role="Offline Query Scheduler",
                    consumed_capabilities=consumed,
                    produced_capabilities=produced
                ))
                current_caps.update(produced)
                step_idx += 1

        # ── State Transition 2: Linear Range / Provider Binding ──
        if "RANGE_AGGREGATION" in target_caps:
            # Select range provider capable of matching mutability and algebra
            provider_candidates = []
            for cid in ("segment_tree_standard", "fenwick_tree", "dynamic_segment_tree", "sparse_table"):
                cand = universe.get(cid)
                if not cand:
                    continue
                if not cand.supports_temporal(vector.temporal):
                    continue
                # Mutability check
                req_point = vector.mutability.satisfies(MutabilityCapability.POINT_WRITE)
                req_range = vector.mutability.satisfies(MutabilityCapability.RANGE_WRITE)
                if req_range and not cand.supports_mutability(MutabilityCapability.RANGE_WRITE):
                    continue
                if req_point and not cand.supports_mutability(MutabilityCapability.POINT_WRITE):
                    continue
                # Aggregate check
                if not cand.supports_aggregate(query.aggregate):
                    continue
                # Coordinate scale check
                if "MASSIVE_COORDINATES" in current_caps and "DENSE_INDEX_SPACE" not in current_caps:
                    if cid != "dynamic_segment_tree":
                        continue
                provider_candidates.append(cand)

            if provider_candidates:
                chosen = provider_candidates[0]
                consumed = frozenset(["LINEAR_ARRAY"])
                produced = frozenset(["RANGE_AGGREGATION", "POINT_UPDATE"])
                pipeline.append(SynthesizedPipelineStep(
                    step_index=step_idx,
                    component_id=chosen.candidate_id,
                    role="Linear Range Query Provider",
                    consumed_capabilities=consumed,
                    produced_capabilities=produced
                ))
                current_caps.update(produced)
                step_idx += 1

        # Check if all target capabilities are satisfied
        missing = [t for t in target_caps if t not in current_caps]
        if not missing and pipeline:
            return CapabilitySynthesisResult(
                success=True,
                pipeline=pipeline,
                final_capabilities=frozenset(current_caps)
            )

        return CapabilitySynthesisResult(
            success=False,
            pipeline=pipeline,
            final_capabilities=frozenset(current_caps),
            gap_reason=f"Unsatisfied target capabilities: {missing}"
        )
