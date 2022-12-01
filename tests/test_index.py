import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_index():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}
