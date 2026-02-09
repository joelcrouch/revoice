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
