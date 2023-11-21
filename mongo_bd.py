from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request
from typing import List

from routes import app

MONGODB_URL = "mongodb://mongo_db:27017/test_database"
client = AsyncIOMotorClient(MONGODB_URL)
app.state.mongo_client = client


async def create_db(request: Request) -> List:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    cursor = mongo_client.records.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res

