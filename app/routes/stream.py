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
