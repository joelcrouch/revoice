# tests/test_upload.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_upload_text():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {'file': ('test_audio.wav', b'test data', 'audio/wav')}
        response = await ac.post("/upload/text", files=files)
    assert response.status_code == 200
    assert "session_id" in response.json()
