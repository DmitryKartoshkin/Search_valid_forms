import pytest
import asyncio
from httpx import AsyncClient
from pymongo import MongoClient

from routes import app


Form = [
    {'name': 'form_name_1', 'name_1': 'text', 'phone': 'phone', 'date': 'date', 'mail': 'email'},
    {'name': 'form_name_2', 'phone': 'phone', 'date': 'date', 'mail': 'email'},
    {'name': 'form_name_3', 'date': 'date'},
    {'name': 'form_name_4', 'name_1': 'text', 'phone': 'phone'}
]


@pytest.fixture(scope="module")
def event_loop():
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


@pytest.fixture(scope="session", autouse=True)
def create_db():
    client = MongoClient("mongo_db", 27017)
    db = client.test_database
    collections = db.records
    collections.insert_many(Form)

