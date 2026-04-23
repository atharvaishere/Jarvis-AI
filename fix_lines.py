with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "else:" in line and "sys.exit(0)" in lines[i+1] and i > 225:
        lines[i] = "            else:\n"
    if "sys.exit(0)" in line and "else:" in lines[i-1] and i > 225:
        lines[i] = "                sys.exit(0)\n"

with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "w") as f:
    f.writelines(lines)
