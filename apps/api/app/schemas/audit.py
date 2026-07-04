from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any

class AuditEventBase(BaseModel):
    event_type: str
    session_id: Optional[str] = None
    event_content: Optional[str] = None
    sources_cited: Optional[Any] = None
    confidence_tier: Optional[str] = None
    metadata: Optional[Any] = Field(None, validation_alias="event_metadata")


class AuditEventCreate(AuditEventBase):
    user_id: Optional[str] = None

class AuditEventResponse(AuditEventBase):
    id: str
    user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
