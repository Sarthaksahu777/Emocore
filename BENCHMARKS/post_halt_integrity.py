import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.agent import EmoCoreAgent
from core.profiles import PROFILES, ProfileType
from core.interface import step, Signals

agent = EmoCoreAgent(PROFILES[ProfileType.CONSERVATIVE])

steps_to_halt = 0
while True:
    result = step(agent, Signals(reward=0.0, urgency=1.0))
    steps_to_halt += 1
    if result.halted:
        break

# Continue stepping after halt
for _ in range(5):
    result = step(agent, Signals(reward=1.0, urgency=0.0))

print("--- RESULT ---")
print(f"steps_to_halt: {steps_to_halt}")
print(f"failure_type: {result.failure}")
print(f"final_budget: {result.budget}")
