import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataclasses import dataclass
from typing import Optional

from core.behavior import BehaviorBudget
from core.failures import FailureType
from core.modes import Mode


@dataclass(frozen=True)
class EngineResult:
    """
    Immutable result of a single EmoEngine step.
    This is the ONLY thing allowed to cross engine boundaries.
    """

    state: Optional[object]
    budget: BehaviorBudget
    halted: bool
    failure: FailureType
    reason: Optional[str]
    mode: Mode