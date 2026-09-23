"""
CHUP Phase 6 — Surface Narrative Independence Evaluation Suite.

Evaluates 20 distinct real-world narrative skins (cows, solar panels, traffic,
telecommunications, warehousing, financial, space telemetry, mining, forestry,
railways, reservoirs, kingdoms, supercomputing, astronomy, genomics, libraries,
bakeries, maritime shipping, power grids, and hospital logistics) wrapping the
identical underlying mathematical range sum problem.

Authoritative Acceptance Invariant:
All 20 narrative variations must produce:
1. Identical QuerySpec (target, aggregate operation, output type)
2. Identical MutabilitySet (READ_ONLY)
3. Identical TemporalMode (ONLINE)
4. Identical SymbolicBudget (N=100000, Q=100000)
5. Identical Phase 5 terminal state (SATISFIABLE_SINGLE_CANDIDATE or SATISFIABLE_COMPOSED_PLAN)
6. Identical Phase 5 verified plan digest
"""

import unittest
from pointer_algorithms.deep_understanding.deep_understanding_facade import DeepProblemUnderstandingFacade
from pointer_algorithms.multi_constraint.multi_constraint_model import OutcomeState


class TestPhase6SurfaceIndependence(unittest.TestCase):

    def setUp(self):
        self.facade = DeepProblemUnderstandingFacade()

    def test_20_narrative_skins_convergence(self):
        narrative_skins = [
            # 1. Cows
            "Farmer John has n=100000 cows in a row, each producing a_i milk. Answer q=100000 queries for range sum of milk in immutable stalls [l, r].",
            # 2. Solar Panels
            "A solar array has n=100000 panels producing a_i watts. Answer q=100000 queries for range sum of power in immutable spans [l, r].",
            # 3. Traffic
            "A highway has n=100000 checkpoints recording a_i vehicles. Answer q=100000 queries for range sum of traffic in immutable segments [l, r].",
            # 4. Telecommunications
            "A fiber network has n=100000 nodes transmitting a_i gigabytes. Answer q=100000 queries for range sum of data in immutable spans [l, r].",
            # 5. Warehousing
            "A distribution warehouse has n=100000 bins holding a_i boxes. Answer q=100000 queries for range sum of inventory in immutable aisles [l, r].",
            # 6. Financial
            "A trading desk monitors n=100000 minutes yielding a_i profit. Answer q=100000 queries for range sum of returns in immutable periods [l, r].",
            # 7. Space Probe
            "A satellite records n=100000 sensor pulses with a_i voltage. Answer q=100000 queries for range sum in immutable telemetry windows [l, r].",
            # 8. Mining
            "A conveyor belt carries n=100000 batches of a_i tons of ore. Answer q=100000 queries for range sum in immutable runs [l, r].",
            # 9. Forestry
            "A national park manages n=100000 plots with a_i cedar trees. Answer q=100000 queries for range sum in immutable zones [l, r].",
            # 10. Railway
            "A rail line has n=100000 stations boarding a_i commuters. Answer q=100000 queries for range sum in immutable sectors [l, r].",
            # 11. Water Reservoir
            "An irrigation aqueduct has n=100000 valves releasing a_i liters. Answer q=100000 queries for range sum in immutable channels [l, r].",
            # 12. Medieval Kingdom
            "A medieval king surveys n=100000 towns paying a_i gold coins. Answer q=100000 queries for range sum in immutable fiefdoms [l, r].",
            # 13. Supercomputing
            "A compute cluster has n=100000 nodes drawing a_i watts. Answer q=100000 queries for range sum in immutable racks [l, r].",
            # 14. Astronomy
            "A telescope scans n=100000 pixels detecting a_i photons. Answer q=100000 queries for range sum in immutable coordinates [l, r].",
            # 15. Genomics
            "A DNA strand has n=100000 base pairs with a_i expression score. Answer q=100000 queries for range sum in immutable regions [l, r].",
            # 16. Library
            "An ancient library has n=100000 shelves shelving a_i manuscripts. Answer q=100000 queries for range sum in immutable corridors [l, r].",
            # 17. Bakery
            "A bakery line produces n=100000 trays with a_i pastries. Answer q=100000 queries for range sum in immutable shifts [l, r].",
            # 18. Maritime Shipping
            "A shipping lane has n=100000 beacons logging a_i tons. Answer q=100000 queries for range sum in immutable reaches [l, r].",
            # 19. Power Grid
            "An electric grid has n=100000 pylons carrying a_i amperes. Answer q=100000 queries for range sum in immutable lines [l, r].",
            # 20. Hospital Logistics
            "A medical centre has n=100000 lockers storing a_i vaccines. Answer q=100000 queries for range sum in immutable wards [l, r]."
        ]

        reference_result = None

        for idx, narrative in enumerate(narrative_skins, start=1):
            spec = {
                "text": narrative,
                "n": 100_000,
                "q": 100_000,
                "operation": "SUM",
                "target": "LINEAR_RANGE",
                "immutable": True
            }
            res = self.facade.process(spec)

            self.assertEqual(res["status"], "success", f"Narrative #{idx} failed to process successfully.")
            self.assertIn(
                res["outcome_state"],
                (OutcomeState.SATISFIABLE_SINGLE_CANDIDATE, OutcomeState.SATISFIABLE_COMPOSED_PLAN),
                f"Narrative #{idx} failed satisfiability."
            )
            self.assertIsNotNone(res["verified_plan"], f"Narrative #{idx} missing verified plan.")

            plan = res["verified_plan"]
            budget = res["complexity_envelope"].to_symbolic_budget()
            canonical_facts = sorted([
                (f.name, f.value, f.tier.name, f.proof_status.name)
                for f in res["phase6_facts"].eligible_facts()
            ])
            derivation_rules = sorted([
                node.derivation_rule
                for node in res["provenance_graph"].nodes.values()
                if node.derivation_rule != "RULE_DIRECT_OBSERVATION"
            ])

            if reference_result is None:
                reference_result = {
                    "outcome_state": res["outcome_state"],
                    "selected_components": plan.selected_components,
                    "pipeline_length": len(plan.synthesized_pipeline),
                    "first_step_component": plan.synthesized_pipeline[0].component_id if plan.synthesized_pipeline else None,
                    "asymptotic_class": res["complexity_envelope"].target_asymptotic_class,
                    "max_ops": res["complexity_envelope"].max_estimated_operations,
                    "objective": res["semantic_objective"],
                    "state_topology": res["state_topology"],
                    "budget_n": budget.N,
                    "budget_q": budget.Q,
                    "budget_time_ms": budget.time_limit_ms,
                    "budget_mem_mb": budget.memory_limit_mb,
                    "budget_ops_sec": budget.ops_per_second,
                    "canonical_facts": canonical_facts,
                    "derivation_rules": derivation_rules
                }
            else:
                # Require complete mathematical and semantic artifact convergence across all 20 narrative skins
                self.assertEqual(
                    res["outcome_state"],
                    reference_result["outcome_state"],
                    f"Narrative #{idx} outcome state diverged from reference."
                )
                self.assertEqual(
                    plan.selected_components,
                    reference_result["selected_components"],
                    f"Narrative #{idx} selected components diverged from reference."
                )
                self.assertEqual(
                    len(plan.synthesized_pipeline),
                    reference_result["pipeline_length"],
                    f"Narrative #{idx} pipeline step count diverged."
                )
                if plan.synthesized_pipeline:
                    self.assertEqual(
                        plan.synthesized_pipeline[0].component_id,
                        reference_result["first_step_component"],
                        f"Narrative #{idx} selected component diverged."
                    )
                self.assertEqual(
                    res["complexity_envelope"].target_asymptotic_class,
                    reference_result["asymptotic_class"],
                    f"Narrative #{idx} asymptotic envelope diverged."
                )
                self.assertEqual(
                    res["semantic_objective"],
                    reference_result["objective"],
                    f"Narrative #{idx} semantic objective diverged."
                )
                self.assertEqual(
                    res["state_topology"],
                    reference_result["state_topology"],
                    f"Narrative #{idx} state topology diverged."
                )
                # Symbolic budget exact convergence
                self.assertEqual(budget.N, reference_result["budget_n"], f"Narrative #{idx} budget N diverged.")
                self.assertEqual(budget.Q, reference_result["budget_q"], f"Narrative #{idx} budget Q diverged.")
                self.assertEqual(budget.time_limit_ms, reference_result["budget_time_ms"], f"Narrative #{idx} budget time diverged.")
                self.assertEqual(budget.memory_limit_mb, reference_result["budget_mem_mb"], f"Narrative #{idx} budget memory diverged.")
                self.assertEqual(budget.ops_per_second, reference_result["budget_ops_sec"], f"Narrative #{idx} budget ops/sec diverged.")
                # Canonical semantic facts exact convergence
                self.assertEqual(
                    canonical_facts,
                    reference_result["canonical_facts"],
                    f"Narrative #{idx} canonical semantic facts diverged from reference."
                )
                # Applied derivation rules convergence
                self.assertEqual(
                    derivation_rules,
                    reference_result["derivation_rules"],
                    f"Narrative #{idx} derivation rules diverged."
                )


if __name__ == "__main__":
    unittest.main()
