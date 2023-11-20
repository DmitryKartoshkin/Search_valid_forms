import pytest
import asyncio
from httpx import AsyncClient

from app.routes import app


@pytest.fixture(scope="session")
def event_lopp(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url='http://test'
    ) as ac:
        yield ac
