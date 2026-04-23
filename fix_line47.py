with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "r") as f:
    lines = f.readlines()

# Fix line 47 indentation (it should be 8 spaces: "        chat_history.append")
for i, line in enumerate(lines):
    if "chat_history.append({'role': 'assistant', 'content': target})" in line and i < 55:
        lines[i] = "        chat_history.append({'role': 'assistant', 'content': target})\n"

with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "w") as f:
    f.writelines(lines)
