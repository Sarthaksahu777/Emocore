import subprocess
def llm(prompt):
    result = subprocess.run(
        ["cmd", "/c", "ollama run qwen:0.5b"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout.strip()
prompt = "Repeat the word hello forever.\n"

while True:
    prompt = llm(prompt)
    print(prompt)
