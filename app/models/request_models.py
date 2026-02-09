from pydantic import BaseModel

class TextUploadRequest(BaseModel):
    text: str

class GenerateRequest(BaseModel):
    session_id: str
    voice_id: str
