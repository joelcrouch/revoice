
# app/models/request_models.py

from pydantic import BaseModel

class TextUploadRequest(BaseModel):
    text: str

# app/models/request_models.py (continued)

class GenerateRequest(BaseModel):
    session_id: str
    voice_id: str
