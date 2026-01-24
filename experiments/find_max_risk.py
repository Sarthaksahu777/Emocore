import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from emocore.agent import EmoCoreAgent
from emocore.profiles import PROFILES, ProfileType
from emocore.failures import FailureType

max_risk_ever = 0.0
best_params = None

for p_type in [ProfileType.BALANCED, ProfileType.AGGRESSIVE, ProfileType.CONSERVATIVE]:
    for r in [0.0, 0.1, 0.5, 1.0, 2.0]:
        for n in [0.0, 0.1, 0.5, 1.0, 2.0]:
            for u in [0.0, 0.5, 0.8, 1.0, 2.0]:
                agent = EmoCoreAgent(PROFILES[p_type])
                for i in range(100):
                    res = agent.step(reward=r, novelty=n, urgency=u)
                    if res.budget.risk > max_risk_ever:
                        max_risk_ever = res.budget.risk
                        best_params = (p_type, r, n, u)
                    if res.halted:
                        break

print(f"Max risk ever: {max_risk_ever}")
print(f"Best params: {best_params}")
