with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_for_loop = False
for i, line in enumerate(lines):
    # Fix the stray indentations around line 49 and line 116
    if "speak(target)" in line and "print(f\"🗣️ Jarvis: {target}\")" in lines[i+1]:
        line = "            speak(target)\n"
    if "else:" in line and "sys.exit(0)" in lines[i+1]:
        line = "                    else:\n"

    # We need to fix lines 127 through 200 properly.
    if "for cmd in commands:" in line:
        in_for_loop = True
    
    if in_for_loop and "elif action == " in line and not line.startswith("                elif"):
        line = "                " + line.lstrip()
    elif in_for_loop and "else:" in line and not line.startswith("                else:"):
        line = "                " + line.lstrip()
    elif in_for_loop and "open_folder(" in line and not line.startswith("                    open"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "read_file(" in line and not line.startswith("                    read"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "play_youtube(" in line and not line.startswith("                    play"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "open_website(" in line and not line.startswith("                    open"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "res = " in line and not line.startswith("                    res"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "if res:" in line and not line.startswith("                    if"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "create_note(" in line and not line.startswith("                    create"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "create_reminder(" in line and not line.startswith("                    create"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "set_timer(" in line and not line.startswith("                    set"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "run_apple_shortcut(" in line and not line.startswith("                    run"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "save_fact(" in line and not line.startswith("                    save"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "take_screenshot(" in line and not line.startswith("                    take"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "send_imessage(" in line and not line.startswith("                    send"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "send_email(" in line and not line.startswith("                    send"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "mac_control(" in line and not line.startswith("                    mac"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "hardware_control(" in line and not line.startswith("                    hardware"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "summary = " in line and not line.startswith("                    summary"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "speak(" in line and "target" not in line and not line.startswith("                    speak"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "chat_history.append" in line and not line.startswith("                    chat"):
        line = "                    " + line.lstrip()
    elif in_for_loop and "state.add_log" in line and not line.startswith("                    state"):
        line = "                    " + line.lstrip()

    if "wait_for_speech()" in line and "if run_as_thread:" not in lines[i+1] and not line.startswith("            wait_for_speech()"):
        line = "            wait_for_speech()\n"
        in_for_loop = False
    
    new_lines.append(line)

with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "w") as f:
    f.writelines(new_lines)
