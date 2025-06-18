from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.weather import WeatherData
from database import get_db
from supabase import Client

router = APIRouter()

@router.get("/", response_model=List[WeatherData])
async def get_weather_data(db: Client = Depends(get_db)):
    response = db.table("weather_data").select("*").execute()
    return [WeatherData.from_supabase(item) for item in response.data]

@router.post("/", response_model=WeatherData)
async def create_weather_data(weather: WeatherData, db: Client = Depends(get_db)):
    response = db.table("weather_data").insert(weather.to_dict()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create weather data")
    return WeatherData.from_supabase(response.data[0])

@router.get("/{weather_id}", response_model=WeatherData)
async def get_weather_data_by_id(weather_id: int, db: Client = Depends(get_db)):
    response = db.table("weather_data").select("*").eq("id", weather_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return WeatherData.from_supabase(response.data[0])

@router.put("/{weather_id}", response_model=WeatherData)
async def update_weather_data(weather_id: int, weather: WeatherData, db: Client = Depends(get_db)):
    response = db.table("weather_data").update(weather.to_dict()).eq("id", weather_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return WeatherData.from_supabase(response.data[0])

@router.delete("/{weather_id}", response_model=WeatherData)
async def delete_weather_data(weather_id: int, db: Client = Depends(get_db)):
    response = db.table("weather_data").delete().eq("id", weather_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return WeatherData.from_supabase(response.data[0]) 