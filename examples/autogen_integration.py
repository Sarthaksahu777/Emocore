# examples/autogen_integration.py
import autogen
from emocore import EmoCoreAgent, step, Signals

class EmoCoreAssistant(autogen.AssistantAgent):
    """AutoGen Assistant with EmoCore governance"""
    
    def __init__(self, *args, emocore_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.emocore = EmoCoreAgent(emocore_profile)
        self.message_history = []
        
    def generate_reply(self, messages, sender, **kwargs):
        """Override reply generation with EmoCore checks"""
        # Track message history
        self.message_history.append(messages[-1])
        
        # Extract signals from conversation
        signals = self._extract_from_messages(messages)
        
        # Check governance
        governance = step(self.emocore, signals)
        
        if governance.halted:
            return f"I need to stop here. Reason: {governance.reason}. " \
                   f"Failure type: {governance.failure.name}. " \
                   f"Budget state - Effort: {governance.budget.effort:.2f}"
        
        # Continue with normal reply if not halted
        return super().generate_reply(messages, sender, **kwargs)
        
    def _extract_from_messages(self, messages):
        """Extract signals from AutoGen messages"""
        recent_msg = messages[-1]["content"] if messages else ""
        
        # Reward: positive feedback or completion signals
        reward = 0.8 if any(word in recent_msg.lower() 
                           for word in ["good", "correct", "done", "complete"]) else 0.3
        
        # Novelty: new information or questions
        novelty = 0.7 if "?" in recent_msg or "new" in recent_msg.lower() else 0.2
        
        # Urgency: message count (more messages = more urgency)
        urgency = min(len(self.message_history) / 20, 1.0)
        
        return Signals(reward=reward, novelty=novelty, urgency=urgency)

# Usage template
if __name__ == "__main__":
    print("EmoCore AutoGen Integration Example Loaded.")
