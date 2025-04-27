🎧 Audiobook Voice Swap

Audiobook Voice Swap is a Python web app that lets you paste text (like from an audiobook) and generate a new voice to read it aloud — live!
It uses modern speech-to-text (STT) and text-to-speech (TTS) technology to swap audiobook narration into a voice of your choice.
🚀 Features

    🗣️ Input text manually (e.g., from an audiobook).

    🎙️ Generate and listen to new voice narration in real-time.

    📄 Simple web frontend to paste text and listen.

    🛠️ Backend built with FastAPI and Uvicorn.

    🎶 Audio streamed dynamically — no need to download files.

    🧹 Easy to extend with additional voices, storage options, or enhancements.

📦 Project Structure

audiobook_voice_swap/
│
├── app/
│ ├── main.py # FastAPI app entrypoint
│ ├── tts_service.py # Text-to-Speech utilities
│ ├── models.py # Pydantic models (request/response schemas)
│ └── utils.py # Helper functions (optional)
│
├── static/
│ ├── frontend.html # Simple HTML page with player and text input
│
├── venv/ # Python virtual environment (ignored by git)
│
├── run.py # Script to run the app
├── .gitignore # Git ignore rules
└── README.md # This file

🔧 Setup Instructions
Clone the repository, Create and activate a virtual environment,Install dependencies,

```bash
git clone https://github.com/your-username/audiobook_voice_swap.git
cd audiobook_voice_swap

python -m venv venv
# On Windows (Git Bash / PowerShell)

source venv/Scripts/activate

# On Mac/Linux

source venv/bin/activate

pip install -r requirements.txt
```

Run the app:

```bash
python run.py
```

Visit your browser: Open http://127.0.0.1:8000/frontend.html

🛠️ Core Technologies

    Python 3.10+

    FastAPI (web server)

    Uvicorn (ASGI server)

    pyttsx3 (offline TTS engine)

    Pydub (audio manipulation)

    Frontend: Basic HTML5 + <audio> player

📋 Future Improvements (Ideas 💡)

    Upload audio files (instead of pasting text).

    Integrate Whisper for automatic audio-to-text transcription.

    Add voice selection dropdown for different TTS voices.

    Allow saving generated MP3s for later listening.

    Split long texts into chapters or sections automatically.

    Authentication and user profiles (optional).

🙌 Acknowledgments

    Inspired by the need for more flexible audiobook listening experiences.

    Powered by the open-source Python ecosystem.

📜 License

MIT License.
Feel free to use, modify, and share this project!
