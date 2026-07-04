from sqlalchemy.orm import Session
from app.models.audit import AuditEvent
from datetime import datetime
from typing import List, Optional, Any

class AuditService:
    @staticmethod
    def get_audit_event(db: Session, event_id: str) -> Optional[AuditEvent]:
        return db.query(AuditEvent).filter(AuditEvent.id == event_id).first()

    @staticmethod
    def list_audit_events(
        db: Session,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditEvent]:
        query = db.query(AuditEvent)
        if user_id:
            query = query.filter(AuditEvent.user_id == user_id)
        if event_type:
            query = query.filter(AuditEvent.event_type == event_type)
        if date_from:
            query = query.filter(AuditEvent.created_at >= date_from)
        if date_to:
            query = query.filter(AuditEvent.created_at <= date_to)
            
        return query.order_by(AuditEvent.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_audit_event(
        db: Session,
        event_type: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        event_content: Optional[str] = None,
        sources_cited: Optional[Any] = None,
        confidence_tier: Optional[str] = None,
        metadata: Optional[Any] = None
    ) -> AuditEvent:
        """
        Creates and persists an immutable audit event in the database, per Phase 9 spec §4.5.
        """
        event = AuditEvent(
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            event_content=event_content,
            sources_cited=sources_cited,
            confidence_tier=confidence_tier,
            event_metadata=metadata
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        return event
