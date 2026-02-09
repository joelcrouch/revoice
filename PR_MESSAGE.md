feat: Implement core ReVoice TTS functionality and improve project professionalism

This PR introduces the foundational Text-to-Speech (TTS) capabilities for the ReVoice application and significantly enhances the project's overall professionalism and maintainability.

Key changes and improvements include:

*   **Core TTS Functionality:**
    *   Implemented API endpoints for text upload (`/upload/text`), available voice listing (`/generate/voices`), and asynchronous audio generation (`/generate/`).
    *   Developed audio streaming (`/stream/{session_id}`) and generation status checks (`/stream/status/{session_id}`).
    *   Integrated `pyttsx3` for offline text-to-speech synthesis.
*   **Documentation:**
    *   Created a comprehensive `README_V2.md` detailing project overview, features, technology stack, setup, API endpoints, and testing instructions.
*   **Dependency Management:**
    *   Generated `requirements.txt` to ensure consistent environment setup.
*   **Testing Infrastructure & Reliability:**
    *   Configured `pytest` with `pytest.ini` for proper module discovery.
    *   Resolved missing test dependencies (`httpx`, `python-multipart`).
    *   Corrected `AsyncClient` usage in asynchronous tests with `httpx.ASGITransport`.
    *   Fixed `422 Unprocessable Entity` errors in tests by ensuring correct form data submission to the `/upload/text` endpoint.
*   **Runtime Stability:**
    *   Ensured necessary runtime directories (`static/`, `temp/audio/`) are present to prevent `RuntimeError`.
    *   Fixed `AttributeError` in `tts_service.py` related to `pyttsx3` language decoding.
*   **Code Quality:**
    *   Performed general code cleanup by removing numerous outdated or unnecessary comments across various files.

This PR sets a robust foundation for further development and improves the developer experience by standardizing setup and ensuring test reliability.