import pytest

from faker import Faker
from httpx import AsyncClient

from .conftest import app


@pytest.mark.asyncio
async def test_registration():
    fake = Faker("ko_KR")
    password = fake.password()
    data = {
        "email": fake.email(),
        "password": password,
        "password_confirm": password,
        "name": fake.name(),
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json=data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_registration_exists_email():
    fake = Faker("ko_KR")
    exists_email = fake.email()
    password = fake.password()

    data1 = {
        "email": exists_email,
        "password": password,
        "password_confirm": password,
        "name": fake.name(),
    }
    data2 = {
        "email": exists_email,
        "password": password,
        "password_confirm": password,
        "name": fake.name(),
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/auth/register", json=data1)
        response = await ac.post("/api/auth/register", json=data2)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_registration_password_confirm_not_same():
    fake = Faker("ko_KR")
    data = {
        "email": fake.email(),
        "password": fake.password(),
        "password_confirm": fake.password(),
        "name": fake.name(),
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json=data)
    assert response.status_code == 400
