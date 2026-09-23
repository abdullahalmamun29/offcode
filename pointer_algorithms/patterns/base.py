"""
Base class for Pointer-Based Algorithm patterns.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from pointer_algorithms.knowledge.pointer_roles import PointerRole
from pointer_algorithms.reasoning.invariant_engine import FormalInvariant
from pointer_algorithms.reasoning.movement_derivation import MovementDerivation

class BasePointerPattern(ABC):
    """Abstract interface for all concrete pointer algorithm patterns."""

    @property
    @abstractmethod
    def pattern_name(self) -> str:
        pass

    @property
    @abstractmethod
    def family_name(self) -> str:
        pass

    @abstractmethod
    def get_pointer_roles(self) -> List[PointerRole]:
        pass

    @abstractmethod
    def get_invariant(self, params: Dict[str, Any]) -> FormalInvariant:
        pass

    @abstractmethod
    def derive_movement(self, params: Dict[str, Any]) -> MovementDerivation:
        pass

    @abstractmethod
    def simulate_step_by_step(self, input_data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Runs an in-memory simulation step by step, validating invariants at every step."""
        pass
