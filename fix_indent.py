with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_for_loop = False
for i, line in enumerate(lines):
    if "for cmd in commands:" in line:
        in_for_loop = True
    
    if in_for_loop and line.strip().startswith("elif action ==") and not line.startswith("                elif"):
        # The line is starting with 12 spaces, it needs 16 spaces
        line = "    " + line
    elif in_for_loop and line.strip().startswith("else:") and not line.startswith("                else:"):
        line = "    " + line
    elif in_for_loop and line.startswith("            chat_history.append"):
        line = "    " + line
    elif in_for_loop and line.startswith("            open_folder"):
        line = "    " + line
    elif in_for_loop and line.startswith("            read_file"):
        line = "    " + line
    elif in_for_loop and line.startswith("            play_youtube"):
        line = "    " + line
    elif in_for_loop and line.startswith("            open_website"):
        line = "    " + line
    elif in_for_loop and line.startswith("            res = "):
        line = "    " + line
    elif in_for_loop and line.startswith("            if res:"):
        line = "    " + line
    elif in_for_loop and line.startswith("            create_note"):
        line = "    " + line
    elif in_for_loop and line.startswith("            create_reminder"):
        line = "    " + line
    elif in_for_loop and line.startswith("            set_timer"):
        line = "    " + line
    elif in_for_loop and line.startswith("            run_apple_shortcut"):
        line = "    " + line
    elif in_for_loop and line.startswith("            save_fact"):
        line = "    " + line
    elif in_for_loop and line.startswith("            take_screenshot"):
        line = "    " + line
    elif in_for_loop and line.startswith("            send_imessage"):
        line = "    " + line
    elif in_for_loop and line.startswith("            send_email"):
        line = "    " + line
    elif in_for_loop and line.startswith("            mac_control"):
        line = "    " + line
    elif in_for_loop and line.startswith("            hardware_control"):
        line = "    " + line
    elif in_for_loop and line.startswith("            summary = "):
        line = "    " + line
    elif in_for_loop and line.startswith("            speak("):
        line = "    " + line
    elif in_for_loop and line.startswith("            state.add_log("):
        line = "    " + line

    if "wait_for_speech()" in line and "if run_as_thread:" not in lines[i+1] and not line.startswith("            wait_for_speech()"):
        in_for_loop = False
    
    new_lines.append(line)

with open("/Users/atharvashrivastava/Jarvis-AI/main.py", "w") as f:
    f.writelines(new_lines)
