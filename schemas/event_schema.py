from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    location: str
    date: datetime
    event_type: str
    category: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    event_type: Optional[str] = None
    category: Optional[str] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 