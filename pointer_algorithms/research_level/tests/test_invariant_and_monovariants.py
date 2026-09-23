"""
Test Suite: Pillar III — Invariant & Monovariant Synthesis Engine
Verifies bounded potential well-foundedness, modular conservation laws
(UNREACHABLE_STATE_PROVEN), and Sprague-Grundy impartial game solving on DAGs.
"""

import unittest
from pointer_algorithms.research_level.invariant_synthesizer import InvariantSynthesizer
from pointer_algorithms.research_level.research_types import (
    EpistemicStatus,
    InvariantClass,
)


class TestInvariantAndMonovariants(unittest.TestCase):

    def test_bounded_potential_valid_countdown(self):
        """Verify potential function Phi(x) = x on decreasing chain."""
        states = [5, 4, 3, 2, 1, 0]

        def transition(s):
            return [s - 1] if s > 0 else []

        def potential(s):
            return s

        cert, status, msg = InvariantSynthesizer.synthesize_bounded_potential(
            potential_formula_repr="Phi(s) = s",
            states_sample=states,
            transition_function=transition,
            potential_evaluator=potential,
        )

        self.assertEqual(status, EpistemicStatus.PROVEN)
        self.assertIsNotNone(cert)
        self.assertTrue(cert.is_valid())
        self.assertEqual(cert.invariant_class, InvariantClass.BOUNDED_POTENTIAL)
        self.assertTrue(cert.well_founded_proven)
        self.assertTrue(cert.strict_decrease_proven)
        self.assertEqual(cert.termination_bound_steps, 5)

    def test_bounded_potential_refuted_on_non_decrease(self):
        """Verify potential function rejected if a transition does not strictly decrease."""
        states = [3, 2, 1]

        # Transition has a self-loop at 2: 2 -> 2
        def transition(s):
            if s == 2:
                return [2]
            return [s - 1] if s > 0 else []

        cert, status, msg = InvariantSynthesizer.synthesize_bounded_potential(
            potential_formula_repr="Phi(s) = s",
            states_sample=states,
            transition_function=transition,
            potential_evaluator=lambda s: s,
        )

        self.assertEqual(status, EpistemicStatus.REFUTED)
        self.assertIsNone(cert)
        self.assertIn("failed strict decrease", msg)

    def test_bounded_potential_refuted_on_negative_value(self):
        """Verify potential function rejected if codomain dips below zero."""
        states = [2, 1, 0, -1]

        cert, status, msg = InvariantSynthesizer.synthesize_bounded_potential(
            potential_formula_repr="Phi(s) = s",
            states_sample=states,
            transition_function=lambda s: [],
            potential_evaluator=lambda s: s,
        )

        self.assertEqual(status, EpistemicStatus.REFUTED)
        self.assertIsNone(cert)
        self.assertIn("violated non-negativity", msg)

    def test_modular_conservation_unreachable_state_proven(self):
        """
        Verify modular conservation I(S) mod 2 proves state unreachability.
        Tile puzzle / parity invariant: start parity != target parity proves impossible.
        """
        states = [(0, 0), (1, 1), (2, 0), (0, 2)]

        # Each move changes coordinates by (+1, +1) or (-1, -1) -> (x + y) mod 2 invariant
        def transition(s):
            x, y = s
            return [(x + 1, y + 1), (x - 1, y - 1)]

        def invariant_fn(s):
            return s[0] + s[1]

        cert, is_unreachable, msg = InvariantSynthesizer.verify_modular_conservation(
            modulus=2,
            invariant_evaluator=invariant_fn,
            transition_function=transition,
            test_states=states,
            start_state=(0, 0),    # 0 + 0 = 0 mod 2
            target_state=(0, 1),   # 0 + 1 = 1 mod 2
        )

        self.assertIsNotNone(cert)
        self.assertTrue(cert.is_valid())
        self.assertTrue(is_unreachable)
        self.assertIn("UNREACHABLE_STATE_PROVEN", msg)

    def test_modular_conservation_reachable_parity(self):
        """Verify modular conservation when start and target have matching parity."""
        states = [(0, 0), (1, 1), (2, 0)]

        def transition(s):
            x, y = s
            return [(x + 1, y + 1)]

        cert, is_unreachable, msg = InvariantSynthesizer.verify_modular_conservation(
            modulus=2,
            invariant_evaluator=lambda s: s[0] + s[1],
            transition_function=transition,
            test_states=states,
            start_state=(0, 0),
            target_state=(2, 2),   # 2 + 2 = 0 mod 2
        )

        self.assertIsNotNone(cert)
        self.assertFalse(is_unreachable)
        self.assertIn("parity matches", msg)

    def test_sprague_grundy_nim_game_on_dag(self):
        """
        Verify Sprague-Grundy theorem on a 1-heap Nim game with subtract {1, 2}.
        Transitions: n -> n-1, n-2.
        Grundy values for n:
        0: 0
        1: mex({G(0)}) = mex({0}) = 1
        2: mex({G(0), G(1)}) = mex({0, 1}) = 2
        3: mex({G(1), G(2)}) = mex({1, 2}) = 0
        4: mex({G(2), G(3)}) = mex({2, 0}) = 1
        """
        transitions = {
            0: [],
            1: [0],
            2: [1, 0],
            3: [2, 1],
            4: [3, 2],
        }

        # Subgames: heap of 3 (G=0) and heap of 4 (G=1) => total XOR = 0 ^ 1 = 1 (P1 win)
        cert, total_xor, p1_win, msg = InvariantSynthesizer.solve_sprague_grundy(
            state_transitions=transitions,
            subgame_states=[3, 4],
        )

        self.assertIsNotNone(cert)
        self.assertTrue(cert.is_valid())
        self.assertEqual(total_xor, 1)
        self.assertTrue(p1_win)
        self.assertIn("First-player win proven", msg)

    def test_sprague_grundy_detects_cycles_and_rejects(self):
        """Verify Sprague-Grundy halts if game graph contains directed cycles."""
        cyclic_transitions = {
            0: [1],
            1: [2],
            2: [0],  # Directed cycle: 0 -> 1 -> 2 -> 0
        }

        cert, total_xor, p1_win, msg = InvariantSynthesizer.solve_sprague_grundy(
            state_transitions=cyclic_transitions,
            subgame_states=[0],
        )

        self.assertIsNone(cert)
        self.assertEqual(total_xor, 0)
        self.assertFalse(p1_win)
        self.assertIn("contains cycles", msg)


if __name__ == "__main__":
    unittest.main()
