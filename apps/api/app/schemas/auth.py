from pydantic import BaseModel
from app.schemas.user import UserResponse

class LoginRequest(BaseModel):
    badge_number: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
