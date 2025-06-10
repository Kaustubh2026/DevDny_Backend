from pydantic import BaseModel
from datetime import datetime

class WeatherDataBase(BaseModel):
    temperature: float
    wind_speed: float
    precipitation: float
    condition: str

class WeatherDataCreate(WeatherDataBase):
    event_id: int

class WeatherData(WeatherDataBase):
    id: int
    event_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class WeatherResponse(BaseModel):
    location: str
    date: datetime
    temperature: float
    wind_speed: float
    precipitation: float
    condition: str 