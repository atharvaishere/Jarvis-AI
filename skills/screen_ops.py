import subprocess
import ollama

def get_active_browser_text(speak_func):
    try:
        # Check if Google Chrome is running
        chrome_running = subprocess.run(['pgrep', '-x', 'Google Chrome'], capture_output=True).returncode == 0
        if chrome_running:
            script = "tell application \"Google Chrome\" to execute front window's active tab javascript \"document.body.innerText\""
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

            if result.returncode == 0:
                text = result.stdout.strip()
                if text and "missing value" not in text.lower():
                    return text
            else:
                error_msg = result.stderr.lower()
                if "allow javascript" in error_msg or "apple events" in error_msg:
                    speak_func("Sir, Google Chrome is blocking me. Please go to the View menu at the top, click Developer, and select 'Allow JavaScript from Apple Events'.")
                    return ""

        # Check if Safari is running
        safari_running = subprocess.run(['pgrep', '-x', 'Safari'], capture_output=True).returncode == 0
        if safari_running:
            script = "tell application \"Safari\" to do JavaScript \"document.body.innerText\" in front document"
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

            if result.returncode == 0:
                text = result.stdout.strip()
                if text and "missing value" not in text.lower():
                    return text
            else:
                error_msg = result.stderr.lower()
                if "allow javascript" in error_msg or "apple events" in error_msg:
                    speak_func("Sir, Safari is blocking me. Please go to the Develop menu at the top and select 'Allow JavaScript from Apple Events'.")
                    return ""

        return ""
    except Exception as e:
        print(f"Browser Text Error: {e}")
        return ""

def summarize_screen(speak_func, chat_history):
    speak_func("Scanning your active screen, sir...")

    text_content = get_active_browser_text(speak_func)

    if not text_content or len(text_content.strip()) < 50:
        speak_func("Sir, you don't seem to have a readable webpage open in Safari or Chrome, or I need permission to read it.")
        return "Failed to read screen."

    speak_func("I've read the webpage directly from your screen. Let me summarize it.")

    try:
        # Limit text to roughly 1000 words for the LLM to process quickly
        short_text = text_content[:4000]

        prompt = f"Summarize the following webpage content in EXACTLY 2 short, punchy sentences. Make it sound like a casual Indian bro talking to his friend. Content: {short_text}"

        messages = [{'role': 'user', 'content': prompt}]

        print("⏳ Jarvis is summarizing...")
        ai_response = ollama.chat(
            model='llama3.2',
            messages=messages,
            stream=False,
            options={'num_predict': 100, 'temperature': 0.3}
        )

        summary = ai_response['message']['content']
        print(f"Summary: {summary}")
        speak_func(summary)

        return summary

    except Exception as e:
        print(f"Screen Read Error: {e}")
        speak_func("Sorry sir, I couldn't summarize the contents of that webpage.")
        return "Error reading webpage."
