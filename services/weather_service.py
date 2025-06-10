import os
import aiohttp
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        logger.debug(f"API Key found: {'Yes' if self.api_key else 'No'}")
        
        if not self.api_key:
            logger.error("OPENWEATHERMAP_API_KEY not found in environment variables")
            raise ValueError("OPENWEATHERMAP_API_KEY not found in environment variables")
            
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, location: str, date: datetime) -> dict:
        try:
            logger.debug(f"Fetching weather for {location} on {date}")
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"  # Use Celsius for temperature
            }
            
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                error_data = response.json()
                logger.error(f"Weather API error: {error_data}")
                raise Exception(f"Weather API error: {error_data.get('message', 'Unknown error')}")
            
            data = response.json()
            logger.debug(f"Weather data received: {data}")
            
            return {
                "main": {
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"]
                },
                "weather": data["weather"],
                "wind": {
                    "speed": data["wind"]["speed"]
                },
                "rain": data.get("rain", {}).get("1h", 0)  # Get rain volume for last hour, default to 0
            }
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise Exception(f"Error fetching weather data: {str(e)}")

    def calculate_suitability_score(self, event_type: str, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        remarks = []

        # Temperature scoring
        temp = weather_data["main"]["temp"]
        if 15 <= temp <= 30:
            score += 30
            remarks.append("Ideal temperature")
        elif 10 <= temp < 15 or 30 < temp <= 35:
            score += 15
            remarks.append("Acceptable temperature")
        else:
            remarks.append("Temperature not suitable")

        # Precipitation scoring
        precip = weather_data.get("rain", 0)
        if precip < 0.2:  # Less than 20% chance
            score += 25
            remarks.append("Low precipitation chance")
        elif precip < 0.4:
            score += 10
            remarks.append("Moderate precipitation chance")
        else:
            remarks.append("High precipitation chance")

        # Wind speed scoring
        wind = weather_data["wind"]["speed"]
        if wind < 5.5:  # Less than 20 km/h
            score += 20
            remarks.append("Light winds")
        elif wind < 11:  # Less than 40 km/h
            score += 10
            remarks.append("Moderate winds")
        else:
            remarks.append("Strong winds")

        # Weather condition scoring
        condition = weather_data["weather"][0]["main"].lower()
        if condition in ["clear", "partly cloudy"]:
            score += 25
            remarks.append("Clear weather conditions")
        elif condition in ["clouds", "scattered clouds"]:
            score += 15
            remarks.append("Cloudy conditions")
        else:
            remarks.append("Poor weather conditions")

        # Determine rating
        if score >= 80:
            rating = "Good"
        elif score >= 50:
            rating = "Okay"
        else:
            rating = "Poor"

        return {
            "score": score,
            "rating": rating,
            "remarks": " | ".join(remarks)
        } 