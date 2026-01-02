import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.agent import EmoCoreAgent
from emocore.interface import step, Signals
def test_interface_step_runs():
    agent = EmoCoreAgent()
    
    result = step(agent, Signals(reward=0.5))

    assert result is not None
    assert hasattr(result, "state")
    assert hasattr(result, "budget")