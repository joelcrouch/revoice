## How to make a python/Fastapi app that takes text and allows you to listen to it

Today, I was listening to an audiobook, and the voice was not to my preferences.
So I decided to make an app such that I can change the voice. Probably not legal.

Anyways. Here we are.

### Figure out flow of data/information

### Setup project

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
├── tests /

The above is a WIP. Change it as necessary.

### Research appropriate libraries to make this easy

### Write minimum amount of code to make this happen

So first setup your environment, inuring Python >=9.0.

```
bash
mkdir audiobook_voice_swap
cd audiobook_voice_swap

python -m venv venv
# On Windows (Git Bash / PowerShell)
source venv/Scripts/activate
# On Mac/Linux
source venv/bin/activate
pip install fastapi uvicorn pyttsx3 pydub librosa pyaudio SpeechRecognition
pip freeze > requirements.txt
```

#### Make the folder structure

In your favorite ide or vim or emacs or notepad, make the project structure as suggested above.

#### Lets start coding

These will be the API calls we will be working around:

# TODO: FIX THIS TABLE

Route | Method | Purpose
/upload/text | POST | Upload pasted text or text file
/upload/audio | POST | Upload audiobook audio file
/voices | GET | List available voices
/generate | POST | Generate TTS audio from text with selected voice
/stream/{session_id} | GET | Stream generated audio chunks

Example API workflow:

Example API Flow:

    User uploads text or audio → /upload/text or /upload/audio

    Server processes:

        If audio → transcribe ( maybe Whisper)

        If text → move on

    User selects a voice → /voices

    Server generates audio → /generate

    User listens via audio stream → /stream/{session_id}

Let start working them.
I suppose we should start out with run.py and main.py before we continue.

```
python

# run.py
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

```
python

# app/main.py
from fastapi import FastAPI
from app.routes import upload, tts, stream

app = FastAPI()

# Register Routes
app.include_router(upload.router, prefix="/upload")
app.include_router(tts.router, prefix="/generate")
app.include_router(stream.router, prefix="/stream")

```

Lets start with upload.py

```
python
# app/routes/upload.py

from fastapi import APIRouter, UploadFile, File, Form
from app.models.request_models import TextUploadRequest
from app.utils.file_utils import save_temp_text_file
import uuid

router = APIRouter()

@router.post("/text")
async def upload_text(text: str = Form(...)):
    """
    Upload pasted text via a form field and save it temporarily.
    """
    session_id = str(uuid.uuid4())  # Generate unique session id
    filepath = save_temp_text_file(session_id, text)

    return {
        "message": "Text uploaded successfully!",
        "session_id": session_id,
        "filepath": filepath
    }


```

and then request_modesl.py in models directory.

```
python
# app/models/request_models.py

from pydantic import BaseModel

class TextUploadRequest(BaseModel):
    text: str

```

and finally a little utility file.

```python
# app/utils/file_utils.py

import os

TEMP_TEXT_DIR = "temp/texts"

os.makedirs(TEMP_TEXT_DIR, exist_ok=True)

def save_temp_text_file(session_id: str, text: str) -> str:
    """
    Save uploaded text into a temporary file.
    """
    filepath = os.path.join(TEMP_TEXT_DIR, f"{session_id}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath

```

Ok. But wait. How does this work?

- User pastes a chunk of text into a form and hits upload.
- Server saves it as a temp .txt file, tagged with a unique session ID.
- Returns a response like:
  Some json response, not really useful, at this point. (wait til later.)

```

{
  "message": "Text uploaded successfully!",
  "session_id": "2cf7caae-2156-46e8-9e8d-6d8f2048c24f",
  "filepath": "temp/texts/2cf7caae-2156-46e8-9e8d-6d8f2048c24f.txt"
}

```

- Later, when the user chooses a voice, you grab that text file and run it through the TTS generator.

🧠 Recap of what we now have:

✅ Server running with FastAPI
✅ /upload/text API ready
✅ Text saving logic ready
✅ Session management started

OK. Now lets create the voices endpoint.
Create a new file: app/routes/tts.py

```python
# app/routes/tts.py

from fastapi import APIRouter
from app.services.tts_service import get_available_voices

router = APIRouter()

@router.get("/voices")
async def list_voices():
    """
    List all available TTS voices.
    """
    voices = get_available_voices()
    return {"voices": voices}
```

Make a basic TTS service: app/services/tts_service.py

```python
# app/services/tts_service.py

import pyttsx3

def get_available_voices():
    """
    Fetch available voices from pyttsx3 TTS engine.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    available_voices = []

    for voice in voices:
        available_voices.append({
            "id": voice.id,
            "name": voice.name,
            "gender": voice.gender if hasattr(voice, "gender") else "Unknown",
            "language": voice.languages[0].decode('utf-8') if voice.languages else "Unknown"
        })

    engine.stop()
    return available_voices

def synthesize_text(session_id: str, text: str, voice_id: str):
    """
    Synthesize text to speech with the selected voice.
    Save it to a temporary audio file.
    """
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)

    temp_audio_path = f"temp/audio/{session_id}.mp3"

    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()

    engine.stop()
    return temp_audio_path

```

pyttsx3 is offline — meaning no API limits — but if you later swap to ElevenLabs, AWS Polly, or Google, this service layer would just talk to their SDKs instead. These other choices will give you more choices for voices.

So what is going on here?

- voices → calls get_available_voices() → returns a list of voices.

- generate (coming next) → will call synthesize_text(session_id, text, voice_id) → and generate audio! => MVP!
  Here is where we are:
- You can upload text ✅
- You can list available voices ✅
- You can synthesize text into audio (almost — /generate API next) ✅

Let's do both: first /generate API (create the new voice audio), then /stream API (play it back)!
So lets add a new route to tts.py:

```python
# app/routes/tts.py (continued)

from fastapi import BackgroundTasks
from app.models.request_models import GenerateRequest
from app.utils.file_utils import load_temp_text
from app.services.tts_service import synthesize_text

@router.post("/")
async def generate_audio(generate_request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate audio from uploaded text using selected voice.
    """
    session_id = generate_request.session_id
    voice_id = generate_request.voice_id

    # Load the text that was uploaded
    text = load_temp_text(session_id)

    # Background task to generate audio
    background_tasks.add_task(synthesize_text, session_id, text, voice_id)

    return {"message": "Audio generation started", "session_id": session_id}

```

and update the request_models.py:

```python
# app/models/request_models.py (continued)

class GenerateRequest(BaseModel):
    session_id: str
    voice_id: str

```

And also update file_utils to load text:

```python
# app/utils/file_utils.py (continued)

def load_temp_text(session_id: str) -> str:
    """
    Load saved text from temporary file.
    """
    filepath = os.path.join("temp/texts", f"{session_id}.txt")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

```

Now, when you hit /generate:
-It grabs the text you uploaded earlier.

- Starts synthesizing speech with the selected voice.
- Saves the generated audio under /temp/audio/{session_id}.mp3.
- Returns quickly thanks to BackgroundTasks (no waiting!)

Now lets get on that stream api:

```python
# app/routes/stream.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/{session_id}")
async def stream_audio(session_id: str):
    """
    Stream generated audio file back to user.
    """
    filepath = os.path.join("temp/audio", f"{session_id}.mp3")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Audio file not found. Generation may still be processing.")

    return FileResponse(filepath, media_type="audio/mpeg", filename=f"{session_id}.mp3")

```

Recap of Full Flow Now:

- Upload Text → /upload/text
- List Voices → /voices
- Generate Audio → /generate
- Stream Audio → /stream/{session_id}

✅ Upload → ✅ Choose Voice → ✅ Generate Voiceover → ✅ Listen!  
So this 'should' work.

But before we test it, we have to create a simple front end and add a /status/{session_id} API

Goal: Check if the generated audio file exists = "ready".

Update app/routes/stream.py (same file, add another route):

```python
# app/routes/stream.py (continued)

@router.get("/status/{session_id}")
async def check_status(session_id: str):
    """
    Check if the audio generation is complete.
    """
    filepath = os.path.join("temp/audio", f"{session_id}.mp3")

    if os.path.exists(filepath):
        return {"status": "ready"}
    else:
        return {"status": "processing"}

```

Now you have:

# TODO FIX THIS TABLE

API Description Status
/status/{id} Check if audio is ready ✅

No need to guess when the audio is done!
Frontend can poll this endpoint every few seconds if you want

Ok. Make a simple front end. We can style it and
do all the good stuff later.
Simple Frontend HTML Audio Player

Let’s make a super basic page to:

- Upload text
- Choose voice
- Generate
- Check Status
- Play the audio

```frontend.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Audiobook Voice Changer 🎧</title>
</head>
<body>
    <h1>Audiobook Voice Changer</h1>

    <h2>Step 1: Upload Text</h2>
    <textarea id="textInput" rows="10" cols="50" placeholder="Paste your audiobook text here..."></textarea><br>
    <button onclick="uploadText()">Upload Text</button>

    <h2>Step 2: Choose Voice</h2>
    <select id="voiceSelect"></select><br><br>
    <button onclick="generateAudio()">Generate Audio</button>

    <h2>Step 3: Listen</h2>
    <button onclick="checkAndPlay()">Check Status & Play</button><br><br>
    <audio id="audioPlayer" controls></audio>

    <script>
        let sessionId = "";

        async function uploadText() {
            const text = document.getElementById("textInput").value;
            const formData = new FormData();
            formData.append("text", text);

            const response = await fetch("/upload/text", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            sessionId = data.session_id;
            alert("Text uploaded! Session ID: " + sessionId);

            fetchVoices();
        }

        async function fetchVoices() {
            const response = await fetch("/generate/voices");
            const data = await response.json();
            const voiceSelect = document.getElementById("voiceSelect");
            voiceSelect.innerHTML = "";

            data.voices.forEach(voice => {
                const option = document.createElement("option");
                option.value = voice.id;
                option.textContent = `${voice.name} (${voice.language})`;
                voiceSelect.appendChild(option);
            });
        }

        async function generateAudio() {
            const selectedVoice = document.getElementById("voiceSelect").value;

            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    voice_id: selectedVoice
                })
            });

            const data = await response.json();
            alert(data.message);
        }

        async function checkAndPlay() {
            const response = await fetch("/stream/status/" + sessionId);
            const data = await response.json();

            if (data.status === "ready") {
                document.getElementById("audioPlayer").src = "/stream/" + sessionId;
            } else {
                alert("Audio still processing, try again in a few seconds!");
            }
        }
    </script>
</body>
</html>

```

How it works:

- Uploads text to /upload/text

- Fetches voices from /generate/voices

- Posts to /generate

- Checks /stream/status/{session_id}

- Streams audio /stream/{session_id} when ready

#### RUN IT

OK. I think its done. So i run it:

```python
python run.py
```

And i got a dumb error:

```error
NFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20876] using StatReload
INFO:     Started server process [9712]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:53564 - "GET /frontend.html HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53565 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53568 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53569 - "GET /favicon.ico HTTP/1.1" 404 Not Found

```

What in the heck is all this nonsense?
So from the fastapi book i just looked into painfully, i found out if you have (and we do) an app already running FastAPI correctly — this is a small expected thing because FastAPI by itself only serves APIs — it doesn't serve static HTML files automatically. So what does that mean?
FastAPI doesn’t know how to find your frontend.html yet.

Add that to the folder and let us see what is good.

Soooo...

```
bash

pip install aiofiles
pip freeze > requirements.txt
```

Update app/main.py

Add these lines to your app/main.py at the top:

```
python
[top]
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
...rest of code

[bottom of file]
# Serve the frontend.html manually
@app.get("/")
async def read_index():
    return FileResponse("frontend.html")

# Serve other static files if needed later
app.mount("/static", StaticFiles(directory="static"), name="static")


```

So i ran it again and got another big long dumb error:

```error
[biglong error-important part]...
packages\starlette\staticfiles.py", line 56, in __init__
    raise RuntimeError(f"Directory '{directory}' does not exist")
RuntimeError: Directory 'static' does not exist

```

We need a blank 'static' folder and some other changes. Dumb fix and I think i can do better but for now, here we are. So do that.

Then run it again and it should work.

### Test Unit/Integration

```
bash
pip install pytest
pip install httpx pytest-asyncio
pip freeze > requirements.txt
```

Create a test folder.

### Refactor

    - [] Break up .html file.  Add some styling to it.
    - [] Break up testsuite so it makes more sense
    -

### TODO

- Upload audio files (instead of pasting text).

- Integrate Whisper for automatic audio-to-text transcription.

- Add voice selection dropdown for different TTS voices.

- Allow saving generated MP3s for later listening.

- Split long texts into chapters or sections automatically.

- Authentication and user profiles (optional).
