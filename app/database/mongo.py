import os
import motor.motor_asyncio
from app.models.position import PositionSchema
from pydantic_extra_types.coordinate import Latitude, Longitude

MONGO_DETAILS = os.environ.get("mongoDBUrI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.local

position_collection = database.get_collection("positions")

def position_helper(position) -> dict:
    return {
        # "id": str(position["_id"]),
        "longitude": position["longitude"],
        "latitude": position["latitude"],
        "timestamp": position["timestamp"],
        "accuracy": position["accuracy"],
        "altitude": position["altitude"],
        "altitudeAccuracy": position["altitudeAccuracy"],
        "heading": position["heading"],
        "headingAccuracy": position["headingAccuracy"],
        "speed": position["speed"],
        "speedAccuracy": position["speedAccuracy"],
        "floor": position["floor"],
        "isMocked": position["isMocked"]
    }

async def add_position(position_data: PositionSchema) -> dict:
    exists = await get_position_by_latlng(position_data.get('latitude'), position_data.get('longitude'))
    if exists is not None: 
        return exists
    position = await position_collection.insert_one(position_data)

    new_position = await position_collection.find_one({"_id": position.inserted_id})

    return new_position


async def get_all_positions() -> list:
    positions = []
    async for position in position_collection.find():
        positions.append(position_helper(position))
    return positions

async def get_positions_by_id(id) -> dict:
    return await position_collection.find_one({"_id": id}, {'_id': 0})

async def get_position_by_latlng(lat: float, lng: float) -> dict:
    return await position_collection.find_one(
        {
            "longitude": lng,
            "latitude": lat
        }, 
        {'_id': 0}
    )