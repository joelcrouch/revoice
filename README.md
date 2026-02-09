# ReVoice - AI-powered Text-to-Speech Application

## Project Overview

ReVoice is a lightweight, AI-powered Text-to-Speech (TTS) application built with FastAPI. It allows users to upload text, select from available voices, and generate audio in an asynchronous manner. The generated audio can then be streamed back to the user. The application leverages `pyttsx3` for its text-to-speech capabilities, providing an offline and cross-platform solution.

## Features

*   **Text Upload:** Easily upload text content via a dedicated API endpoint.
*   **Voice Management:** Retrieve a list of all available TTS voices.
*   **Asynchronous Audio Generation:** Generate audio from text using a selected voice as a background task, preventing API timeouts.
*   **Audio Streaming:** Stream the generated audio file directly to the user.
*   **Generation Status Check:** Monitor the progress of audio generation.
*   **Simple Web Interface:** A basic `frontend.html` is provided for interaction.

## Technology Stack

*   **Backend Framework:** FastAPI
*   **TTS Engine:** `pyttsx3` (utilizes underlying OS TTS engines like SAPI5, NSSpeechSynthesizer, eSpeak)
*   **Data Validation:** Pydantic
*   **Web Server:** Uvicorn (for running FastAPI)

## Project Structure

```
.
├───app/
│   ├───__init__.py
│   ├───main.py                 # Main FastAPI application
│   ├───models/
│   │   ├───__init__.py
│   │   └───request_models.py   # Pydantic models for API requests
│   ├───routes/
│   │   ├───__init__.py
│   │   ├───stream.py           # API routes for audio streaming and status checks
│   │   ├───tts.py              # API routes for TTS voice listing and generation
│   │   └───upload.py           # API routes for text upload
│   ├───services/
│   │   ├───__init__.py
│   │   └───tts_service.py      # Core TTS logic using pyttsx3
│   └───utils/
│       ├───__init__.py
│       └───file_utils.py       # Utility functions for file operations
├───frontend.html               # Simple frontend for demonstration
├───run.py                      # (Likely) Script to run the application
├───tests/                      # Unit and integration tests
│   ├───test_integration.py
│   ├───test_tts.py
│   └───test_upload.py
├───.gitignore
├───HOWTO.md
└───README.md
```

## Setup and Installation

To set up and run ReVoice, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:joelcrouch/revoice.git
    cd revoice
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    It is recommended to generate a `requirements.txt` file first.
    ```bash
    # You might need to run this command first to generate requirements.txt
    # pip freeze > requirements.txt
    pip install -r requirements.txt
    ```
    **Note:** Ensure you have `pyttsx3` compatible TTS engine installed on your system (e.g., eSpeak for Linux, SAPI5 for Windows).

## Running the Application

1.  **Start the FastAPI Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will run on `http://127.0.0.1:8000` by default.

2.  **Access the Frontend:**
    Open your web browser and navigate to `http://127.0.0.1:8000`. The `frontend.html` provides a basic interface to interact with the API.

## API Endpoints

The ReVoice application exposes the following API endpoints:

### Text Upload

*   **Endpoint:** `/upload/text`
*   **Method:** `POST`
*   **Description:** Uploads text for audio generation.
*   **Request Body (Form Data):**
    *   `text`: The text content to be synthesized.
*   **Response:**
    ```json
    {
        "message": "Text uploaded successfully!",
        "session_id": "unique-session-id",
        "filepath": "path/to/temp/text/file"
    }
    ```

### TTS Voice Listing

*   **Endpoint:** `/generate/voices`
*   **Method:** `GET`
*   **Description:** Retrieves a list of available TTS voices.
*   **Response:**
    ```json
    {
        "voices": [
            {
                "id": "voice-id-1",
                "name": "Voice Name 1",
                "gender": "male/female/unknown",
                "language": "en-US"
            },
            // ... more voices
        ]
    }
    ```

### Audio Generation

*   **Endpoint:** `/generate/`
*   **Method:** `POST`
*   **Description:** Initiates asynchronous audio generation from previously uploaded text.
*   **Request Body (JSON):**
    ```json
    {
        "session_id": "unique-session-id-from-upload",
        "voice_id": "id-of-selected-voice"
    }
    ```
*   **Response:**
    ```json
    {
        "message": "Audio generation started",
        "session_id": "unique-session-id-from-upload"
    }
    ```

### Audio Streaming

*   **Endpoint:** `/stream/{session_id}`
*   **Method:** `GET`
*   **Description:** Streams the generated audio file.
*   **Response:** Binary audio stream (`audio/mpeg`)

### Generation Status Check

*   **Endpoint:** `/stream/status/{session_id}`
*   **Method:** `GET`
*   **Description:** Checks the status of the audio generation for a given session.
*   **Response:**
    ```json
    {
        "status": "ready"
    }
    ```
    or
    ```json
    {
        "status": "processing"
    }
    ```

## Testing

The project includes a `tests/` directory with unit and integration tests. To run the tests, you will typically use `pytest`:

```bash
pip install pytest
pytest
```

## Future Improvements (Ideas )

    Upload audio files (instead of pasting text).

    Integrate Whisper for automatic audio-to-text transcription.

    Add voice selection dropdown for different TTS voices.

    Allow saving generated MP3s for later listening.

    Split long texts into chapters or sections automatically.

    Authentication and user profiles (optional).

## Acknowledgments

    Inspired by the need for more flexible audiobook listening experiences.

    Powered by the open-source Python ecosystem.



## Contributing

(Add guidelines for contributing if this were an open-source project)

## License

MIT License.
Feel free to use, modify, and share this project!
