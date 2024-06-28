import os
import motor.motor_asyncio

from app.models.position import PositionSchema

MONGO_DETAILS = os.environ.get("mongoDBUrI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.local

position_collection = database.get_collection("positions")

def position_helper(position) -> dict:
    return {
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
    position = await position_collection.insert_one(position_data)
    # return position.inserted_id
    new_position = await position_collection.find_one({"_id": position.inserted_id}, {'_id', 0})
    # print(new_position)
    # if new_position: 
    #     return True
    # else: 
    #     return False
    return new_position
    # return position_helper(new_position)

async def get_all_positions() -> list:
    positions = []
    async for position in position_collection.find():
        positions.append(position_helper(position))
    return positions