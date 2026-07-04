from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class ConversationBase(BaseModel):
    case_id: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    role: str  # USER, ASSISTANT
    content: str
    content_kannada: Optional[str] = None
    confidence_tier: Optional[str] = None
    sources: Optional[List[Dict[str, Any]]] = None
    reasoning_trace_id: Optional[str] = None
    has_conflict: bool = False

class MessageCreate(BaseModel):
    query: str
    language: str = "en"

class MessageResponse(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse] = []
