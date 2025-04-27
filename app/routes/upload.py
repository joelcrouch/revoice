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
