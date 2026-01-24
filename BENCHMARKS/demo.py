import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from emocore.agent import EmoCoreAgent
from emocore.profiles import AGGRESSIVE
from emocore.interface import step, Signals

agent = EmoCoreAgent(AGGRESSIVE)

while True:
    result = step(agent, Signals(reward=0.0, urgency=0.8))
    print(result)
    if result.halted:
        break
