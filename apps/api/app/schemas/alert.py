from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AlertBase(BaseModel):
    alert_type: str  # HOTSPOT_THRESHOLD, PATTERN_SPIKE, EARLY_WARNING
    severity: str  # LOW, MEDIUM, HIGH
    district_id: Optional[str] = None
    station_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    confidence_tier: Optional[str] = None
    supporting_data: Optional[Any] = None

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: str
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
