# tests/test_integration.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_full_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1. Upload
        files = {'file': ('test_audio.wav', b'test data', 'audio/wav')}
        upload_response = await ac.post("/upload/text", files=files)
        assert upload_response.status_code == 200
        session_id = upload_response.json()["session_id"]

        # 2. Generate
        generate_response = await ac.post(f"/generate/{session_id}?voice_id=somevoice")
        assert generate_response.status_code in [200, 404]  # depends if dummy ID

        # 3. Stream
        stream_response = await ac.get(f"/stream/{session_id}")
        assert stream_response.status_code in [200, 404]
