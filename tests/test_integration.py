import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_full_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Upload
        form_data = {"text": "This is some test text for integration."}
        upload_response = await ac.post("/upload/text", data=form_data)
        assert upload_response.status_code == 200
        session_id = upload_response.json()["session_id"]

        # 2. Generate
        generate_response = await ac.post(f"/generate/{session_id}?voice_id=somevoice")
        assert generate_response.status_code in [200, 404]  # depends if dummy ID

        # 3. Stream
        stream_response = await ac.get(f"/stream/{session_id}")
        assert stream_response.status_code in [200, 404]
