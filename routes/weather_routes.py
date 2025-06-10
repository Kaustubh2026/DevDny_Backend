from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from services.weather_service import WeatherService
from schemas.weather_schema import WeatherResponse
from cache.cache_utils import weather_cache
from models.event import Event

router = APIRouter()
weather_service = WeatherService()

async def get_weather_data(location: str, date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weather_data = await weather_service.get_weather(location, date_obj)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_suitability_score(weather_data: dict, event_type: str) -> int:
    score = 100
    temp = weather_data.get("main", {}).get("temp", 0)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    weather_condition = weather_data.get("weather", [{}])[0].get("main", "").lower()
    
    # Temperature penalties
    if event_type == "outdoor":
        if temp < 10 or temp > 30:
            score -= 30
        elif temp < 15 or temp > 25:
            score -= 15
    elif event_type == "indoor":
        if temp < 15 or temp > 28:
            score -= 10
    
    # Wind speed penalties
    if wind_speed > 20:
        score -= 40
    elif wind_speed > 15:
        score -= 20
    elif wind_speed > 10:
        score -= 10
    
    # Weather condition penalties
    if weather_condition in ["rain", "snow", "thunderstorm"]:
        score -= 50
    elif weather_condition in ["drizzle", "mist", "fog"]:
        score -= 20
    
    return max(0, min(100, score))

def get_rating(score: int) -> str:
    if score >= 80:
        return "Good"
    elif score >= 50:
        return "Okay"
    else:
        return "Poor"

def get_remarks(weather_data: dict, event_type: str) -> str:
    temp = weather_data.get("main", {}).get("temp", 0)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    weather_condition = weather_data.get("weather", [{}])[0].get("description", "")
    
    remarks = []
    
    if event_type == "outdoor":
        if temp < 10:
            remarks.append("Too cold for outdoor activities")
        elif temp > 30:
            remarks.append("Too hot for outdoor activities")
    elif event_type == "indoor":
        if temp < 15:
            remarks.append("Consider heating")
        elif temp > 28:
            remarks.append("Consider cooling")
    
    if wind_speed > 15:
        remarks.append("Strong winds expected")
    
    if weather_condition:
        remarks.append(f"Weather condition: {weather_condition}")
    
    return " | ".join(remarks) if remarks else "Weather conditions are suitable"

@router.get("/weather/{location}/{date}", response_model=WeatherResponse)
async def get_weather(location: str, date: str, db: Session = Depends(get_db)):
    try:
        # Parse date string to datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        
        # Check cache first
        cached_data = weather_cache.get(location, date_obj)
        if cached_data:
            return cached_data
        
        # Get weather data from service
        weather_data = await weather_service.get_weather(location, date_obj)
        
        # Create response
        response = WeatherResponse(
            location=location,
            date=date_obj,
            temperature=weather_data["temperature"],
            wind_speed=weather_data["wind_speed"],
            precipitation=weather_data["precipitation"],
            condition=weather_data["condition"]
        )
        
        # Cache the response
        weather_cache.set(location, date_obj, response.dict())
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}/suitability")
async def get_event_suitability(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Get weather data
    weather_data = await get_weather_data(event.location, event.date)
    
    # Calculate suitability score
    score = calculate_suitability_score(weather_data, event.event_type)
    rating = get_rating(score)
    remarks = get_remarks(weather_data, event.event_type)

    return {
        "score": score,
        "rating": rating,
        "remarks": remarks,
        "temperature": weather_data.get("main", {}).get("temp"),
        "conditions": weather_data.get("weather", [{}])[0].get("description", "Unknown"),
        "humidity": weather_data.get("main", {}).get("humidity"),
        "wind_speed": weather_data.get("wind", {}).get("speed")
    }

@router.get("/events/{event_id}/alternatives")
async def get_alternative_dates(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    alternatives = []
    event_date = datetime.strptime(event.date, "%Y-%m-%d")
    
    for i in range(1, 6):  # Check next 5 days
        check_date = event_date + timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        
        weather_data = await get_weather_data(event.location, date_str)
        score = calculate_suitability_score(weather_data, event.event_type)
        rating = get_rating(score)
        remarks = get_remarks(weather_data, event.event_type)
        
        alternatives.append({
            "date": date_str,
            "score": score,
            "rating": rating,
            "remarks": remarks,
            "temperature": weather_data.get("main", {}).get("temp"),
            "conditions": weather_data.get("weather", [{}])[0].get("description", "Unknown")
        })
    
    return alternatives 