import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from emocore.agent import EmoCoreAgent
from emocore.profiles import PROFILES, ProfileType
from emocore.interface import step, Signals

agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])

steps = 0
while True:
    result = step(agent, Signals(reward=0.0, novelty=0.0, urgency=0.0))
    steps += 1

    if result.halted:
        print("--- RESULT ---")
        print(f"steps_to_halt: {steps}")
        print(f"failure_type: {result.failure}")
        print(f"final_budget: {result.budget}")
        break
