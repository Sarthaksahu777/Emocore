# core/interface.py

from dataclasses import dataclass, asdict
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.agent import EmoCoreAgent
from core.guarantees import (
    StepResult,
    GuaranteeEnforcer,
)
from core.failures import FailureType
from core.modes import Mode


@dataclass(frozen=True)
class Signals:
    reward: float
    novelty: float = 0.0
    urgency: float = 0.0


def step(agent: EmoCoreAgent, signals: Signals) -> StepResult:
    """
    Canonical public interface.
    Pure function: no mutation of inputs.
    """

    res = agent.step(
        reward=signals.reward,
        novelty=signals.novelty,
        urgency=signals.urgency,
    )

    # EngineResult → StepResult
    result = StepResult(
        state=asdict(res.state), # Snapshot dict for the interface
        budget=res.budget,
        halted=res.halted,
        failure=res.failure,
        reason=res.reason,
        mode=res.mode,
    )

    # Enforce guarantees (clamp, override if halted)
    return GuaranteeEnforcer().enforce(result)
