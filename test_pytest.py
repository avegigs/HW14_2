import pytest
from httpx import AsyncClient
from main import app
from database.test_database import create_test_database, drop_test_database
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
async def test_client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
async def setup_teardown():
    await create_test_database()
    yield  
    await drop_test_database()

@pytest.mark.asyncio
async def test_register_user(test_client):
    response = await test_client.post(
        "/register/",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"
    assert response.json()["is_verified"] is False


def test_get_protected_resource(client):
    response = client.get("/protected-resource/")
    assert response.status_code == 200