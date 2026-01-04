# core/agent.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.engine import EmoEngine
from core.profiles import Profile, PROFILES, ProfileType


class EmoCoreAgent:
    def __init__(self, profile: Profile = PROFILES[ProfileType.BALANCED]):
        self.engine = EmoEngine(profile)

    def step(self, reward: float, novelty: float, urgency: float):
        return self.engine.step(reward, novelty, urgency)
