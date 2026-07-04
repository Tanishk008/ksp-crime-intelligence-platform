from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict, Any

class CaseBase(BaseModel):
    case_number: str
    case_type: str
    status: str
    station_id: Optional[str] = None
    assigned_officer_id: Optional[str] = None
    incident_date: Optional[date] = None
    incident_location: Optional[str] = None  # WKT Point
    incident_address: Optional[str] = None
    narrative: Optional[str] = None

class CaseCreate(CaseBase):
    pass

class CaseResponse(CaseBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseDetailResponse(CaseResponse):
    entities: List[Dict[str, Any]] = []
    exhibits: List[Dict[str, Any]] = []

class CaseEntityLinkResponse(BaseModel):
    case_id: str
    entity_id: str
    role: str
    confidence: float

    class Config:
        from_attributes = True

class TimelineEventResponse(BaseModel):
    id: str
    case_id: str
    event_type: str
    description: str
    event_date: datetime
    has_conflict: bool = False
    conflict_details: Optional[str] = None
