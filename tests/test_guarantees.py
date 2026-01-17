import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from core.behavior import BehaviorBudget
from core.state import PressureState
from core.failures import FailureType
from core.modes import Mode
from core.guarantees import StepResult, GuaranteeEnforcer
def test_halted_zeroes_budget():
    result = StepResult(
        state=PressureState(),
        budget=BehaviorBudget(1, 1, 1, 1),
        halted=True,
        failure=FailureType.EXHAUSTION,
        reason="exhaustion",
        mode=Mode.IDLE,
    )

    enforced = GuaranteeEnforcer().enforce(result)

    assert enforced.budget.effort == 0.0
    assert enforced.halted is True