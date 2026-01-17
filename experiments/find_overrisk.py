import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.agent import EmoCoreAgent
from core.profiles import PROFILES, ProfileType
from core.failures import FailureType

agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])

for r in [0.0, 0.1, 0.2, 0.5, 1.0]:
    for n in [0.0, 0.1, 0.5, 1.0]:
        for u in [0.0, 0.5, 0.8, 1.0, 2.0]:
            agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])
            steps = 0
            for i in range(200):
                res = agent.step(reward=r, novelty=n, urgency=u)
                steps += 1
                if res.halted:
                    if res.failure == FailureType.OVERRISK:
                        print(f"FOUND!! r={r}, n={n}, u={u}, steps={steps}")
                        sys.exit(0)
                    break
