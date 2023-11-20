from typing import Annotated
import asyncio
from fastapi import FastAPI, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from services import find_matching_template
from validator import get_type

test = "name1=test1&name1=test2&date=30.08.2035&mail=test1@gmail.com&phone=+7 777 88 86"

Form = [
    {
        "name": "form_name_1",
        "name_frend": "text",
        "phone": "phone",
        "date": "date",
        "mail": "email"
    },
    {
        "name": "form_name_2",
        "phone": "phone___",
        "date": "date",
        "mail": "email"
    },
    {
        "name": "form_name_3",
        "mail": "email"
    }
]

app = FastAPI()
MONGODB_URL = "mongodb://mongo_db:27017/test_database"
# MONGODB_URL = "mongodb://localhost:27017/test_database"
client = AsyncIOMotorClient(MONGODB_URL)
app.state.mongo_client = client


@app.post("/")
async def create_record(request: Request) -> dict:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    for i in Form:
        await mongo_client.records.insert_one(i)
    return {"Success": True}


@app.get("/")
async def get_records(request: Request) -> list:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    cursor = mongo_client.records.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


@app.post("/get_form")
async def post_data(request: Request, q: Annotated[str, None, Query()] = None):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    cursor = mongo_client.records.find({})

    # получаем словарь значений парметров запроса
    decoded_data = dict((i.split("=")[0], i.split("=")[1]) for i in q.split("&"))

    # получаем словарь с типами значений парметров запроса
    typed_data = {field: await get_type(value) for field, value in decoded_data.items() if field != "name"}

    list_tasks = []
    for document in await cursor.to_list(length=100):
        list_tasks.append(find_matching_template(document, typed_data))
    list_valid_form_name_ = await asyncio.gather(*list_tasks)
    list_valid_form_name = [i for i in list_valid_form_name_ if i]

    if list_valid_form_name:
        return {f"Name of the valid form {i}": j for i, j in enumerate(list_valid_form_name, start=1)}
    else:
        return typed_data


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5050)
