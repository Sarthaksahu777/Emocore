import os

path = r'd:\EMOCORE\V0.5\FAILURES_MODES.md'
if os.path.exists(path):
    print(f"File exists. Size: {os.path.getsize(path)}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Content length: {len(content)}")
        print("--- CONTENT START ---")
        print(content)
        print("--- CONTENT END ---")
else:
    print("File does not exist.")
