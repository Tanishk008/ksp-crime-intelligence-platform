from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash
from typing import Optional, List

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_badge(db: Session, badge_number: str) -> Optional[User]:
        return db.query(User).filter(User.badge_number == badge_number).first()

    @staticmethod
    def authenticate_user(db: Session, badge_number: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_badge(db, badge_number)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            badge_number=user_in.badge_number,
            full_name=user_in.full_name,
            role=user_in.role,
            rank=user_in.rank,
            station_id=user_in.station_id,
            district_id=user_in.district_id,
            password_hash=hashed_password,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: str, user_in: UserUpdate) -> Optional[User]:
        db_user = UserService.get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
