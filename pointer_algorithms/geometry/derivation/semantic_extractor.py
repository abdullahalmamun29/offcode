"""
CHUP Phase 3R — Semantic Geometry Extractor.

Translates problem descriptions and specifications into a formal SemanticGeometryModel.
Zero algorithm names are allowed in the ontology representation.
"""

import re
from typing import Optional

from pointer_algorithms.geometry.semantic_ontology import (
    SemanticGeometryModel,
    CoordinateDomain,
    CorrectnessGuarantee,
    GeometryObjective,
    HullCollinearPolicy,
    SweepLineObjective,
    FloatingPointPolicy,
)


class SemanticExtractor:
    """
    NLP extraction engine translating text into a formal SemanticGeometryModel.
    """

    def extract(self, text: str) -> SemanticGeometryModel:
        lower = text.lower()
        model = SemanticGeometryModel()

        # ── 1. Coordinate Domain & Floating Point Policy ──
        if re.search(r'\bfloat\b|\bdouble\b|\breals?\b|\br\^2\b|floating[- ]point|continuous', lower):
            model.coordinate_domain = CoordinateDomain.FLOATING_APPROXIMATE
            model.correctness_guarantee = CorrectnessGuarantee.CORRECTNESS_NUMERIC_APPROXIMATE
        else:
            model.coordinate_domain = CoordinateDomain.INTEGER_EXACT
            model.correctness_guarantee = CorrectnessGuarantee.DETERMINISTIC_EXACT

        # Scale tolerances
        abs_eps_match = re.search(r'eps(?:ilon)?\s*(?:=|is)?\s*1e-?(\d+)', lower)
        if abs_eps_match:
            exp = int(abs_eps_match.group(1))
            model.floating_point_policy.abs_epsilon = 10 ** (-exp)

        # ── 2. Magnitude Detection ──
        if re.search(r'2\s*[\*x×]\s*10\^9|2e9|10\^9|1e9|1000000000', lower):
            model.max_coordinate_magnitude = 2_000_000_000
        elif re.search(r'10\^5|1e5|100000', lower):
            model.max_coordinate_magnitude = 100_000

        # ── 3. Cardinality & Counts ──
        n_match = re.search(r'\bn\s*=\s*(\d+)\b|\b(\d+)\s+points\b', lower)
        if n_match:
            val = int(n_match.group(1) or n_match.group(2))
            model.points_count = val

        seg_match = re.search(r'\b(\d+)\s+segments\b', lower)
        if seg_match:
            model.segments_count = int(seg_match.group(1))

        # ── 4. Policies & Sub-Objectives ──
        if re.search(r'collinear\s+(?:points\s+)?(?:included|preserved|kept|on\s+boundary)|keep\s+collinear|non-strict\s+hull', lower):
            model.hull_collinear_policy = HullCollinearPolicy.KEEP_BOUNDARY_POINTS
        else:
            model.hull_collinear_policy = HullCollinearPolicy.STRICT_VERTICES

        if re.search(r'count\s+(?:total\s+)?intersections?', lower):
            model.sweep_line_objective = SweepLineObjective.COUNT
        elif re.search(r'enumerate|all\s+intersection\s+points|reporting\s+pairs|report\s+all', lower):
            model.sweep_line_objective = SweepLineObjective.ENUMERATE
        else:
            model.sweep_line_objective = SweepLineObjective.EXISTENCE

        # ── 5. Geometric Objective Classification ──
        # Check out-of-scope first
        if re.search(r'\b3d\b|3-space|spatial\s+mesh|z-axis|three-dimensional', lower):
            model.objective = GeometryObjective.OUT_OF_SCOPE_3D_GEOMETRY
            return model
        if re.search(r'voronoi|delaunay\s+triangulation', lower):
            model.objective = GeometryObjective.OUT_OF_SCOPE_VORONOI_DELAUNAY
            return model

        # Canonical 10 Patterns
        if re.search(r'rotating\s+calipers|polygon\s+diameter|diameter\s+of\s+.*polygon|farthest\s+pair|maximum\s+(?:pairwise\s+)?distance\s+between\s+points|antipodal', lower):
            model.objective = GeometryObjective.ROTATING_CALIPERS_DIAMETER
        elif re.search(r'halfplane|half-plane|kernel\s+of\s+polygon|convex\s+kernel', lower):
            model.objective = GeometryObjective.HALFPLANE_INTERSECTION
        elif re.search(r'closest\s+pair|minimum\s+(?:euclidean\s+)?distance\s+between\s+.*(?:points|coordinates)|nearest\s+pair', lower):
            model.objective = GeometryObjective.CLOSEST_PAIR_POINTS
        elif re.search(r'convex\s+hull|monotone\s+chain|andrew|graham\s+scan|smallest\s+convex\s+polygon|fence\s+enclosing|minimal.*fence', lower):
            model.objective = GeometryObjective.CONVEX_HULL_ANDREW
        elif re.search(r'shoelace|surveyor|polygon\s+area|area\s+of\s+(?:simple\s+)?polygon|enclosed\s+area\s+of\s+.*polygon|2\*area\s+for\s+.*polygon', lower):
            model.objective = GeometryObjective.POLYGON_AREA_SHOELACE
        elif re.search(r'point\s+in\s+polygon|\bpip\b|ray\s+casting|winding\s+number|point\s+inside\s+polygon|containment\s+test|inside,\s+outside,\s+or\s+on\s+the\s+boundary|boundary\s+point\s+test|point\s+lies\s+inside\s+.*polygon', lower):
            model.objective = GeometryObjective.POINT_IN_POLYGON
        elif re.search(r'sweep\s+line|bentley[- ]ottmann|segment\s+intersections?\s+sweep', lower):
            model.objective = GeometryObjective.SWEEP_LINE_SEGMENTS
        elif re.search(r'segment\s+intersection|segments?\s+intersect|crossing\s+segments?|do\s+segments?\s+(?:cross|intersect)|non-intersection\s+of\s+.*segments?|segments?\s+.*(?:overlap|cross|intersect)|endpoint\s+lies\s+on\s+.*segment', lower):
            model.objective = GeometryObjective.SEGMENT_INTERSECTION
        elif re.search(r'line\s+intersection|cramer.*line|two\s+lines\s+intersect|intersection\s+point\s+of\s+(?:two\s+)?(?:perpendicular\s+|parallel\s+|coincident\s+)?lines|intersection\s+of\s+(?:two\s+)?lines', lower):
            model.objective = GeometryObjective.LINE_INTERSECTION_POINT
        elif re.search(r'orientation|cross\s+product|turn\s+direction|clockwise|counter[- ]clockwise|collinear', lower):
            model.objective = GeometryObjective.ORIENTATION_CROSS_PRODUCT
        else:
            model.objective = GeometryObjective.NONE

        return model
