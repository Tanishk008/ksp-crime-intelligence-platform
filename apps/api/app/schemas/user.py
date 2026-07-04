from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    badge_number: str
    full_name: str
    role: str
    rank: Optional[str] = None
    station_id: Optional[str] = None
    district_id: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=12)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    rank: Optional[str] = None
    station_id: Optional[str] = None
    district_id: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
