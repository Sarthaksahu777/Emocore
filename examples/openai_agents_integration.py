# examples/openai_agents_integration.py
from openai import OpenAI
from emocore import EmoCoreAgent, step, Signals

class EmoCoreOpenAIAgent:
    """OpenAI Agents with EmoCore governance"""
    
    def __init__(self, model="gpt-4", profile=None):
        self.client = OpenAI()
        self.model = model
        self.emocore = EmoCoreAgent(profile)
        
    def run_with_governance(self, messages, tools=None, max_steps=50):
        """Run agent with EmoCore governance"""
        conversation_history = messages.copy()
        
        for step_num in range(max_steps):
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation_history,
                tools=tools
            )
            
            # Extract signals
            signals = self._extract_from_response(response, step_num)
            
            # Check governance
            governance = step(self.emocore, signals)
            
            if governance.halted:
                return {
                    "status": "halted",
                    "reason": governance.reason,
                    "conversation": conversation_history,
                    "budget": governance.budget
                }
            
            # Process tool calls if any
            if response.choices[0].message.tool_calls:
                # Handle tool execution...
                pass
            else:
                # Final answer
                return {
                    "status": "success",
                    "answer": response.choices[0].message.content,
                    "conversation": conversation_history
                }
                
    def _extract_from_response(self, response, step_num):
        finish_reason = response.choices[0].finish_reason
        
        # Reward: completion vs continuation
        reward = 1.0 if finish_reason == "stop" else 0.4
        
        # Novelty: tool calls indicate exploration
        novelty = 0.8 if response.choices[0].message.tool_calls else 0.3
        
        # Urgency: increases with steps
        urgency = step_num / 50
        
        return Signals(reward=reward, novelty=novelty, urgency=urgency)

# Usage template
if __name__ == "__main__":
    print("EmoCore OpenAI Agents Integration Example Loaded.")
