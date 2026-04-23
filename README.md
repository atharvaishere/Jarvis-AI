# 🤖 J.A.R.V.I.S. - Advanced Offline/Cloud Hybrid AI Assistant for macOS

An Iron-Man inspired, highly advanced AI assistant built for macOS. It features a modern 2026-style Glassmorphism UI, zero-latency streaming neural TTS, Context-Aware RAG Memory, and deep macOS hardware/software integration. 

## ✨ Key Features

- **Modern HUD Dashboard:** A beautiful PyQt6-based borderless GUI with a breathing AI glowing orb, live system vitals (CPU/RAM/Battery), and matrix-style terminal logs.
- **Hyper-Fast Brain:** Powered by Groq Cloud's `llama-3.3-70b-versatile` model, enabling human-level logic in milliseconds.
- **Multi-Step Auto-Jarvis:** Understands and executes chained commands in a single sentence (e.g., *"Set volume to max, open YouTube, and set a 5-minute timer"*).
- **Native Hindi/English Persona:** Speaks flawlessly in Hindi using Microsoft Edge's Neural TTS Engine (`hi-IN-MadhurNeural`) for ultra-realistic pronunciation.
- **Deep macOS Control:**
  - Open/Close Apps gracefully
  - Take Screenshots & Hide Windows
  - Adjust Brightness & Volume
  - Hardware toggles: Sleep, Restart, Shutdown, Wi-Fi on/off
- **Productivity & Comms:** 
  - Create Apple Notes & Reminders
  - Send iMessages and draft Emails natively
  - Run Apple Shortcuts
- **Screen Awareness:** Reads and summarizes your active Google Chrome or Safari tabs seamlessly.
- **Long-Term Memory & RAG Engine:** 
  - Save explicit personal facts to memory.
  - Drop PDFs/TXT files into `Jarvis-Brain/` and run `python core/rag_engine.py` to train Jarvis on your personal data offline!

## 🚀 Installation

### 1. Prerequisites
- macOS (M1/M2/M3 or Intel)
- Python 3.9+
- Chrome or Safari (For Screen Reading)

### 2. Setup
Clone the repository and set up a virtual environment:
```bash
git clone <your-repo-url>
cd Jarvis-AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. API Key
Get your free API key from [Groq Console](https://console.groq.com/keys).
Create a `.env` file in the root directory (you can copy `.env.example`):
```bash
cp .env.example .env
```
Edit `.env` and add your key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

## 🎮 How to Run

Launch the Modern GUI Dashboard:
```bash
python gui_modern.py
```
- Click the power button to close.
- Say *"Jarvis"* to wake the AI from sleep mode.
- Speak your command naturally. Example: *"Jarvis, open calendar and tell me the weather."*

## 📂 Project Structure
- `core/` - The main engines (Brain, RAG, Memory, Speech, Listen)
- `skills/` - Modular capabilities (Mac Ops, Comms, Web, Productivity)
- `Jarvis-Brain/` - Folder for putting your PDFs to train the RAG engine
- `gui_modern.py` - The main graphical interface

## ⚠️ Permissions Needed
On first run, macOS will prompt you to allow Terminal/Python to access:
- Microphone
- Accessibility (For Brightness & System Events)
- Apple Events (For Safari/Chrome reading & Notes/Reminders)
