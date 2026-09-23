"""
Semantic Adapter for Architecture V2.

Transforms natural language problem text into Evidence objects with provenance,
hypotheses, and confirmed semantic facts.
Populates the canonical ProblemModel and triggers the DerivationEngine.

STRICT INVARIANT:
Lexical tokens NEVER directly select an algorithm.
No "target sum" → Knapsack.
No "xor" → Trie.
No "nearest" → BFS.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from architecture_v2.semantic_model import (
    Evidence, EvidenceStatus, SemanticScope,
    Fact, FactStatus,
    Hypothesis, HypothesisStatus,
    SelectionKind, SelectionModel,
    ObjectiveKind, ObjectiveModel,
    ConstraintDomain, InputSizeAggregateConstraint,
    ConstraintModel,
    RequiredOperation,
    RelationKind, OperatorKind, RelationModel,
    StructuralProperty,
    ProblemModel
)
from architecture_v2.derivation_engine import DerivationEngine


class SemanticAdapter:
    """
    Translates raw problem text into a canonical ProblemModel without algorithm bias.
    """

    @staticmethod
    def parse_bound_val(val_str: str) -> int:
        raw = val_str.replace(" ", "").replace(",", "").rstrip(".").lower()
        if "e" in raw:
            parts = raw.split("e")
            try:
                return int(float(parts[0]) * (10 ** int(parts[1])))
            except Exception:
                pass
        if "*10^" in raw:
            parts = raw.split("*10^")
            try:
                return int(float(parts[0])) * (10 ** int(parts[1]))
            except Exception:
                pass
        elif "*10" in raw:
            parts = raw.split("*10")
            try:
                exp = int(parts[1]) if parts[1] else 1
                return int(float(parts[0])) * (10 ** exp)
            except Exception:
                pass
        elif "10^" in raw:
            try:
                return 10 ** int(raw.split("10^")[1])
            except Exception:
                pass
        try:
            return int(float(raw))
        except Exception:
            return int(re.sub(r"[^\d]", "", raw) or 0)

    @classmethod
    def parse(cls, problem_text: str, constraints_override: Optional[Dict[str, Any]] = None) -> ProblemModel:
        model = ProblemModel(raw_text=problem_text)

        # Defensive Unicode & MathJax/KaTeX artifact normalization:
        cleaned_text = problem_text.replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-')
        cleaned_text = cleaned_text.replace('≤', '<=').replace('≥', '>=').replace('\u200b', '').replace('⋅', '*')
        cleaned_text = re.sub(r'\b([a-zA-Z])\1\b', r'\1', cleaned_text)
        cleaned_text = re.sub(r'([a-zA-Z0-9]+(?:\s*[-+*/]\s*[a-zA-Z0-9]+)+)\1', r'\1', cleaned_text)
        cleaned_lines = []
        for l in cleaned_text.split('\n'):
            lt = l.strip()
            if len(lt) >= 6 and len(lt) % 2 == 0 and ('<=' in lt or '>=' in lt or '=' in lt):
                mid = len(lt) // 2
                if lt[:mid] == lt[mid:]:
                    cleaned_lines.append(lt[:mid])
                    continue
            cleaned_lines.append(l)
        cleaned_text = '\n'.join(cleaned_lines)

        lower = cleaned_text.lower()

        # ── 0A. Input-Size Aggregate Meta-Constraint Extraction & Scope Isolation ──
        # Identifies problem-wide or multi-test-case resource bounds (e.g. "sum of n over all test cases <= 2e5")
        # and partitions them strictly into ConstraintDomain.INPUT_SIZE.
        # These constraints MUST NEVER participate in problem data relations, range aggregates, or target sums.
        meta_constraint_patterns = [
            # 1. Multi-test-case input-size aggregate (e.g. "sum of n over all test cases <= 2e5", "total queries in all test cases <= ...")
            re.compile(
                r'(?:it\s+is\s+guaranteed\s+that\s+)?(?:the\s+)?(?:total\s+)?(?:sum|number|length|count)\s+of\s+'
                r'([a-z0-9_\|\s]+?)\s+(?:over|across|for|in)\s+all\s+(?:the\s+)?test\s*cases\b'
                r'[^.\n;]*?'
                r'(?:does\s+not\s+exceed|will\s+not\s+exceed|may\s+not\s+exceed|cannot\s+exceed|should\s+not\s+exceed|'
                r'is\s+at\s+most|is\s+less\s+than\s+or\s+equal\s+to|is\s+smaller\s+than|is\s+strictly\s+less\s+than|'
                r'not\s+greater\s+than|not\s+more\s+than|<=|≤|<|=)\s*'
                r'([0-9\s*^eE\.,]+)',
                re.IGNORECASE
            ),
            re.compile(
                r'(?:over|across|for|in)\s+all\s+(?:the\s+)?test\s*cases[,\s]+(?:it\s+is\s+guaranteed\s+that\s+)?(?:the\s+)?(?:total\s+)?(?:sum|number|length|count)\s+of\s+'
                r'([a-z0-9_\|\s]+?)'
                r'[^.\n;]*?'
                r'(?:does\s+not\s+exceed|will\s+not\s+exceed|may\s+not\s+exceed|cannot\s+exceed|should\s+not\s+exceed|'
                r'is\s+at\s+most|is\s+less\s+than\s+or\s+equal\s+to|is\s+smaller\s+than|is\s+strictly\s+less\s+than|'
                r'not\s+greater\s+than|not\s+more\s+than|<=|≤|<|=)\s*'
                r'([0-9\s*^eE\.,]+)',
                re.IGNORECASE
            ),
            re.compile(
                r'(?:it\s+is\s+guaranteed\s+that\s+)?(?:the\s+)?(?:total\s+)?(?:sum|number|length|count)\s+of\s+'
                r'([a-z0-9_\|\s]+?)'
                r'[^.\n;]*?'
                r'(?:does\s+not\s+exceed|will\s+not\s+exceed|may\s+not\s+exceed|cannot\s+exceed|should\s+not\s+exceed|'
                r'is\s+at\s+most|is\s+less\s+than\s+or\s+equal\s+to|is\s+smaller\s+than|is\s+strictly\s+less\s+than|'
                r'not\s+greater\s+than|not\s+more\s+than|<=|≤|<|=)\s*'
                r'([0-9\s*^eE\.,]+)'
                r'[^.\n;]*?(?:over|across|for|in)\s+all\s+(?:the\s+)?test\s*cases\b',
                re.IGNORECASE
            ),
            re.compile(
                r'(?:sum|total)\s+([a-z0-9_]+)\s*(?:<=|≤|<|=)\s*([0-9\s*^eE\.,]+)[^.\n;]*?(?:over|across|for|in)\s+all\s+(?:the\s+)?test\s*cases\b',
                re.IGNORECASE
            ),
            # 2. Global input-size aggregates (e.g. "the total number of vertices does not exceed 2*10^5", "total queries <= 2e5")
            re.compile(
                r'(?:it\s+is\s+guaranteed\s+that\s+)?(?:the\s+)?total\s+(?:number|count|sum|length)\s+of\s+'
                r'([a-z0-9_\|\s]+?)'
                r'[^.\n;]*?'
                r'(?:does\s+not\s+exceed|will\s+not\s+exceed|may\s+not\s+exceed|cannot\s+exceed|should\s+not\s+exceed|'
                r'is\s+at\s+most|is\s+less\s+than\s+or\s+equal\s+to|is\s+smaller\s+than|is\s+strictly\s+less\s+than|'
                r'not\s+greater\s+than|not\s+more\s+than|<=|≤|<|=)\s*'
                r'([0-9\s*^eE\.,]+)',
                re.IGNORECASE
            ),
            re.compile(
                r'(?:the\s+)?total\s+(vertices|vertexes|nodes|edges|queries|operations|strings|test\s*cases|characters)\s*'
                r'[^.\n;]*?'
                r'(?:does\s+not\s+exceed|will\s+not\s+exceed|may\s+not\s+exceed|cannot\s+exceed|should\s+not\s+exceed|'
                r'is\s+at\s+most|is\s+less\s+than\s+or\s+equal\s+to|is\s+smaller\s+than|is\s+strictly\s+less\s+than|'
                r'not\s+greater\s+than|not\s+more\s+than|<=|≤|<|=)\s*'
                r'([0-9\s*^eE\.,]+)',
                re.IGNORECASE
            )
        ]

        found_meta = True
        while found_meta:
            found_meta = False
            for pat in meta_constraint_patterns:
                m = pat.search(lower)
                if m:
                    var_raw = m.group(1).strip()
                    clean_var = re.sub(r'^(?:the|total)\s+', '', var_raw).strip('| ')
                    bound_raw = m.group(2).strip()
                    bound_val = cls.parse_bound_val(bound_raw)

                    is_test_case_scoped = bool(re.search(r'\ball\s+(?:the\s+)?test\s*cases\b', m.group(0), re.IGNORECASE))
                    input_size_vars = {"n", "m", "q", "k", "v", "e", "t", "vertices", "vertexes", "nodes", "edges", "queries", "strings", "operations", "characters", "test cases", "testcases", "steps", "elements"}
                    is_known_input_var = clean_var in input_size_vars or any(v in clean_var.split() for v in input_size_vars)

                    if not (is_test_case_scoped or is_known_input_var):
                        # Not an input size variable; do not consume
                        continue

                    scope = "ALL_TEST_CASES" if is_test_case_scoped else "GLOBAL"

                    input_size_agg = InputSizeAggregateConstraint(
                        domain=ConstraintDomain.INPUT_SIZE,
                        aggregate="SUM",
                        variable=clean_var,
                        scope=scope,
                        bound=bound_val,
                        raw=m.group(0)
                    )
                    model.constraints.input_size_aggregates.append(input_size_agg)

                    ev_meta = Evidence(
                        fact=f"constraint_input_size_aggregate_{clean_var}",
                        source=cls._find_matching_snippet(problem_text, m.group(0)),
                        confidence=0.99,
                        status=EvidenceStatus.EXPLICIT,
                        scope=SemanticScope.CONSTRAINT
                    )
                    model.evidence.append(ev_meta)
                    model.add_fact(Fact(
                        f"constraint.input_size.{clean_var}",
                        bound_val,
                        FactStatus.KNOWN,
                        ev_meta.source,
                        scope=SemanticScope.CONSTRAINT
                    ))
                    if is_test_case_scoped:
                        model.add_fact(Fact(
                            f"constraint.input_size.sum_{clean_var}_all_test_cases",
                            bound_val,
                            FactStatus.KNOWN,
                            ev_meta.source,
                            scope=SemanticScope.CONSTRAINT
                        ))

                    # Blank out the matched span with spaces so downstream stages never conflate
                    # this input-size aggregate with problem data relations.
                    span_len = m.end() - m.start()
                    lower = lower[:m.start()] + (" " * span_len) + lower[m.end():]
                    found_meta = True
                    break

        # ── 0. Input Schema Extraction & Scope Isolation ──
        schema_pattern = r'(?:(?:the\s+)?(?:first|second|third|next|each|only)?\s*line\s+(?:contains|has)|input\s+(?:format|consists\s+of)|the\s+input\s+contains)\s+([^.\n]+)'
        input_schema_match = re.search(schema_pattern, lower)
        task_text = lower
        if input_schema_match:
            schema_snippet = input_schema_match.group(0)
            param_match = re.search(r'\b(?:two|2)\s+integers\b|\b(?:three|3)\s+integers\b|\b(\d+)\s+integers\b', schema_snippet)
            if param_match:
                matched_str = param_match.group(0)
                if "two" in matched_str or matched_str.startswith("2"):
                    p_count = 2
                elif "three" in matched_str or matched_str.startswith("3"):
                    p_count = 3
                else:
                    p_count = int(param_match.group(1) or 2)
                ev_schema = Evidence(
                    fact="input_parameter_count",
                    source=cls._find_matching_snippet(problem_text, r'\b(?:two|three|2|3|\d+)\s+integers\b'),
                    confidence=0.98,
                    status=EvidenceStatus.EXPLICIT,
                    scope=SemanticScope.INPUT_SCHEMA
                )
                model.evidence.append(ev_schema)
                model.add_fact(Fact("input.parameter_count", p_count, FactStatus.KNOWN, ev_schema.source, scope=SemanticScope.INPUT_SCHEMA))
            # Remove schema snippet from task_text so schema parameters don't pollute task selection cardinality
            task_text = lower.replace(schema_snippet, " ")

        # ── 0b. Multiple Input Collections & One-to-One Matching Extraction ──
        has_two_arrays = False
        n_array_match = re.search(r'\b(?:contains|has)?\s*n\s+integers\b', lower)
        m_array_match = re.search(r'\b(?:contains|has)?\s*m\s+integers\b', lower)
        two_array_phrase = re.search(r'\b(?:two\s+(?:arrays|sequences|collections|lists)|given\s+(?:an?\s+)?(?:array|sequence)\s+.*?\s+and\s+(?:an?\s+)?(?:array|sequence))\b', lower)
        n_and_m_entities = re.search(r'\b(?:there\s+are\s+)?n\s+([a-z]+)\s+and\s+m\s+([a-z]+)\b', lower)

        if (n_array_match and m_array_match) or two_array_phrase or (n_and_m_entities and (n_array_match or m_array_match or "array" in lower or "integers" in lower)):
            has_two_arrays = True
            model.collections = ["collection_A", "collection_B"]
            ev_colls = Evidence(
                fact="two_distinct_collections",
                source=cls._find_matching_snippet(problem_text, r'n\s+integers.*?m\s+integers|two\s+arrays|n\s+\w+\s+and\s+m\s+\w+'),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.INPUT_SCHEMA
            )
            model.evidence.append(ev_colls)
            model.add_fact(Fact("collection.count", 2, FactStatus.KNOWN, ev_colls.source, scope=SemanticScope.INPUT_SCHEMA))
            model.add_fact(Fact("collection.two_distinct_collections", True, FactStatus.KNOWN, ev_colls.source, scope=SemanticScope.INPUT_SCHEMA))
            model.structural_properties.add(StructuralProperty.TWO_SEQUENCE_MATCHING)

        matching_1to1_match = re.search(
            r'\b(?:one-to-one|one\s+to\s+one|bipartite\s+matching)\b|'
            r'\b(?:at\s+most\s+once|cannot\s+be\s+(?:used|reused|assigned|given|matched|placed)\s+(?:more\s+than\s+once|again)|without\s+reuse)\b|'
            r'\beach\s+\w+\s+(?:can|may)?\s*(?:get|have|receive|take|hold|fit\s+in|carry|contain|be\s+given|be\s+assigned|be\s+placed\s+in|be\s+matched\s+to)\s+(?:at\s+most\s+one|an?|one)\s+\w+\b|'
            r'\bdistribute\s+(?:the\s+)?\w+\s+so\s+that\s+(?:as\s+many\s+\w+\s+as\s+possible|each\s+\w+)\s+(?:will|can)?\s*(?:get|receive|have)\s+an?\s+\w+\b',
            lower
        )
        if matching_1to1_match and has_two_arrays:
            ev_1to1 = Evidence(
                fact="matching_one_to_one",
                source=cls._find_matching_snippet(problem_text, matching_1to1_match.group(0)),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.CONSTRAINT
            )
            model.evidence.append(ev_1to1)
            model.add_fact(Fact("matching.one_to_one", True, FactStatus.KNOWN, ev_1to1.source, scope=SemanticScope.CONSTRAINT))
            model.structural_properties.add(StructuralProperty.ONE_TO_ONE_MATCHING)
        else:
            model.collections = ["collection_A"]
            model.structural_properties.add(StructuralProperty.SINGLE_COLLECTION)
            model.add_fact(Fact("collection.single", True, FactStatus.KNOWN, "input_schema", scope=SemanticScope.INPUT_SCHEMA))
            model.structural_properties.add(StructuralProperty.SORTABLE)
            model.add_fact(Fact("collection.sortable", True, FactStatus.KNOWN, "input_schema", scope=SemanticScope.INPUT_SCHEMA))

        # ── 1. Cardinality & Selection Extraction (Task Requirement Scope) ──
        # Check for fixed cardinality in task_text:
        k_found = None
        source_regex = None

        noun_pattern = r'(?:elements|numbers|values|items|integers|cards|entries)'

        if re.search(rf'\b(?:exactly\s+)?(?:four|4)\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}\b|\bquadruplet\b', task_text):
            k_found = 4
            source_regex = rf'(?:exactly\s+)?(?:four|4)\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}|quadruplet'
        elif re.search(rf'\b(?:exactly\s+)?(?:three|3)\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}\b|\btriplet\b', task_text):
            k_found = 3
            source_regex = rf'(?:exactly\s+)?(?:three|3)\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}|triplet'
        else:
            two_match = None
            for m in re.finditer(rf'\b(?:exactly\s+)?(?:two|2)\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}\b|'
                                rf'\bfind\s+(?:a\s+)?pair\b|\bpair\s+of\s+(?:distinct\s+)?(?:array\s+)?{noun_pattern}\b', task_text):
                start = m.start()
                prefix = task_text[max(0, start - 25):start].lower()
                suffix = task_text[m.end():min(len(task_text), m.end() + 25)].lower()
                if re.search(r'\b(?:at\s+most|up\s+to|one\s+or|maximum\s+(?:of\s+)?|no\s+more\s+than|any|every|each|between\s+any)\s*$', prefix):
                    continue
                if re.search(r'^\s*(?:differ|have\s+difference|must|cannot|should)\b', suffix):
                    continue
                if re.search(r'\b(?:select|choose|pick|find)\s+(?:a\s+|the\s+)?(?:largest\s+|maximum\s+)?(?:subset|subsequence)\b', task_text.lower()):
                    continue
                two_match = m
                break
            if two_match is not None:
                k_found = 2
                source_regex = two_match.group(0)

        if k_found is not None:
            ev = Evidence(
                fact=f"selection_cardinality_{k_found}",
                source=cls._find_matching_snippet(problem_text, source_regex),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.TASK_REQUIREMENT
            )
            model.evidence.append(ev)
            model.selection = SelectionModel(SelectionKind.FIXED_CARDINALITY, k_found)
            model.add_fact(Fact("selection.cardinality", k_found, FactStatus.KNOWN, ev.source, scope=SemanticScope.TASK_REQUIREMENT))
            model.add_fact(Fact("selection.kind", SelectionKind.FIXED_CARDINALITY, FactStatus.KNOWN, ev.source, scope=SemanticScope.TASK_REQUIREMENT))
        elif re.search(r'\b(?:contiguous\s+(?:subarray|subarrays|range|ranges|segment|segments|subsegment|subsegments|block|blocks|window|windows)|subarray|subarrays|window\s+of\s+size\s+[a-z0-9_]+|in\s+each\s+window)\b', lower):
            ev = Evidence(
                fact="selection_contiguous_segment",
                source=cls._find_matching_snippet(problem_text, r'\b(?:contiguous\s+(?:subarray|subarrays|range|ranges|segment|segments|subsegment|subsegments|block|blocks|window|windows)|subarray|subarrays|window\s+of\s+size\s+[a-z0-9_]+|in\s+each\s+window)\b'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.selection = SelectionModel(SelectionKind.CONTIGUOUS_SEGMENT)
            model.add_fact(Fact("selection.kind", SelectionKind.CONTIGUOUS_SEGMENT, FactStatus.KNOWN, ev.source))
            model.structural_properties.add(StructuralProperty.CONTIGUOUS_SELECTION)
        elif re.search(r'\b(?:subsets?|subsequences?|teams?|selections?)\b|\b(?:as\s+many\b.*?\bas\s+possible|items?\s+you\s+can\s+pick)\b|\b(?:select|choose|pick)\s+(?:a\s+)?(?:subset|team|group)\b', lower):
            ev = Evidence(
                fact="selection_arbitrary_subset",
                source=cls._find_matching_snippet(problem_text, r'subsets?|subsequences?|teams?|selections?|as\s+many|pick|choose|select'),
                confidence=0.90,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.selection = SelectionModel(SelectionKind.ARBITRARY_SUBSET)
            model.add_fact(Fact("selection.kind", SelectionKind.ARBITRARY_SUBSET, FactStatus.KNOWN, ev.source))
            model.structural_properties.add(StructuralProperty.ARBITRARY_SUBSET)
        elif re.search(
            r'\b(?:all|every)\s+(?:elements|cubes|items|children|people|packages|objects|numbers|values|entries)\b|'
            r'\beach\s+(?:element|cube|item|child|person|package|object|number|value|entry)\b|'
            r'\bfor\s+(?:each|every)\s+(?!query\b|line\b|group\b|pair\b|step\b|turn\b|test\b|case\b|testcase\b)\w+\b|'
            r'\bevery\s+(?!test\s*case\b)\w+\s+(?:must|needs?\s+to)\s+be\s+assigned\b|'
            r'\bfor\s+the\s+(?:children|people|items|packages|elements)\b',
            lower
        ):
            ev = Evidence(
                fact="selection_all_elements",
                source=cls._find_matching_snippet(problem_text, r'all|every|each'),
                confidence=0.90,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.selection = SelectionModel(SelectionKind.ALL_ELEMENTS)
            model.add_fact(Fact("selection.kind", SelectionKind.ALL_ELEMENTS, FactStatus.KNOWN, ev.source))

        # Check for group / partition cardinality constraints (e.g. at most two per group)
        group_card_match = re.search(
            r'\b(?:at\s+most|up\s+to|one\s+or|maximum\s+(?:of\s+)?|no\s+more\s+than)\s+(?:two|2)\b|'
            r'\b(?:two|2)\s+(?:elements|items|people|children|packages|objects)?\s*(?:at\s+most|maximum)\b|'
            r'\beach\s+\w+\s+(?:may|can)?\s*(?:have|hold|contain|carry|fit|take)\s+(?:one\s+or\s+two|at\s+most\s+two|up\s+to\s+two|(?:at\s+most|up\s+to)\s+2)\b',
            task_text
        )
        if group_card_match:
            ev_gc = Evidence(
                fact="group_max_cardinality_2",
                source=cls._find_matching_snippet(problem_text, r'(?:at\s+most|up\s+to|one\s+or|maximum\s+(?:of\s+)?|no\s+more\s+than)\s+(?:two|2)'),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.CONSTRAINT
            )
            model.evidence.append(ev_gc)
            model.constraints.max_group_cardinality = 2
            model.add_fact(Fact("group.max_cardinality", 2, FactStatus.KNOWN, ev_gc.source, scope=SemanticScope.CONSTRAINT))

        distinct_expr = (
            r'at\s+distinct\s+positions|distinct\s+(?:indices|indexes|positions)|'
            r'different\s+(?:positions|indices|indexes)|choose\s+different\s+elements|'
            r'no\s+position\s+may\s+be\s+used\s+more\s+than\s+once|'
            r'no\s+two\s+(?:elements\s+)?(?:from|at)\s+the\s+same\s+position|pairwise\s+distinct|'
            rf'positions\s+of\s+(?:two|three|four|\d+)\s+{noun_pattern}'
        )
        if re.search(rf'\b(?:{distinct_expr})\b', lower):
            ev = Evidence(
                fact="selection_distinct_positions",
                source=cls._find_matching_snippet(problem_text, distinct_expr),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.TASK_REQUIREMENT
            )
            model.evidence.append(ev)
            model.selection.distinct_positions = True
            model.add_fact(Fact("selection.distinct_positions", True, FactStatus.KNOWN, ev.source, scope=SemanticScope.TASK_REQUIREMENT))
        elif re.search(rf'\b(?:two|three|four|\d+)\s+distinct\s+{noun_pattern}\b', lower):
            ev = Evidence(
                fact="selection_distinct_positions",
                source=cls._find_matching_snippet(problem_text, rf'(?:two|three|four|\d+)\s+distinct\s+{noun_pattern}'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.TASK_REQUIREMENT
            )
            model.evidence.append(ev)
            model.selection.distinct_positions = True
            model.add_fact(Fact("selection.distinct_positions", True, FactStatus.KNOWN, ev.source, scope=SemanticScope.TASK_REQUIREMENT))

        # ── 2. Relation & Operator Extraction ──
        # Isolate task and I/O specifications from constraints block to prevent constraint bounds (e.g. 1 <= n <= 5000, 10^9)
        # from polluting the task relation or operator model.
        constraints_split = re.split(r'\b(?:constraints|constraint)\b', lower, maxsplit=1)
        task_rel_text = constraints_split[0]
        # Mask parenthesized variable bounds e.g. (1 <= ai <= 10^9) or (1 <= t <= 10^4)
        task_rel_text = re.sub(r'\([^)]*?(?:<=|≤|>=|≥|<|>)[^)]*?\)', ' ', task_rel_text)
        # Mask standalone variable bounds e.g. 1 <= ai <= 10^9 or 1 <= n <= 2*10^5
        task_rel_text = re.sub(r'\b\d+\s*(?:<=|≤|<)\s*[a-z0-9_,\s]+\s*(?:<=|≤|<)\s*[0-9\s*^eE\.,]+', ' ', task_rel_text)

        # SUM relation & operator (distinguish exact sum vs at-most sum)
        is_at_most_sum = bool(re.search(r'\b(?:at\s+most|no\s+more\s+than|less\s+than\s+or\s+equal\s+to|<=|≤)\s+(?:total\s+)?sum\b|\b(?:sum|total)\s+(?:is\s+)?(?:at\s+most|no\s+more\s+than|less\s+than\s+or\s+equal\s+to|<=|≤)', task_rel_text))
        sum_target_match = re.search(r'\b(?:having|with|target|equals?|is|=|to)\s+sum\s+([a-z0-9_]+)\b|\b(?:sum|total)\s+(?:of|is|=|equals?)\s+([a-z0-9_]+)\b|\bwhose\s+sum\s+is\s+([a-z0-9_]+)\b', task_rel_text)
        sum_expr = (
            r'(?:sum|total)\s*(?:equals?|equal\s+to|is|=|adds?\s+up\s+to|summing\s+to|to)\b|'
            r'(?:adds?|adding)\s+up\s+to\b|\bwhose\s+(?:values\s+)?(?:sum|total)\b|'
            r'\bwith\s+sum\b|\btarget\s+sum\b|\bcombined\s+(?:value|sum)\b|\bhaving\s+sum\b|\bexact\s+sum\b'
        )
        if re.search(rf'\b(?:{sum_expr})', task_rel_text):
            target_token = None
            if sum_target_match:
                target_token = sum_target_match.group(1) or sum_target_match.group(2) or sum_target_match.group(3)

            rel_kind = RelationKind.LESS_EQUAL if is_at_most_sum else RelationKind.SUM

            ev = Evidence(
                fact="relation_sum",
                source=cls._find_matching_snippet(problem_text, sum_expr),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(rel_kind, operator=OperatorKind.SUM, target=target_token))
            if not is_at_most_sum:
                model.relations.append(RelationModel(RelationKind.EQUALITY, operator=OperatorKind.SUM, target=target_token))
                model.relations.append(RelationModel(RelationKind.SUM))
            else:
                model.relations.append(RelationModel(RelationKind.LESS_EQUAL))
            model.add_fact(Fact("relation.kind", rel_kind, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("operator.kind", OperatorKind.SUM, FactStatus.KNOWN, ev.source))
            if not is_at_most_sum:
                model.add_fact(Fact("relation.exact_range_sum", True, FactStatus.KNOWN, ev.source))
            if target_token:
                model.add_fact(Fact("relation.target_token", target_token, FactStatus.KNOWN, ev.source))

        # DIFFERENCE relation
        if re.search(r'\bdifference\s*(?:equals?|equal\s+to|is|=|of)\b', task_rel_text):
            ev = Evidence(
                fact="relation_difference",
                source=cls._find_matching_snippet(problem_text, r'difference\s*(?:equals?|equal\s+to|is|=|of)'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(RelationKind.DIFFERENCE))
            model.add_fact(Fact("relation.kind", RelationKind.DIFFERENCE, FactStatus.KNOWN, ev.source))

        # XOR operator (guard against mathematical exponent notation such as 10^9 or 2^31)
        if re.search(r'\bxor\b|bitwise\s+xor|(?<![\d\w])\^(?![\d\w])', task_rel_text):
            ev = Evidence(
                fact="operator_xor",
                source=cls._find_matching_snippet(problem_text, r'\bxor\b|bitwise\s+xor|(?<![\d\w])\^(?![\d\w])'),
                confidence=1.0,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(RelationKind.EQUALITY, operator=OperatorKind.XOR))
            model.add_fact(Fact("operator.kind", OperatorKind.XOR, FactStatus.KNOWN, ev.source))

        # Interval / Tolerance compatibility relation:
        # e.g., "|a - b| <= k", "between x - k and x + k", "difference is at most k",
        # "within k of", "maximum allowed difference is k"
        tol_match = re.search(
            r'(?:(?:abs\(|\|)\s*([a-z0-9_]+)\s*-\s*([a-z0-9_]+)\s*(?:\)|\|)\s*(?:<=|≤)\s*([a-z0-9_]+))|'
            r'(?:between\s+([a-z0-9_]+)\s*-\s*([a-z0-9_]+)\s+and\s+\4\s*\+\s*\5)|'
            r'(?:\[\s*([a-z0-9_]+)\s*-\s*([a-z0-9_]+)\s*,\s*\6\s*\+\s*\7\s*\])|'
            r'(?:(?:maximum\s+allowed\s+)?difference\s*(?:between\s+[^,\.]*?\s*)?(?:is|=|:)?\s*(?:at\s+most|<=|≤|less\s+than\s+or\s+equal\s+to|no\s+more\s+than)?\s*([a-z0-9_]+))|'
            r'(?:within\s+(?:tolerance\s+)?([a-z0-9_]+)\s+of)',
            task_rel_text
        )
        if tol_match and has_two_arrays:
            k_token = tol_match.group(3) or tol_match.group(5) or tol_match.group(7) or tol_match.group(8) or tol_match.group(9) or "k"
            ev_tol = Evidence(
                fact="relation_interval_tolerance",
                source=cls._find_matching_snippet(problem_text, tol_match.group(0)),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.TASK_REQUIREMENT
            )
            model.evidence.append(ev_tol)
            model.relations.append(RelationModel(RelationKind.INTERVAL_TOLERANCE, tolerance=k_token))
            model.add_fact(Fact("relation.kind", RelationKind.INTERVAL_TOLERANCE, FactStatus.KNOWN, ev_tol.source))
            model.add_fact(Fact("relation.interval_tolerance", True, FactStatus.KNOWN, ev_tol.source))
            model.add_fact(Fact("relation.tolerance_token", k_token, FactStatus.KNOWN, ev_tol.source))
            model.structural_properties.add(StructuralProperty.MONOTONE_COMPATIBILITY)

        # Pairwise absolute difference constraint:
        # e.g., "the programming skill of each pair of students should differ by no more than 5"
        # "every pair of selected numbers differs by at most k"
        # "the absolute difference between any two chosen values must not exceed k"
        # "for every pair x,y in the selected set: |x-y| <= k"
        # "all selected values lie within a range of width k"
        # Pairwise absolute difference constraint:
        pairwise_diff_match = re.search(
            r'(?:(?:each|every|any)\s+[^.\n;]*?\s+differs?\s+(?:from\s+[^.\n;]*?)?\s+by\s+(?:no\s+more\s+than|at\s+most|not\s+exceeding|<=|≤)\s*([a-z0-9_]+))|'
            r'(?:(?:each|every|any|all)\s+(?:pairs?|two\s+\w+)\s+(?:of\s+[^.\n;]*?)?(?:should|must|to)?\s*(?:differ|have\s+difference)\s+(?:by\s+)?(?:no\s+more\s+than|at\s+most|not\s+exceeding|<=|≤)\s*([a-z0-9_]+))|'
            r'(?:(?:every|each|any)\s+pair\s+(?:differs|differ|has\s+(?:absolute\s+)?difference)\s*(?:by\s+)?(?:at\s+most|no\s+more\s+than|<=|≤)\s*([a-z0-9_]+))|'
            r'(?:(?:absolute\s+)?difference\s+between\s+(?:any\s+two|each\s+pair\s+of|every\s+pair\s+of|the\s+maximum\s+and\s+minimum\b)[^.\n;]*?(?:must\s+not|may\s+not|does\s+not|cannot|should\s+not|is\s+)?\s*(?:exceed|be\s+(?:greater|more)\s+than|<=|≤|at\s+most)\s*([a-z0-9_]+))|'
            r'(?:for\s+(?:every|each|all)\s+pairs?[^|]*?(?:\|[a-z0-9_]+(?:\s*-\s*|\s*−\s*)[a-z0-9_]+\||abs\([a-z0-9_]+-[a-z0-9_]+\))\s*(?:<=|≤)\s*([a-z0-9_]+))|'
            r'(?:(?:max\s*-\s*min|max\(s\)\s*-\s*min\(s\))\s*(?:<=|≤)\s*([a-z0-9_]+))|'
            r'(?:all\s+selected\s+(?:values|elements|numbers)\s+lie\s+within\s+a\s+range\s+of\s+width\s+([a-z0-9_]+))|'
            r'(?:\bdiameter\s*(?:of|is|=|:)?\s*(?:at\s+most|<=|≤|no\s+more\s+than)?\s*([a-z0-9_]+)\b)',
            task_rel_text,
            re.IGNORECASE
        )
        if pairwise_diff_match and not has_two_arrays:
            k_token = (
                pairwise_diff_match.group(1) or pairwise_diff_match.group(2) or
                pairwise_diff_match.group(3) or pairwise_diff_match.group(4) or
                pairwise_diff_match.group(5) or pairwise_diff_match.group(6) or
                pairwise_diff_match.group(7) or pairwise_diff_match.group(8) or "k"
            ).strip()

            k_val = None
            try:
                k_val = int(k_token)
            except ValueError:
                pass

            is_k_in_input = bool(re.search(r'\b(?:two|2)\s+integers\b|\b[a-z0-9_]+\s+and\s+' + re.escape(k_token) + r'\b', lower))
            tol_type = "INPUT_VARIABLE" if is_k_in_input else "CONSTANT"

            ev_pairwise = Evidence(
                fact="relation_pairwise_absolute_difference",
                source=cls._find_matching_snippet(problem_text, pairwise_diff_match.group(0)),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.CONSTRAINT
            )
            model.evidence.append(ev_pairwise)
            model.relations.append(RelationModel(
                kind=RelationKind.PAIRWISE_ABSOLUTE_DIFFERENCE,
                quantifier="FOR_ALL_PAIRS",
                tolerance=k_token
            ))
            model.add_fact(Fact("relation.pairwise_absolute_difference", k_val if k_val is not None else k_token, FactStatus.KNOWN, ev_pairwise.source, scope=SemanticScope.CONSTRAINT))
            model.add_fact(Fact("relation.pairwise_quantifier", "FOR_ALL_PAIRS", FactStatus.KNOWN, ev_pairwise.source, scope=SemanticScope.CONSTRAINT))
            model.add_fact(Fact("relation.tolerance_type", tol_type, FactStatus.KNOWN, ev_pairwise.source, scope=SemanticScope.CONSTRAINT))
            if k_val is not None:
                model.constraints.k = k_val
                model.constraints.match_tolerance = k_val
                model.add_fact(Fact("constraint.k", k_val, FactStatus.KNOWN, ev_pairwise.source, scope=SemanticScope.CONSTRAINT))

            model.structural_properties.add(StructuralProperty.PAIRWISE_RELATION)

            if model.selection.kind == SelectionKind.UNKNOWN:
                model.selection = SelectionModel(SelectionKind.ARBITRARY_SUBSET)
                model.add_fact(Fact("selection.kind", SelectionKind.ARBITRARY_SUBSET, FactStatus.KNOWN, ev_pairwise.source))
                model.structural_properties.add(StructuralProperty.ARBITRARY_SUBSET)

        # Inequalities in task description: <= x (LESS_EQUAL) or >= x (GREATER_EQUAL)
        cap_match = re.search(
            r'(?:total\s+)?(?:weight|cost|load|sum|size)?\s*(?:in\s+a\s+\w+\s+|per\s+\w+\s+|in\s+each\s+\w+\s+)?'
            r'(?:may\s+not|cannot|can\s+not|does\s+not|must\s+not)?\s*(?:exceed|be\s+greater\s+than)\s+(?!of\s+[^,\.]*?\btest\s*cases\b)([a-z0-9_]+)\b|'
            r'\b(?:the\s+)?(?:sum|total|weight)\s+(?:of\s+(?!.*?\btest\s*cases\b)[^,\.]*?\s+)?(?:is\s+)?(?:at\s+most|less\s+than\s+or\s+equal\s+to|not\s+greater\s+than|<=)\s+([a-z0-9_]+)\b|'
            r'\bcapacity\s*(?:of|is|=|:)?\s*([a-z0-9_]+)\b|'
            r'\bweight\s+limit\s*(?:of|is|=|:)?\s*([a-z0-9_]+)\b|'
            r'\bmaximum\s+(?:allowed\s+)?(?:weight|capacity|load)\s*(?:of|is|=|:)?\s*([a-z0-9_]+)\b',
            task_rel_text
        )
        if cap_match:
            target_token = cap_match.group(1) or cap_match.group(2) or cap_match.group(3) or cap_match.group(4)
            ev = Evidence(
                fact="constraint_group_capacity",
                source=cls._find_matching_snippet(problem_text, cap_match.group(0)),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.CONSTRAINT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(RelationKind.LESS_EQUAL, operator=OperatorKind.SUM))
            model.add_fact(Fact("relation.kind", RelationKind.LESS_EQUAL, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("operator.kind", OperatorKind.SUM, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("constraint.group_capacity", target_token, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("group.capacity_constrained", True, FactStatus.KNOWN, ev.source))
        elif re.search(r'(?:\b(?:not\s+exceeding|at\s+most|less\s+than\s+or\s+equal\s+to|not\s+greater\s+than|may\s+not\s+exceed|cannot\s+exceed)\b|<=)', task_rel_text):
            ev = Evidence(
                fact="relation_less_equal",
                source=cls._find_matching_snippet(problem_text, r'not\s+exceeding|at\s+most|less\s+than\s+or\s+equal\s+to|not\s+greater\s+than|may\s+not\s+exceed|cannot\s+exceed|<='),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(RelationKind.LESS_EQUAL))
            model.add_fact(Fact("relation.kind", RelationKind.LESS_EQUAL, FactStatus.KNOWN, ev.source))
        elif re.search(r'(?:\b(?:at\s+least|greater\s+than\s+or\s+equal\s+to|not\s+less\s+than|on\s+top\s+of\s+(?:an?\s+)?existing\s+(?:tower|pile)|on\s+(?:an?\s+)?existing\s+tower)\b|>=)', task_rel_text):
            ev = Evidence(
                fact="relation_greater_equal",
                source=cls._find_matching_snippet(problem_text, r'at\s+least|greater\s+than\s+or\s+equal\s+to|not\s+less\s+than|on\s+top\s+of\s+(?:an?\s+)?existing\s+(?:tower|pile)|on\s+(?:an?\s+)?existing\s+tower|>='),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.relations.append(RelationModel(RelationKind.GREATER_EQUAL))
            model.add_fact(Fact("relation.kind", RelationKind.GREATER_EQUAL, FactStatus.KNOWN, ev.source))

        # ── 3. Objective Extraction ──
        # Isolate relational phrases ("at most k", "no more than k", "at least k", "no less than k")
        # so isolated words "most" or "least" never hijack the optimization objective.
        # Check specific optimization patterns:

        cardinality_max_pattern = (
            r'\b(?:maximum|largest|greatest)\s+(?:possible\s+)?(?:number\s+of\s+)?(?:students|elements|items|values|numbers|cards|entries|vertices|nodes|cardinality|subsets?|groups?|teams?|selections?|size)\b|'
            r'\b(?:maximize|maximizing)\s+(?:the\s+)?(?:number\s+of\s+)?(?:students|elements|items|values|numbers|cards|entries|vertices|nodes|cardinality|matched|matches|pairs|assignments|size)\b|'
            r'\b(?:as\s+many\b.*?\bas\s+possible|as\s+large\s+as\s+possible|largest\s+(?:possible\s+)?(?:subset|group|team|selection))\b|'
            r'\b(?:team|subset|group|selection)\s+(?:to\s+be\s+)?as\s+large\s+as\s+possible\b|'
            r'\b(?:maximum|largest)\s+(?:possible\s+)?(?:cardinality|size)\b|'
            r'\b(?:subset|selection|team|group)\s+of\s+maximum\s+(?:cardinality|size)\b'
        )

        count_pattern = (
            r'\b(?:count\s+the\s+number\s+of|number\s+of\s+ways|how\s+many)\b|'
            r'\b(?:calculate|compute|determine|find|print|output)\s+(?:the\s+)?(?:total\s+)?number\s+of\s+(?:subarrays|segments|ways|pairs|tuples|subsequences|blocks|occurrences)\b'
        )

        negated_min = re.search(r'\b(?:not|never|without|do\s+not|does\s+not)\s+(?:to\s+)?(?:compute|find|determine|calculate|require|select)?\s*(?:the\s+)?(?:minimize|minimum|smallest|fewest)\b', lower)
        negated_max = re.search(r'\b(?:not|never|without|do\s+not|does\s+not)\s+(?:to\s+)?(?:compute|find|determine|calculate|require|select)?\s*(?:the\s+)?(?:maximize|maximum|largest|greatest)\b', lower)

        cardinality_match = re.search(cardinality_max_pattern, lower)
        count_match = re.search(count_pattern, lower)

        if cardinality_match and not count_match:
            target_prop = "general"
            if model.has_fact("matching.one_to_one") or "matched" in lower or "matches" in lower:
                target_prop = "matches"
                ev = Evidence(
                    fact=f"objective_maximize_{target_prop}",
                    source=cls._find_matching_snippet(problem_text, cardinality_match.group(0)),
                    confidence=0.95,
                    status=EvidenceStatus.EXPLICIT
                )
                model.evidence.append(ev)
                model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE, target_property=target_prop)
                model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE, FactStatus.KNOWN, ev.source))
                model.add_fact(Fact("objective.target_property", target_prop, FactStatus.KNOWN, ev.source))
                model.add_fact(Fact("objective.maximize_matches", True, FactStatus.KNOWN, ev.source))
                model.structural_properties.add(StructuralProperty.MAX_CARDINALITY_MATCHING)
            else:
                target_prop = "cardinality"
                ev = Evidence(
                    fact="objective_maximize_cardinality",
                    source=cls._find_matching_snippet(problem_text, cardinality_match.group(0)),
                    confidence=0.95,
                    status=EvidenceStatus.EXPLICIT
                )
                model.evidence.append(ev)
                model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE_CARDINALITY, target_property="cardinality")
                model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE_CARDINALITY, FactStatus.KNOWN, ev.source))
                model.add_fact(Fact("objective.maximize_cardinality", True, FactStatus.KNOWN, ev.source))
                model.add_fact(Fact("objective.target_property", "cardinality", FactStatus.KNOWN, ev.source))
        elif count_match:
            ev = Evidence(
                fact="objective_count",
                source=cls._find_matching_snippet(problem_text, count_match.group(0)),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.COUNT)
            model.add_fact(Fact("objective.kind", ObjectiveKind.COUNT, FactStatus.KNOWN, ev.source))
        elif re.search(r'\b(?:maximum|maximizes?|maximizing)\s+(?:the\s+)?(?:total\s+)?sum\b', lower):
            ev = Evidence(
                fact="objective_maximize_sum",
                source=cls._find_matching_snippet(problem_text, r'maximum\s+sum|maximizes?\s+sum|maximizing\s+sum'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE_SUM, target_property="sum")
            model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE_SUM, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("objective.target_property", "sum", FactStatus.KNOWN, ev.source))
        elif re.search(r'\b(?:maximum|maximizes?|maximizing)\s+(?:the\s+)?(?:possible\s+)?(?:value|score|answer|xor|product)\b', lower):
            ev = Evidence(
                fact="objective_maximize_value",
                source=cls._find_matching_snippet(problem_text, r'maximum\s+value|maximizes?\s+value|maximizing\s+value'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE_VALUE, target_property="value")
            model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE_VALUE, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("objective.target_property", "value", FactStatus.KNOWN, ev.source))
        elif bool(re.search(r'\b(?:minimize|minimum|smallest|fewest)\b', lower)) and not bool(negated_min):
            target_prop = "general"
            if re.search(r'\b(?:groups?|gondolas?|boats?|containers?|vehicles?|trips?|bins?|partitions?|boxes?|teams?)\b', lower):
                target_prop = "groups"
            elif "towers" in lower or "tower" in lower:
                target_prop = "towers"
            elif "pile" in lower or "subsequence" in lower or "partition" in lower:
                target_prop = "partitions"
            elif "cost" in lower:
                target_prop = "cost"
            elif "length" in lower or "size" in lower:
                target_prop = "length"
            ev = Evidence(
                fact=f"objective_minimize_{target_prop}",
                source=cls._find_matching_snippet(problem_text, r'minimize|minimum|smallest|fewest'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.MINIMIZE, target_property=target_prop)
            model.add_fact(Fact("objective.kind", ObjectiveKind.MINIMIZE, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("objective.target_property", target_prop, FactStatus.KNOWN, ev.source))
        elif bool(re.search(r'\b(?:maximize|maximum|largest|greatest)\b', lower)) and not bool(negated_max):
            target_prop = "general"
            if re.search(r'\b(?:maximum|max|longest)\s+length\b|\blength\s+of\s+the\s+longest\b', lower):
                target_prop = "length"
            elif "price" in lower:
                target_prop = "price"
            elif "area" in lower:
                target_prop = "area"
            ev = Evidence(
                fact=f"objective_maximize_{target_prop}",
                source=cls._find_matching_snippet(problem_text, r'maximize|maximum|largest|greatest'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE, target_property=target_prop)
            model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("objective.target_property", target_prop, FactStatus.KNOWN, ev.source))
        elif re.search(r'\b(?:customers?\s+want\s+tickets?|tickets?\s+with\s+price\s+at\s+most|willing\s+to\s+pay\s+at\s+most)\b', lower):
            ev = Evidence(
                fact="objective_maximize_price",
                source=cls._find_matching_snippet(problem_text, r'customers?\s+want\s+tickets?|tickets?\s+with\s+price\s+at\s+most|willing\s+to\s+pay\s+at\s+most'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.MAXIMIZE, target_property="price")
            model.add_fact(Fact("objective.kind", ObjectiveKind.MAXIMIZE, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("objective.target_property", "price", FactStatus.KNOWN, ev.source))
        elif re.search(r'\b(?:count|number\s+of\s+ways|how\s+many)\b', lower):
            ev = Evidence(
                fact="objective_count",
                source=cls._find_matching_snippet(problem_text, r'count|number\s+of\s+ways|how\s+many'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.COUNT)
            model.add_fact(Fact("objective.kind", ObjectiveKind.COUNT, FactStatus.KNOWN, ev.source))
        elif re.search(r'\b(?:determine\s+whether|check\s+(?:whether|if)|is\s+there\s+(?:a\b|an\b|any\b)|does\s+there\s+exist)\b', lower):
            ev = Evidence(
                fact="objective_decide",
                source=cls._find_matching_snippet(problem_text, r'determine\s+whether|check\s+(?:whether|if)|is\s+there|does\s+there\s+exist'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.DECIDE)
            model.add_fact(Fact("objective.kind", ObjectiveKind.DECIDE, FactStatus.KNOWN, ev.source))
        elif re.search(r'\bfind\b|\blocat(?:e|ing)\b|\bsearch\b', lower):
            ev = Evidence(
                fact="objective_find_any",
                source=cls._find_matching_snippet(problem_text, r'find|locate|search'),
                confidence=0.90,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.objective = ObjectiveModel(ObjectiveKind.FIND_ANY)
            model.add_fact(Fact("objective.kind", ObjectiveKind.FIND_ANY, FactStatus.KNOWN, ev.source))

        # ── 4. Output Specification ──
        if re.search(r'\b(?:original\s+)?(?:indices|indexes|positions)\b|\b1-based\s+indices\b', lower):
            ev = Evidence(
                fact="output_original_indices",
                source=cls._find_matching_snippet(problem_text, r'(?:original\s+)?(?:indices|indexes|positions)|1-based\s+indices'),
                confidence=0.98,
                status=EvidenceStatus.EXPLICIT,
                scope=SemanticScope.OUTPUT_SPEC
            )
            model.evidence.append(ev)
            model.output_spec = {"type": "ORIGINAL_INDICES", "base": 1, "cardinality": model.selection.cardinality}
            model.add_fact(Fact("output.type", "ORIGINAL_INDICES", FactStatus.KNOWN, ev.source, scope=SemanticScope.OUTPUT_SPEC))
        elif re.search(r'\b(?:output|return|print)\s+(?:the\s+)?(?:values?|elements?)\b', lower):
            model.output_spec = {"type": "VALUES"}
            model.add_fact(Fact("output.type", "VALUES", FactStatus.KNOWN, "text"))
        elif re.search(r'\b(?:yes\s+or\s+no|true\s+or\s+false|boolean|exists?)\b', lower):
            model.output_spec = {"type": "BOOLEAN"}
            model.add_fact(Fact("output.type", "BOOLEAN", FactStatus.KNOWN, "text"))
        elif re.search(r'\b(?:print|output|return)\s+(?:one|an?)\s+integer\b|\bnumber\s+of\b', lower):
            model.output_spec = {"type": "COUNT"}
            model.add_fact(Fact("output.type", "COUNT", FactStatus.KNOWN, "text", scope=SemanticScope.OUTPUT_SPEC))

        # ── 5. Dynamic / Mutability Operations & Sequential Context ──
        if re.search(r'\bremov(?:e|ed|ing)|delet(?:e|ed|ing)|eras(?:e|ed|ing)|purchas(?:e|ed|ing)|bought|cannot\s+be\s+(?:purchased|used|bought)\s+again\b', lower):
            ev = Evidence(
                fact="operation_delete",
                source=cls._find_matching_snippet(problem_text, r'remov(?:e|ed|ing)|delet(?:e|ed|ing)|eras(?:e|ed|ing)|purchas(?:e|ed|ing)|bought|cannot\s+be\s+(?:purchased|used|bought)\s+again'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("action.delete", True, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("collection.dynamic", True, FactStatus.KNOWN, ev.source))

        if re.search(r'\binsert(?:ion)?\b|\bappend\b|\b(?<!in\s)add(?:ing|ed)?\b(?!\s+(?:to\b|up\b))', lower):
            ev = Evidence(
                fact="operation_insert",
                source=cls._find_matching_snippet(problem_text, r'\binsert(?:ion)?\b|\bappend\b|\b(?<!in\s)add(?:ing|ed)?\b'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("action.insert", True, FactStatus.KNOWN, ev.source))
            model.add_fact(Fact("collection.dynamic", True, FactStatus.KNOWN, ev.source))

        if re.search(r'\b(?:one\s+by\s+one|one\s+after\s+another|sequentially|in\s+(?:the\s+)?given\s+order)\b', lower):
            ev = Evidence(
                fact="processing_sequential",
                source=cls._find_matching_snippet(problem_text, r'one\s+by\s+one|one\s+after\s+another|sequentially|in\s+(?:the\s+)?given\s+order'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("stream.sequential", True, FactStatus.KNOWN, ev.source))

        if re.search(r'\b(?:each\s+customer|for\s+each\s+query|q\s+queries|repeatedly|stream\s+of|arrive(?:s|d)?)\b', lower):
            ev = Evidence(
                fact="query_repeated",
                source=cls._find_matching_snippet(problem_text, r'each\s+customer|for\s+each\s+query|q\s+queries|repeatedly|stream\s+of|arrive(?:s|d)?'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("query.repeated", True, FactStatus.KNOWN, ev.source))

        if re.search(r'\bdynamic\b', lower):
            ev = Evidence(
                fact="collection_dynamic",
                source=cls._find_matching_snippet(problem_text, r'\bdynamic\b'),
                confidence=0.95,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("collection.dynamic", True, FactStatus.KNOWN, ev.source))

        # ── 6. Disambiguation: "Nearest" ──
        if "nearest" in lower or "closest" in lower:
            ev = Evidence(
                fact="relation_nearest",
                source=cls._find_matching_snippet(problem_text, r'nearest|closest'),
                confidence=0.90,
                status=EvidenceStatus.EXPLICIT
            )
            model.evidence.append(ev)
            model.add_fact(Fact("relation.nearest", True, FactStatus.KNOWN, ev.source))

            # Check if context defines predecessor/successor or absolute distance
            if "graph" in lower or "node" in lower or "edge" in lower:
                hyp = Hypothesis(
                    name="nearest_semantics",
                    value="graph_shortest_path",
                    status=HypothesisStatus.CONFIRMED,
                    evidence=[Evidence("nearest_graph", "context", 0.90, EvidenceStatus.INFERRED)]
                )
            elif model.has_fact("relation.kind") and model.get_fact("relation.kind").value in (RelationKind.LESS_EQUAL, RelationKind.GREATER_EQUAL):
                hyp = Hypothesis(
                    name="nearest_semantics",
                    value="bounded_predecessor_or_successor",
                    status=HypothesisStatus.CONFIRMED,
                    evidence=[Evidence("nearest_bounded", "context", 0.95, EvidenceStatus.INFERRED)]
                )
            else:
                hyp = Hypothesis(
                    name="nearest_semantics",
                    value="ambiguous_distance_vs_order",
                    status=HypothesisStatus.AMBIGUOUS,
                    evidence=[Evidence("nearest_ambiguous", "text", 0.50, EvidenceStatus.INFERRED)]
                )
                model.uncertainty["nearest_semantics"] = "Cannot determine whether nearest implies absolute numeric difference or predecessor ordering."
            model.hypotheses["nearest"] = hyp

        # ── 7. Extract Constraints ──
        if constraints_override:
            for k, v in constraints_override.items():
                if hasattr(model.constraints, k):
                    setattr(model.constraints, k, v)
        else:
            # Parse simple constraint bounds from text e.g. "n <= 200000", "n <= 2*10^5", "x <= 10^9"
            target_match = re.search(r'(?:target|sum|x)\s*=\s*(\d+)|(?:target|sum|x)\s*(?:is|equals?)\s*(\d+)', lower)
            if target_match:
                val = int(target_match.group(1) or target_match.group(2))
                model.constraints.target_value = val
                model.add_fact(Fact("constraint.target_value", val, FactStatus.KNOWN, target_match.group(0)))

            bound_pattern = r'(?:(?:\d+|[a-z0-9_]+)\s*(?:<=|≤|<)\s*)?([a-z_][a-z0-9_]*(?:\s*,\s*[a-z_][a-z0-9_]*)*)\s*(?:<=|≤|=)\s*(\d+(?:\s*\*\s*10\^?\d+|\s*10\^?\d+)?)'
            for cm in re.finditer(bound_pattern, lower):
                vars_str = cm.group(1)
                val_str = cm.group(2)
                val = cls.parse_bound_val(val_str)
                var_names = [v.strip() for v in vars_str.split(',')]
                for vname in var_names:
                    if vname == 'n':
                        model.constraints.n = val
                        model.add_fact(Fact("constraint.n", val, FactStatus.KNOWN, cm.group(0)))
                        model.add_fact(Fact("constraint.n_raw", cm.group(0), FactStatus.KNOWN, cm.group(0)))
                    elif vname == 'm':
                        model.constraints.m = val
                        model.add_fact(Fact("constraint.m", val, FactStatus.KNOWN, cm.group(0)))
                    elif vname == 'k':
                        model.constraints.k = val
                        model.constraints.match_tolerance = val
                        model.add_fact(Fact("constraint.k", val, FactStatus.KNOWN, cm.group(0)))
                    elif vname in ('x', 'capacity') and any(term in lower for term in ('weight', 'capacity', 'load', 'gondola')):
                        model.constraints.group_capacity = val
                        model.add_fact(Fact("constraint.group_capacity_val", val, FactStatus.KNOWN, cm.group(0)))

            # Positivity: numeric constraint bounds establish a_i >= 1 or a_i > 0
            # e.g., 1 <= x, ai <= 10^9 or 1 <= ai <= 10^9 or ai >= 1 or ai > 0
            pos_bound_match = re.search(r'\b1\s*(?:<=|≤|<)\s*(?:[a-z0-9_,\s]+)?\b(?:ai|a_i|x_i|p_i|arr\[i\]|elements?|values?)\b|\b(?:ai|a_i|x_i|p_i|arr\[i\])\s*(?:>=|≥|>)\s*1\b|\b(?:ai|a_i|x_i|p_i|arr\[i\])\s*>\s*0\b', lower)
            pos_text_match = re.search(r'\b(?:strictly\s+)?positive\s+(?:integers|numbers|values|elements)\b|\ball\s+(?:elements|values|numbers|integers)\s+are\s+positive\b', lower)
            neg_or_zero_match = re.search(r'\b0\s*(?:<=|≤|<)\s*(?:[a-z0-9_,\s]+)?\b(?:ai|a_i|x_i|p_i)\b|\bmay\s+contain\s+negative\b|\bnegative\s+integers\b|\bnegative\s+values\b|\bnegative\s+numbers\b|(?<!\w)-\s*\d+(?:\^\d+)?\s*(?:<=|≤|<)\s*(?:[a-z0-9_,\s]+)?\b(?:ai|a_i|x_i|p_i)\b', lower)

            if (pos_bound_match or pos_text_match) and not neg_or_zero_match:
                model.constraints.strictly_positive = True
                ev_pos = Evidence(
                    fact="domain_strictly_positive",
                    source=cls._find_matching_snippet(problem_text, (pos_bound_match.group(0) if pos_bound_match else pos_text_match.group(0))),
                    confidence=0.98,
                    status=EvidenceStatus.EXPLICIT,
                    scope=SemanticScope.CONSTRAINT
                )
                model.evidence.append(ev_pos)
                model.add_fact(Fact("domain.strictly_positive", True, FactStatus.KNOWN, ev_pos.source, scope=SemanticScope.CONSTRAINT))
                model.add_fact(Fact("domain.value_positivity", "POSITIVE", FactStatus.KNOWN, ev_pos.source, scope=SemanticScope.CONSTRAINT))

        # ── 8. Run Derivation Engine ──
        engine = DerivationEngine()
        model = engine.run(model)

        # ── 9. Validate Semantic Model ──
        validation = model.validate()
        if not validation.is_valid:
            for err in validation.errors:
                model.uncertainty[f"validation_error_{len(model.uncertainty)}"] = err

        return model

    @staticmethod
    def _find_matching_snippet(text: str, regex: str) -> str:
        m = re.search(regex, text, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 20)
            end = min(len(text), m.end() + 20)
            return text[start:end].strip()
        return text[:50]
