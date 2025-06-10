from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.event import Event
from schemas.event_schema import EventCreate, EventUpdate, Event as EventSchema

router = APIRouter()

@router.post("/events/", response_model=EventSchema)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events/", response_model=List[EventSchema])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Update existing events with default category if needed
    events = db.query(Event).all()
    for event in events:
        if event.category is None:
            # Set default category based on event type
            if event.event_type in ['cricket', 'marathon', 'golf']:
                event.category = 'sports'
            elif event.event_type in ['wedding', 'beach', 'picnic']:
                event.category = 'social'
            elif event.event_type in ['hiking', 'camping', 'photoshoot']:
                event.category = 'outdoor'
            else:
                event.category = 'professional'
    db.commit()
    
    # Return all events
    return db.query(Event).offset(skip).limit(limit).all()

@router.get("/events/{event_id}", response_model=EventSchema)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update category if needed
    if event.category is None:
        if event.event_type in ['cricket', 'marathon', 'golf']:
            event.category = 'sports'
        elif event.event_type in ['wedding', 'beach', 'picnic']:
            event.category = 'social'
        elif event.event_type in ['hiking', 'camping', 'photoshoot']:
            event.category = 'outdoor'
        else:
            event.category = 'professional'
        db.commit()
    
    return event

@router.put("/events/{event_id}", response_model=EventSchema)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"} 