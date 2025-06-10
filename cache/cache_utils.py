from cachetools import TTLCache
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Get cache TTL from environment variable (default: 6 hours)
CACHE_TTL = int(os.getenv("CACHE_TTL", 21600))

class WeatherCache:
    def __init__(self):
        # Cache with TTL of 6 hours by default
        self.cache = TTLCache(maxsize=100, ttl=CACHE_TTL)

    def get_cache_key(self, location: str, date: datetime) -> str:
        # Create a unique key for location and date
        return f"{location}_{date.strftime('%Y-%m-%d')}"

    def get(self, location: str, date: datetime):
        key = self.get_cache_key(location, date)
        return self.cache.get(key)

    def set(self, location: str, date: datetime, data: dict):
        key = self.get_cache_key(location, date)
        self.cache[key] = data

    def clear(self):
        self.cache.clear()

# Create a singleton instance
weather_cache = WeatherCache() 