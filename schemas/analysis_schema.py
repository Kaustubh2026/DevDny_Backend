from pydantic import BaseModel
from datetime import datetime

class AnalysisBase(BaseModel):
    score: float
    remarks: str

class AnalysisCreate(AnalysisBase):
    event_id: int

class Analysis(AnalysisBase):
    id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SuitabilityResponse(BaseModel):
    score: float
    rating: str  # "Good", "Okay", or "Poor"
    remarks: str 