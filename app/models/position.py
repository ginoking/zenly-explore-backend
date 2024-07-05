from typing import Optional

from pydantic import ConfigDict, BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude
from pydantic_mongo import PydanticObjectId
from datetime import datetime

class PositionSchema(BaseModel):
    id: Optional[PydanticObjectId] = None
    longitude: Longitude
    latitude: Latitude
    timestamp: Optional[datetime] = datetime.now()
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    altitudeAccuracy: Optional[float] = None
    heading: Optional[float] = None
    headingAccuracy: Optional[float] = None
    speed: Optional[float] = None
    speedAccuracy: Optional[float] = None
    floor: Optional[float] = None
    isMocked: bool = False
    model_config = ConfigDict(
        # populate_by_name = True,
        # arbitrary_types_allowed = True,
        json_schema_extra = {
            "example": {
                "longitude": 0.0,
                "latitude": 0.0,
                "timestamp": datetime.now(),
                "accuracy": 0.0,
                "altitude": 0.0,
                "altitudeAccuracy": 0.0,
                "heading": 0.0,
                "headingAccuracy": 0.0,
                "speed": 0.0,
                "speedAccuracy": 0.0,
                "floor": 0.0,
                "isMocked": False
            }
        }
    )