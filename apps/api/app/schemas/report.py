from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class ReportBase(BaseModel):
    case_id: Optional[str] = None
    title: str

class ReportCreate(ReportBase):
    conversation_id: Optional[str] = None

class ReportResponse(ReportBase):
    id: str
    created_by: str
    content_json: Optional[Any] = None
    pdf_path: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
