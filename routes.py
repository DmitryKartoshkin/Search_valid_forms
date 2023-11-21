from typing import Annotated
import asyncio

from fastapi import FastAPI, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request
import uvicorn

from services import find_matching_template
from validator import get_type


Form = [
        {'name': 'form_name_1', 'name_1': 'text', 'phone': 'phone', 'date': 'date', 'mail': 'email'},
        {'name': 'form_name_2', 'phone': 'phone', 'date': 'date', 'mail': 'email'},
        {'name': 'form_name_3', 'date': 'date'},
        {'name': 'form_name_4', 'name_1': 'text', 'phone': 'phone'}
]

app = FastAPI()

from mongo_bd import create_db


@app.post("/")
async def create_record(request: Request) -> dict:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    for i in Form:
        await mongo_client.records.insert_one(i)
    return {"Success": True}


@app.get("/")
async def get_records(request: Request) -> list:
    cursor = await create_db(request)
    return cursor


@app.post("/get_form")
async def post_data(request: Request, q: Annotated[str, None, Query()] = None):
    cursor = await create_db(request)

    decoded_data = dict((i.split("=")[0], i.split("=")[1]) for i in q.split("&"))
    typed_data = {field: await get_type(value) for field, value in decoded_data.items() if field != "name"}

    list_tasks = []
    for document in cursor:
        list_tasks.append(find_matching_template(document, typed_data))
    list_valid_form_name_ = await asyncio.gather(*list_tasks)
    list_valid_form_name = [i for i in list_valid_form_name_ if i]

    if list_valid_form_name:
        return {f"Name of the valid form {i}": j for i, j in enumerate(list_valid_form_name, start=1)}
    else:
        return typed_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
