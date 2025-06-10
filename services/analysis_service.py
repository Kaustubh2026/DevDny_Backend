from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.event import Event
from models.weather import WeatherData
from models.analysis import EventWeatherAnalysis
from services.weather_service import WeatherService

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()

    async def analyze_event_weather(self, event_id: int) -> Dict[str, Any]:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise ValueError(f"Event with id {event_id} not found")

        # Get weather data
        weather_data = await self.weather_service.get_weather(event.location, event.date)
        
        # Calculate suitability score
        analysis = self.weather_service.calculate_suitability_score(weather_data, event.event_type)
        
        # Store weather data
        weather_record = WeatherData(
            event_id=event_id,
            temperature=weather_data["temperature"],
            wind_speed=weather_data["wind_speed"],
            precipitation=weather_data["precipitation"],
            condition=weather_data["condition"]
        )
        self.db.add(weather_record)
        
        # Store analysis
        analysis_record = EventWeatherAnalysis(
            event_id=event_id,
            score=analysis["score"],
            remarks=analysis["remarks"]
        )
        self.db.add(analysis_record)
        self.db.commit()
        
        return analysis

    async def suggest_alternative_dates(self, event_id: int) -> List[Dict[str, Any]]:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise ValueError(f"Event with id {event_id} not found")

        alternatives = []
        current_date = event.date
        
        # Check next 5 days
        for i in range(1, 6):
            check_date = current_date + timedelta(days=i)
            weather_data = await self.weather_service.get_weather(event.location, check_date)
            analysis = self.weather_service.calculate_suitability_score(weather_data, event.event_type)
            
            alternatives.append({
                "date": check_date,
                "weather": weather_data,
                "analysis": analysis
            })
        
        # Sort by score in descending order
        alternatives.sort(key=lambda x: x["analysis"]["score"], reverse=True)
        return alternatives 