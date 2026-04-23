with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix the sys.exit(0) under else (around line 117)
    if "else:" in lines[i-1] and "sys.exit(0)" in line and not line.startswith("                        sys.exit"):
        line = "                        sys.exit(0)\n"
    # Fix chat_history.append under if res:
    elif "if res:" in lines[i-1] and "chat_history.append" in line and not line.startswith("                        chat"):
        line = "                        " + line.lstrip()
    # Fix else under KeyboardInterrupt
    elif "else:" in line and "sys.exit(0)" in lines[i+1] and "KeyboardInterrupt" in lines[i-3] and not line.startswith("            else:"):
        line = "            else:\n"
    # Fix sys.exit under KeyboardInterrupt else
    elif "sys.exit(0)" in line and "else:" in lines[i-1] and "KeyboardInterrupt" in lines[i-4] and not line.startswith("                sys.exit"):
        line = "                sys.exit(0)\n"
    
    new_lines.append(line)

with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "w") as f:
    f.writelines(new_lines)
