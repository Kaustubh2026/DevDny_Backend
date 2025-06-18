from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.analysis import EventWeatherAnalysis
from database import get_db
from supabase import Client

router = APIRouter()

@router.get("/", response_model=List[EventWeatherAnalysis])
async def get_recommendations(db: Client = Depends(get_db)):
    response = db.table("event_weather_analysis").select("*").execute()
    return [EventWeatherAnalysis.from_supabase(item) for item in response.data]

@router.post("/", response_model=EventWeatherAnalysis)
async def create_recommendation(recommendation: EventWeatherAnalysis, db: Client = Depends(get_db)):
    response = db.table("event_weather_analysis").insert(recommendation.to_dict()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create recommendation")
    return EventWeatherAnalysis.from_supabase(response.data[0])

@router.get("/{recommendation_id}", response_model=EventWeatherAnalysis)
async def get_recommendation_by_id(recommendation_id: int, db: Client = Depends(get_db)):
    response = db.table("event_weather_analysis").select("*").eq("id", recommendation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return EventWeatherAnalysis.from_supabase(response.data[0])

@router.put("/{recommendation_id}", response_model=EventWeatherAnalysis)
async def update_recommendation(recommendation_id: int, recommendation: EventWeatherAnalysis, db: Client = Depends(get_db)):
    response = db.table("event_weather_analysis").update(recommendation.to_dict()).eq("id", recommendation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return EventWeatherAnalysis.from_supabase(response.data[0])

@router.delete("/{recommendation_id}", response_model=EventWeatherAnalysis)
async def delete_recommendation(recommendation_id: int, db: Client = Depends(get_db)):
    response = db.table("event_weather_analysis").delete().eq("id", recommendation_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return EventWeatherAnalysis.from_supabase(response.data[0]) 