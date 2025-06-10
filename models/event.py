from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    date = Column(DateTime)
    event_type = Column(String)  # e.g., "cricket", "wedding", "hiking"
    category = Column(String)  # e.g., "sports", "social", "outdoor", "professional"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    weather_data = relationship("WeatherData", back_populates="event")
    analysis = relationship("EventWeatherAnalysis", back_populates="event") 