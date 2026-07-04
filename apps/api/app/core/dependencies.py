from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User

def get_current_user(token: dict = Depends(verify_token), db: Session = Depends(get_db)) -> User:
    """
    Dependency to fetch the currently authenticated user from the database.
    """
    user_id = token.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return user

class RoleChecker:
    """
    Dependency factory to enforce role-based access control (RBAC) 
    mirroring the police hierarchical structure (e.g. CONSTABLE, SI, INSPECTOR, SHO, ACP, SP, ANALYST, ADMIN, AUDITOR).
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient permissions"
            )
        return user
