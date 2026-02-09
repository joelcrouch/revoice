import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_upload_text():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        form_data = {"text": "This is some test text."}
        response = await ac.post("/upload/text", data=form_data)
    assert response.status_code == 200
    assert "session_id" in response.json()
