from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.event import Event
from database import get_db
from supabase import Client

router = APIRouter()

@router.get("/", response_model=List[Event])
async def get_events(db: Client = Depends(get_db)):
    response = db.table("events").select("*").execute()
    return [Event.from_supabase(item) for item in response.data]

@router.post("/", response_model=Event)
async def create_event(event: Event, db: Client = Depends(get_db)):
    response = db.table("events").insert(event.to_dict()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create event")
    return Event.from_supabase(response.data[0])

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: int, db: Client = Depends(get_db)):
    response = db.table("events").select("*").eq("id", event_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event.from_supabase(response.data[0])

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event, db: Client = Depends(get_db)):
    response = db.table("events").update(event.to_dict()).eq("id", event_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event.from_supabase(response.data[0])

@router.delete("/{event_id}", response_model=Event)
async def delete_event(event_id: int, db: Client = Depends(get_db)):
    response = db.table("events").delete().eq("id", event_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event.from_supabase(response.data[0]) 