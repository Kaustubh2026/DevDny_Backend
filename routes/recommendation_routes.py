from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import get_db
from services.analysis_service import AnalysisService
from schemas.analysis_schema import SuitabilityResponse

router = APIRouter()

@router.get("/events/{event_id}/suitability", response_model=SuitabilityResponse)
async def get_event_suitability(event_id: int, db: Session = Depends(get_db)):
    try:
        analysis_service = AnalysisService(db)
        analysis = await analysis_service.analyze_event_weather(event_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}/alternatives")
async def get_alternative_dates(event_id: int, db: Session = Depends(get_db)):
    try:
        analysis_service = AnalysisService(db)
        alternatives = await analysis_service.suggest_alternative_dates(event_id)
        return alternatives
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 