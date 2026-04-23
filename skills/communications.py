import os
import subprocess

def send_imessage(contact, message, speak_func):
    speak_func(f"Sending a message to {contact}, sir.")

    # AppleScript to natively send an iMessage/SMS via the macOS Messages app
    applescript = f'''
    tell application "Messages"
        try
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{contact}" of targetService
            send "{message}" to targetBuddy
        on error
            try
                set targetService to 1st service whose service type = SMS
                set targetBuddy to buddy "{contact}" of targetService
                send "{message}" to targetBuddy
            end try
        end try
    end tell
    '''

    try:
        # Run the AppleScript using subprocess to avoid quote escaping issues
        process = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
        if process.returncode == 0:
            speak_func("Message sent successfully.")
        else:
            speak_func(f"Sir, I couldn't find a chat with {contact}. Please use an exact saved name or phone number.")
            print(f"Messages Error: {process.stderr}")
    except Exception as e:
        speak_func("There was an error sending the message.")
        print(f"Error: {e}")

def send_email(contact_email, subject, body, speak_func):
    speak_func(f"Drafting an email to {contact_email}, sir.")

    # AppleScript to natively send an email via the macOS Mail app without needing passwords!
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{contact_email}"}}
        end tell
        send newMessage
    end tell
    '''

    try:
        process = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
        if process.returncode == 0:
            speak_func("Email has been sent.")
        else:
            speak_func("Sir, there was an issue sending the email via the Mail app.")
            print(f"Mail Error: {process.stderr}")
    except Exception as e:
        speak_func("There was an error drafting the email.")
        print(f"Error: {e}")
