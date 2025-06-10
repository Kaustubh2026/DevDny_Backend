from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    temperature = Column(Float)
    wind_speed = Column(Float)
    precipitation = Column(Float)
    condition = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="weather_data") 