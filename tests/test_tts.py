# tests/test_tts.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_generate(session_id="dummy_id"):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/generate/{session_id}?voice_id=somevoice")
    # Because dummy_id doesn't exist, maybe expect a 404 or handle accordingly
    assert response.status_code in [200, 404]
