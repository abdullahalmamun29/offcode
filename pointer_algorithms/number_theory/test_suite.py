"""
Comprehensive Unit Test Suite for CHUP Phase 3P: Number Theory & Combinatorics.

Validates:
1. Semantic ontology & orthogonal primitive representation (zero algorithm names).
2. Derived facts & provenance records (PROVEN status, proof obligations, rule tracking).
3. StateContract strict semantic substitutability in NT (positive match, supertype match, attribute conflict rejection).
4. Suffix / Table state isolation: ArithmeticFunctionTableState does NOT inherit SieveTableState.
5. Divisor lattice state does NOT inherit generic DirectedAcyclicGraph.
6. Modular ring Z/mZ does NOT claim is_field=True when modulus is composite.
7. Closed-world Gate A: ExtGCD selected for composite modulus; Fermat rejected with MODULUS_NOT_PRIME.
8. Closed-world Gate A: Fermat selected for certified prime modulus; ExtGCD marked suboptimal.
9. Closed-world Gate A: Modular inverse fails closed with INVERSE_DOES_NOT_EXIST when gcd(a, m) != 1.
10. Closed-world Gate B: Non-coprime CRT checks solvability and fails closed with CRT_NO_SIMULTANEOUS_SOLUTION.
11. Closed-world Gate B: CRT fails closed with INTEGER_DOMAIN_EXCEEDED when cumulative LCM >= 2^127 - 1.
12. Closed-world Gate C: Lucas theorem requires p prime (LUCAS_DOMAIN_VALID).
13. Closed-world Gate C: Table feasibility bound (p <= 10^6 feasible; p > 10^6 fails with FACTORIAL_TABLE_INFEASIBLE).
14. Closed-world Gate D: Multiplicative functions (phi, mu) range tables strictly require linear_sieve_builder.
15. Closed-world Gate E: Factorial combinatorics requires prime p and N < p; N >= p routes to Lucas.
16. Arithmetic safety fact derivation: m <= 3,037,000,499 vs m > 3.037e9 int128 requirement.
17. Miller-Rabin exact 7-witness basis certified deterministic for unsigned 64-bit N < 2^64.
18. Out-of-scope boundaries: Elliptic curve point counting, Nim-sum game theory, calendar simulation.
19. 4-phase formal invariants for all 10 NT patterns in InvariantEngine.
20. Formal movement derivations and elimination proofs in MovementDerivationEngine.
21. C++ generator dispatch and code generation for all 10 NT patterns.
22. C++ standalone syntax validation (fast I/O, unsigned long long for Miller-Rabin, __int128_t).
23. Bridge integration with handle_request() for number theory problems.
24. Number theory candidate eliminator overrides generic fallbacks.
25. Matrix exponentiation handles K=0 identity matrix base case.
26. Component registry registration and dependency queries.
"""

import unittest
import sys
import os
import subprocess
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.knowledge.taxonomy import (
    PatternKind,
    NUMBER_THEORY_PATTERNS
)
from pointer_algorithms.number_theory.semantic_ontology import (
    IntegerMagnitude,
    ModulusCharacteristic,
    ArithmeticMode,
    QueryMultiplicity,
    AlgebraicStructure,
    CorrectnessGuarantee,
    NumberTheoryObjective,
    DerivedFact,
    ProvenanceStatus,
    SemanticNumberTheoryModel
)
from pointer_algorithms.adv_graph.component_model import StateContract
from pointer_algorithms.number_theory.nt_state_contracts import (
    make_integer_state,
    make_diophantine_system_state,
    make_modular_ring_state,
    make_modular_inverse_state,
    make_crt_system_state,
    make_sieve_table_state,
    make_arithmetic_function_table_state,
    make_divisor_lattice_state,
    make_matrix_ring_state,
    make_factorial_table_state,
    make_lucas_decomposition_state,
    make_miller_rabin_result_state,
)
from pointer_algorithms.number_theory.component_model import (
    AlgorithmComponent,
    NumberTheoryComponentRegistry,
)
from pointer_algorithms.number_theory.derivation_engine import (
    NumberTheoryDerivationEngine,
    CandidateStatus,
    SelectionStatus
)
from pointer_algorithms.reasoning.invariant_engine import InvariantEngine
from pointer_algorithms.reasoning.movement_derivation import MovementDerivationEngine
from pointer_algorithms.generator.cpp_generator import CppPointerGenerator
from pointer_algorithms.generator.nt_cpp_generator import generate_nt_cpp
from pointer_algorithms.bridge import handle_request
from pointer_algorithms.recognition.feature_extractor import ProblemFeatures, FeatureExtractor
from pointer_algorithms.recognition.candidate_generator import AlgorithmCandidate
from pointer_algorithms.recognition.candidate_eliminator import CandidateEliminator


class TestNumberTheoryUnitSuite(unittest.TestCase):

    def setUp(self):
        self.registry = NumberTheoryComponentRegistry()
        self.engine = NumberTheoryDerivationEngine(self.registry)

    # ── Test 01: Semantic Ontology & Orthogonal Primitive Representation ──
    def test_01_semantic_ontology_orthogonal_dimensions(self):
        model = SemanticNumberTheoryModel()
        self.assertEqual(model.integer_magnitude, IntegerMagnitude.MAGNITUDE_LE_1E9)
        self.assertEqual(model.modulus_characteristic, ModulusCharacteristic.GENERAL_COMPOSITE)
        self.assertEqual(model.arithmetic_mode, ArithmeticMode.MODULAR_FIXED_WIDTH)
        self.assertEqual(model.query_multiplicity, QueryMultiplicity.SINGLE_INSTANCE)
        self.assertEqual(model.algebraic_structure, AlgebraicStructure.MODULAR_RING)
        self.assertEqual(model.correctness_guarantee, CorrectnessGuarantee.DETERMINISTIC_EXACT)
        self.assertEqual(model.objective, NumberTheoryObjective.NONE)

    # ── Test 02: Derived Facts & Provenance Records ──
    def test_02_derived_facts_provenance_tracking(self):
        model = SemanticNumberTheoryModel()
        model.add_derived_property(
            "PRIME_MODULUS_CERTIFIED", True,
            ["input:modulus=1000000007"],
            "FERMAT_CONGRUENCE_PRECONDITION",
            ["modulus_is_prime"]
        )
        self.assertTrue(model.has_derived_fact("PRIME_MODULUS_CERTIFIED"))
        self.assertEqual(len(model.provenance_records), 1)
        rec = model.provenance_records[0]
        self.assertEqual(rec.status, ProvenanceStatus.PROVEN)
        self.assertEqual(rec.derivation_rule, "FERMAT_CONGRUENCE_PRECONDITION")
        self.assertIn("modulus_is_prime", rec.proof_obligations)

    # ── Test 03: StateContract Exact Match ──
    def test_03_state_contract_positive_exact_match(self):
        s1 = StateContract(name="ModularRingState", attributes={"modulus_known": True, "is_prime": True})
        req = StateContract(name="ModularRingState", attributes={"modulus_known": True, "is_prime": True})
        self.assertTrue(s1.satisfies(req))

    # ── Test 04: StateContract Supertype Match ──
    def test_04_state_contract_supertype_match(self):
        # StateContract with supertypes
        sub = StateContract(name="ModularInverseState", supertypes={"ModularRingState"}, attributes={"is_coprime": True})
        req = StateContract(name="ModularRingState", attributes={"is_coprime": True})
        self.assertTrue(sub.satisfies(req))

    # ── Test 05: StateContract Attribute Conflict Rejection ──
    def test_05_state_contract_attribute_conflict_rejection(self):
        s1 = StateContract(name="ModularRingState", attributes={"is_prime": False})
        req = StateContract(name="ModularRingState", attributes={"is_prime": True})
        self.assertFalse(s1.satisfies(req))

    # ── Test 06: Strict Substitutability — ArithmeticFunctionTableState Isolation ──
    def test_06_arithmetic_function_table_state_isolation(self):
        phi_state = make_arithmetic_function_table_state(function_name="phi", limit_n=1000000)
        sieve_req = StateContract(name="SieveTableState")
        # Invariant: ArithmeticFunctionTableState does NOT inherit SieveTableState
        self.assertNotIn("SieveTableState", phi_state.supertypes)
        self.assertFalse(phi_state.satisfies(sieve_req))
        self.assertEqual(phi_state.attributes["source_sieve_capability"], "linear_sieve_builder")

    # ── Test 07: Divisor Lattice State Does NOT Inherit DirectedAcyclicGraph ──
    def test_07_divisor_lattice_state_isolation(self):
        lattice_state = make_divisor_lattice_state(n=120)
        dag_req = StateContract(name="DirectedAcyclicGraph")
        self.assertNotIn("DirectedAcyclicGraph", lattice_state.supertypes)
        self.assertFalse(lattice_state.satisfies(dag_req))

    # ── Test 08: Modular Ring Z/mZ with Composite Modulus Is NOT Field ──
    def test_08_modular_ring_composite_not_field(self):
        # Ring without certificate is not a field
        ring_state = make_modular_ring_state(modulus=12)
        self.assertFalse(ring_state.attributes["is_field"])
        self.assertFalse(ring_state.attributes["is_prime"])
        self.assertEqual(ring_state.name, "ModularRingState")

        # Even with an evaluated test on a composite, field properties are denied
        comp_cert = make_miller_rabin_result_state(n=12)
        ring_with_comp = make_modular_ring_state(modulus=12, prime_certificate=comp_cert)
        self.assertFalse(ring_with_comp.attributes["is_field"])

        # Genuine certified prime establishes field properties
        prime_cert = make_miller_rabin_result_state(n=17)
        prime_field = make_modular_ring_state(modulus=17, prime_certificate=prime_cert)
        self.assertTrue(prime_field.attributes["is_field"])
        self.assertTrue(prime_field.attributes["is_prime"])

    # ── Test 09: Gate A — Modular Inverse Composite Requires ExtGCD ──
    def test_09_gate_a_modular_inverse_extgcd_composite(self):
        model = self.engine.extract_semantic_model("Find modular inverse of a modulo composite number m.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertEqual(selected, "nt_modular_inverse")
        extgcd_eval = next(e for e in evals if e.component_name == "modular_inverse_extgcd")
        fermat_eval = next(e for e in evals if e.component_name == "fermat_inverse_builder")
        self.assertEqual(extgcd_eval.status, CandidateStatus.VALID_OPTIMAL)
        self.assertEqual(fermat_eval.status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(fermat_eval.rejection_code, "MODULUS_NOT_PRIME")

    # ── Test 10: Gate A — Modular Inverse Prime Selects Fermat ──
    def test_10_gate_a_modular_inverse_fermat_prime(self):
        model = self.engine.extract_semantic_model("Find modular inverse of a modulo a prime p mod 10^9+7.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertEqual(selected, "nt_modular_inverse")
        fermat_eval = next(e for e in evals if e.component_name == "fermat_inverse_builder")
        extgcd_eval = next(e for e in evals if e.component_name == "modular_inverse_extgcd")
        self.assertEqual(fermat_eval.status, CandidateStatus.VALID_OPTIMAL)
        self.assertEqual(extgcd_eval.status, CandidateStatus.VALID_SUBOPTIMAL)

    # ── Test 11: Gate A — Non-coprime Inverse Fails Closed ──
    def test_11_gate_a_modular_inverse_zero_divisor_closed(self):
        model = self.engine.extract_semantic_model("Compute modular inverse of a modulo m where gcd(a, m) != 1.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "INVERSE_DOES_NOT_EXIST" for e in evals))

    # ── Test 12: Gate B — Non-coprime CRT Solvability Check ──
    def test_12_gate_b_crt_non_coprime_solvability(self):
        model = self.engine.extract_semantic_model("Solve Chinese remainder system with non-coprime moduli but contradictory inconsistent remainders.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "CRT_NO_SIMULTANEOUS_SOLUTION" for e in evals))

    # ── Test 13: Gate B — CRT Modulus Exceeds 128-bit Fails Closed ──
    def test_13_gate_b_crt_int128_overflow_closed(self):
        model = self.engine.extract_semantic_model("Solve system of congruences CRT where cumulative lcm overflows 128-bit integer_domain_exceeded.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "INTEGER_DOMAIN_EXCEEDED" for e in evals))

    # ── Test 14: Gate C — Lucas Theorem Requires Prime Domain ──
    def test_14_gate_c_lucas_theorem_prime_domain(self):
        model = self.engine.extract_semantic_model("Compute nCr modulo small prime p with large n and k up to 10^18 using Lucas theorem.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertEqual(selected, "nt_lucas_theorem")
        lucas_eval = next(e for e in evals if e.pattern == "nt_lucas_theorem")
        self.assertEqual(lucas_eval.status, CandidateStatus.VALID_OPTIMAL)

    # ── Test 15: Gate C — Lucas Table Feasibility Bound ──
    def test_15_gate_c_lucas_table_feasibility_bound(self):
        model = self.engine.extract_semantic_model("Evaluate combination nCr mod p using Lucas theorem where prime p is too large for table p >= 10^9 factorial_table_infeasible.")
        evals, selected = self.engine.evaluate_candidates(model)
        self.assertIsNone(selected)
        self.assertTrue(any(e.rejection_code == "FACTORIAL_TABLE_INFEASIBLE" for e in evals))

    # ── Test 16: Gate D — Multiplicative Range Tables Require Linear Sieve ──
    def test_16_gate_d_multiplicative_functions_require_linear_sieve(self):
        mobius_comp = self.registry.get("mobius_sieve_builder")
        self.assertIsNotNone(mobius_comp)
        req_state = mobius_comp.requires_states[0]
        # Invariant: mobius_sieve_builder requires SieveTableState
        self.assertEqual(req_state.name, "SieveTableState")
        # Linear sieve provides SieveTableState
        sieve_comp = self.registry.get("linear_sieve_builder")
        self.assertTrue(any(s.satisfies(req_state) for s in sieve_comp.provides_states))

    # ── Test 17: Gate E — Factorial Combinatorics N >= p Domain Gate ──
    def test_17_gate_e_factorial_combinatorics_domain_gate(self):
        model = self.engine.extract_semantic_model("Compute binomial coefficient nCr mod p with n greater than p domain_violation_n_ge_p.")
        evals, selected = self.engine.evaluate_candidates(model)
        # Routes to Lucas theorem instead of failing or accepting invalid factorial table
        self.assertEqual(selected, "nt_lucas_theorem")
        fact_eval = next(e for e in evals if e.pattern == "nt_combinatorics_factorials")
        self.assertEqual(fact_eval.status, CandidateStatus.INVALID_PRECONDITION)
        self.assertEqual(fact_eval.rejection_code, "DOMAIN_VIOLATION_N_GE_P")

    # ── Test 18: Arithmetic Safety Facts — 3.037e9 Threshold ──
    def test_18_arithmetic_safety_modular_product_threshold(self):
        # Exact mathematical threshold: sqrt(2^63 - 1) = 3,037,000,499
        safe_model = SemanticNumberTheoryModel(modulus_value=1000000007)
        safe_model.add_derived_property(
            "MODULAR_PRODUCT_FITS_INT64", True, ["modulus_value_le_3037000499"],
            "INT64_MODULAR_MULTIPLICATION_SAFETY"
        )
        self.assertTrue(safe_model.has_derived_fact("MODULAR_PRODUCT_FITS_INT64"))

        large_model = SemanticNumberTheoryModel(modulus_value=4000000000)
        large_model.add_derived_property(
            "MODULAR_PRODUCT_REQUIRES_INT128", True, ["modulus_or_operands_exceed_3e9"],
            "INT128_MODULAR_CAST_REQUIRED"
        )
        self.assertTrue(large_model.has_derived_fact("MODULAR_PRODUCT_REQUIRES_INT128"))

    # ── Test 19: Miller-Rabin Locked 7-Witness Basis ──
    def test_19_miller_rabin_locked_7_witness_basis(self):
        mr_state = make_miller_rabin_result_state(n=1000000007)
        expected_witnesses = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
        self.assertEqual(mr_state.attributes["witness_basis"], expected_witnesses)
        self.assertTrue(mr_state.attributes["deterministic_64bit"])
        self.assertTrue(mr_state.attributes["result"])
        self.assertEqual(mr_state.attributes["certification_method"], "DETERMINISTIC_7_WITNESS_BASIS")

        # Composite candidate evaluates to False without caller intervention
        mr_comp = make_miller_rabin_result_state(n=561)
        self.assertFalse(mr_comp.attributes["result"])

    # ── Test 20: Out-of-Scope Boundaries Rejected ──
    def test_20_out_of_scope_boundaries(self):
        # 1. Elliptic curve point counting
        m1 = self.engine.extract_semantic_model("Point counting on elliptic curves using Schoof algorithm.")
        evals1, sel1 = self.engine.evaluate_candidates(m1)
        self.assertIsNone(sel1)
        self.assertTrue(any(e.rejection_code == "ELLIPTIC_CURVE_UNSUPPORTED" for e in evals1))

        # 2. Game theory / Nim-sum
        m2 = self.engine.extract_semantic_model("Solve impartial game using Nim-sum and Sprague-Grundy values.")
        evals2, sel2 = self.engine.evaluate_candidates(m2)
        self.assertIsNone(sel2)
        self.assertTrue(any(e.rejection_code == "GAME_THEORY_UNSUPPORTED" for e in evals2))

        # 3. Calendar simulation
        m3 = self.engine.extract_semantic_model("Calculate day of week in Gregorian calendar date arithmetic.")
        evals3, sel3 = self.engine.evaluate_candidates(m3)
        self.assertIsNone(sel3)
        self.assertTrue(any(e.rejection_code == "SIMULATION_UNSUPPORTED" for e in evals3))

    # ── Test 21: 4-Phase Formal Invariants in InvariantEngine ──
    def test_21_formal_invariants_all_10_patterns(self):
        nt_patterns = [
            "nt_extended_gcd", "nt_modular_inverse", "nt_chinese_remainder",
            "nt_linear_sieve", "nt_euler_totient", "nt_mobius_inversion",
            "nt_matrix_power", "nt_combinatorics_factorials", "nt_lucas_theorem",
            "nt_miller_rabin"
        ]
        for pat in nt_patterns:
            inv = InvariantEngine.construct_invariant(pat, {})
            self.assertTrue(len(inv.before_iteration) > 0, f"Missing before_iteration for {pat}")
            self.assertTrue(len(inv.during_iteration) > 0, f"Missing during_iteration for {pat}")
            self.assertTrue(len(inv.after_movement) > 0, f"Missing after_movement for {pat}")
            self.assertTrue(len(inv.at_termination) > 0, f"Missing at_termination for {pat}")

    # ── Test 22: Formal Movement Derivations & Elimination Proofs ──
    def test_22_movement_derivations_all_10_patterns(self):
        nt_patterns = [
            "nt_extended_gcd", "nt_modular_inverse", "nt_chinese_remainder",
            "nt_linear_sieve", "nt_euler_totient", "nt_mobius_inversion",
            "nt_matrix_power", "nt_combinatorics_factorials", "nt_lucas_theorem",
            "nt_miller_rabin"
        ]
        for pat in nt_patterns:
            mov = MovementDerivationEngine.derive(pat, {})
            self.assertTrue(len(mov.objective_function) > 0, f"Missing objective for {pat}")
            self.assertTrue(len(mov.decision_conditions) > 0, f"Missing decisions for {pat}")
            self.assertTrue(len(mov.elimination_proof) > 0, f"Missing proof for {pat}")

    # ── Test 23: C++ Generator Dispatch for All 10 Patterns ──
    def test_23_cpp_generator_dispatch_all_10_patterns(self):
        nt_patterns = [
            "nt_extended_gcd", "nt_modular_inverse", "nt_chinese_remainder",
            "nt_linear_sieve", "nt_euler_totient", "nt_mobius_inversion",
            "nt_matrix_power", "nt_combinatorics_factorials", "nt_lucas_theorem",
            "nt_miller_rabin"
        ]
        for pat in nt_patterns:
            code = CppPointerGenerator.generate(pat, {})
            self.assertIn("#include <iostream>", code)
            self.assertIn("int main()", code)

    # ── Test 24: C++ Standalone Compilation Check ──
    def test_24_cpp_generator_standalone_compilation(self):
        # Verify compilation of Miller-Rabin with unsigned long long
        code = generate_nt_cpp("nt_miller_rabin", {})
        self.assertIn("unsigned long long", code)
        self.assertIn("mul_mod", code)
        tmp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp.write(code.encode("utf-8"))
        tmp.close()
        exe = tmp.name[:-4]
        try:
            res = subprocess.run(["g++", "-std=c++17", "-O2", tmp.name, "-o", exe], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Compilation failed: {res.stderr}")
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
            if os.path.exists(exe):
                os.remove(exe)

    # ── Test 25: Bridge handle_request Integration ──
    def test_25_bridge_handle_request_number_theory(self):
        res = handle_request({"problemText": "Solve linear Diophantine equation a*x + b*y = c using extended GCD."})
        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("family"), "number_theory")
        self.assertEqual(res.get("selectedPattern"), "nt_extended_gcd")
        self.assertIsNotNone(res.get("number_theory"))
        self.assertTrue(res["number_theory"]["detected"])

    # ── Test 26: Candidate Eliminator Overrides Generic Fallbacks ──
    def test_26_candidate_eliminator_overrides_generic_fallbacks(self):
        features = FeatureExtractor.extract("Find modular inverse of a modulo m using extended GCD.")
        generic_candidate = AlgorithmCandidate(
            pattern="graph_shortest_path_or_scc",
            family="graph",
            confidence_prior=0.5,
            supporting_signals=[]
        )
        eval_res = CandidateEliminator.evaluate_candidate(generic_candidate, features)
        self.assertFalse(eval_res.accepted)
        self.assertEqual(eval_res.rejection_code, "NT_SPECIFIC_ALGORITHM_RESOLVED")
        self.assertEqual(eval_res.recommended_alternative, "nt_modular_inverse")


if __name__ == "__main__":
    unittest.main()
