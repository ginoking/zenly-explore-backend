import logging
# import sys
import json

from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware
from pydantic_mongo import PydanticObjectId

from app.database.mongo import (
    add_position,
    get_all_positions,
    get_positions_by_id
)

from app.models.position import PositionSchema

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    DebugToolbarMiddleware,
    panels=[
        "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
        "debug_toolbar.panels.tortoise.TortoisePanel"
    ],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/test")
async def read_position(q: Union[str, None] = None):
    return await get_positions_by_id(PydanticObjectId(q))

@app.get("/positions")
async def get_positions():
    return await get_all_positions()

@app.post("/positions")
async def create_position(position_data: PositionSchema):
    # logger.debug(type(position_data))
    # return position_data
    await add_position(position_data.model_dump())

    # logger.debug(position)
    # return position
    # return await add_position(position_data)