# EmoCore Integrations

This folder contains working examples of EmoCore integrated with popular LLM frameworks.

## Quick Start

### Using Ollama (Local, No API Key Required)

Make sure Ollama is running with a model installed:
```bash
ollama run gemma3:1b
```

Then run any `*_ollama.py` example:
```bash
python integrations/langchain_ollama.py
python integrations/autogen_ollama.py
python integrations/openai_sdk_ollama.py
python integrations/crewai_ollama.py
```

### Using OpenAI API (Requires API Key)

Set your API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

Then run any `*_openai.py` example:
```bash
python integrations/langchain_openai.py
python integrations/autogen_openai.py
python integrations/openai_sdk.py
python integrations/crewai_openai.py
```

## What Each Example Demonstrates

| File | Framework | Backend | What It Shows |
|------|-----------|---------|---------------|
| `langchain_ollama.py` | LangChain | Ollama | Agent loop with EmoCore governance |
| `autogen_ollama.py` | AutoGen | Ollama | Multi-agent chat with EmoCore |
| `openai_sdk_ollama.py` | OpenAI SDK | Ollama | Direct API calls with EmoCore |
| `crewai_ollama.py` | CrewAI | Ollama | Role-based agents with EmoCore |

## Dependencies

Install framework dependencies as needed:
```bash
# LangChain
pip install langchain langchain-ollama  # For Ollama
pip install langchain langchain-openai  # For OpenAI

# AutoGen
pip install autogen-agentchat autogen-ext

# CrewAI
pip install crewai

# OpenAI SDK (also works with Ollama)
pip install openai
```

## How EmoCore Helps

Each example shows how EmoCore prevents:
- **Infinite loops** - Agent keeps retrying without progress
- **Resource exhaustion** - Agent burns through tokens/time
- **Silent failures** - Agent appears to work but accomplishes nothing

EmoCore adds a governance layer that halts execution when these patterns are detected.
