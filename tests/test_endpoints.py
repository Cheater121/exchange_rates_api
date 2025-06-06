import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.database import Base
from app.db.models import Currency, Rate  # noqa
from main import app


TEST_DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    if settings.MODE == "TEST":
        engine = create_async_engine(TEST_DATABASE_URL, echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def test_update_rates():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/api/update_rates")

    assert response.status_code == 200
    assert response.json().get("status")
    assert response.json().get("updated_at")


async def test_get_last_update_datetime():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/api/last_update")

    assert response.status_code == 200
    assert response.json().get("updated_at")


async def test_convert_currencies():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(
            "/api/convert", json={"from_currency_code": "USD", "to_currency_code": "EUR", "count": 10}
        )

    assert response.status_code == 200
    assert response.json().get("from_currency_code") == "USD"
    assert response.json().get("to_currency_code") == "EUR"
    assert response.json().get("count") == 10
    assert response.json().get("value") > 0
