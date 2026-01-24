# core/__init__.py
"""
EmoCore - Runtime Governance for Autonomous Agents

Public API:
    from core import EmoCoreAgent, step, Signals
    from core.profiles import PROFILES, ProfileType

Usage:
    agent = EmoCoreAgent()
    result = step(agent, Signals(reward=0.5, novelty=0.1, urgency=0.2))
"""

from core.agent import EmoCoreAgent
from core.interface import step, observe, Signals
from core.observation import Observation
from core.adapters import LLMLoopAdapter, ToolCallingAgentAdapter
from core.guarantees import StepResult, GuaranteeEnforcer
from core.failures import FailureType
from core.modes import Mode
from core.behavior import BehaviorBudget
from core.state import PressureState
from core.profiles import Profile, PROFILES, ProfileType

__all__ = [
    # Main API
    "EmoCoreAgent",
    "step",
    "observe",
    "Signals",
    "Observation",
    "StepResult",
    # Adapters
    "LLMLoopAdapter",
    "ToolCallingAgentAdapter",
    # Types
    "FailureType",
    "Mode",
    "BehaviorBudget",
    "PressureState",
    # Profiles
    "Profile",
    "PROFILES",
    "ProfileType",
    # Guarantees
    "GuaranteeEnforcer",
]

__version__ = "0.7.0"
