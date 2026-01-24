# examples/langchain_integration.py
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from emocore import EmoCoreAgent, step, Signals

class EmoCoreLangChainAgent:
    def __init__(self, llm, tools, profile=None):
        self.emocore = EmoCoreAgent(profile)
        self.langchain_agent = create_openai_tools_agent(llm, tools)
        self.executor = AgentExecutor(agent=self.langchain_agent, tools=tools)
        
    def run(self, task, max_iterations=50):
        for i in range(max_iterations):
            # Execute one step of LangChain agent
            result = self.executor.invoke({"input": task})
            
            # Extract signals from LangChain result
            signals = self._extract_signals(result, i)
            
            # Check EmoCore governance
            emocore_result = step(self.emocore, signals)
            
            if emocore_result.halted:
                return {
                    "status": "halted",
                    "reason": emocore_result.reason,
                    "output": result
                }
                
            if result.get("final_answer"):
                return {
                    "status": "success",
                    "output": result
                }
                
    def _extract_signals(self, result, iteration):
        # Extract reward based on progress
        reward = 1.0 if result.get("final_answer") else 0.3
        
        # Extract novelty from intermediate steps
        novelty = 0.8 if result.get("intermediate_steps") else 0.2
        
        # Extract urgency (increases with iterations)
        urgency = min(iteration / 50, 1.0)
        
        return Signals(reward=reward, novelty=novelty, urgency=urgency)

# Usage example
if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    
    # This is a template example
    print("EmoCore LangChain Integration Example Loaded.")
