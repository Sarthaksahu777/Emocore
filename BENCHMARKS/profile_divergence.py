import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.agent import EmoCoreAgent
from core.profiles import PROFILES, ProfileType
from core.interface import step, Signals

profiles = ["CONSERVATIVE", "BALANCED", "AGGRESSIVE"]

for name in profiles:
    agent = EmoCoreAgent(PROFILES[ProfileType[name]])
    steps = 0

    while True:
        result = step(agent, Signals(reward=0.0, novelty=0.2, urgency=0.4))
        steps += 1

        if result.halted:
            print(f"--- RESULT ({name}) ---")
            print(f"steps_to_halt: {steps}")
            print(f"failure_type: {result.failure}")
            print(f"final_budget: {result.budget}")
            break
