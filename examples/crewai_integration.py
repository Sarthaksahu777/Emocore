# examples/crewai_integration.py
from crewai import Agent, Task, Crew
from emocore import EmoCoreAgent, step, Signals, ProfileType, PROFILES

class EmoCoreCrewAgent(Agent):
    """CrewAI Agent with EmoCore governance"""
    
    def __init__(self, *args, profile=ProfileType.BALANCED, **kwargs):
        super().__init__(*args, **kwargs)
        self.emocore = EmoCoreAgent(PROFILES[profile])
        self.iteration_count = 0
        
    def execute_task(self, task):
        """Override task execution with EmoCore checks"""
        while self.iteration_count < 100:
            # Execute one step
            step_result = self._execute_step(task)
            
            # Extract signals
            signals = self._extract_signals_from_step(step_result)
            
            # Check governance
            governance = step(self.emocore, signals)
            
            if governance.halted:
                return {
                    "status": "halted",
                    "reason": governance.reason,
                    "failure_type": governance.failure,
                    "partial_result": step_result
                }
                
            if step_result.get("complete"):
                return {
                    "status": "success",
                    "result": step_result
                }
                
            self.iteration_count += 1
            
    def _extract_signals_from_step(self, step_result):
        """Extract EmoCore signals from CrewAI step"""
        # Reward: task progress
        reward = step_result.get("progress", 0.0)
        
        # Novelty: new information discovered
        novelty = 0.8 if step_result.get("new_insights") else 0.2
        
        # Urgency: task priority and time constraints
        urgency = step_result.get("urgency", 0.5)
        
        return Signals(reward=reward, novelty=novelty, urgency=urgency)

# Usage template
if __name__ == "__main__":
    print("EmoCore CrewAI Integration Example Loaded.")
