import os
import glob
from pypdf import PdfReader

def open_folder(target, speak_func):
    speak_func(f"Opening your {target} folder, sir.")

    folder_aliases = {
        'downloads': '~/Downloads',
        'documents': '~/Documents',
        'desktop': '~/Desktop',
        'pictures': '~/Pictures',
        'movies': '~/Movies',
        'music': '~/Music',
        'home': '~/'
    }

    clean_target = target.lower().strip()
    path = folder_aliases.get(clean_target)

    if path:
        expanded_path = os.path.expanduser(path)
        os.system(f'open "{expanded_path}"')
    else:
        # Fallback to searching the home directory generically or just open home
        speak_func(f"I couldn't find a standard folder named {target}. Opening your home directory instead.")
        os.system(f'open "{os.path.expanduser("~")}"')

def find_file_in_common_folders(filename):
    # Common locations to search
    locations = [
        '~/Desktop',
        '~/Downloads',
        '~/Documents'
    ]

    for loc in locations:
        path = os.path.expanduser(loc)
        # Perform a case-insensitive search
        for file in os.listdir(path):
            if filename.lower() in file.lower():
                return os.path.join(path, file)
    return None

def read_file(target, speak_func):
    speak_func(f"Searching for the file {target}, sir...")

    file_path = find_file_in_common_folders(target)

    if not file_path:
        speak_func(f"Sorry sir, I couldn't find a file named {target} on your Desktop, Downloads, or Documents.")
        return

    speak_func("File found. Let me read it for you.")

    try:
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            # Read just the first page to avoid endlessly talking
            if len(reader.pages) > 0:
                page = reader.pages[0]
                text = page.extract_text()

                # Clean up the text a bit for speaking
                text = text.replace('\n', ' ')

                # Limit reading to first 500 characters so it doesn't ramble
                summary = text[:500] + ("... That's the summary, sir." if len(text) > 500 else "")

                print(f"Reading PDF: {summary}")
                speak_func(summary)
            else:
                speak_func("The PDF seems to be empty, sir.")

        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                summary = content[:500] + ("... That's the first part of the file, sir." if len(content) > 500 else "")
                print(f"Reading Text: {summary}")
                speak_func(summary)
        else:
            speak_func("Sir, I can currently only read PDF or Text files out loud.")
            # Still open it for the user
            os.system(f'open "{file_path}"')
            speak_func("I've opened the file for you instead.")

    except Exception as e:
        print(f"Error reading file: {e}")
        speak_func("Sir, there was an error trying to read the file contents.")