from sqlalchemy import Column, String, DateTime, Text, text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user import generate_uuid

class AuditEvent(Base):
    """
    Immutable event store for audit logging, per Phase 9 Section 4.5 & 7.3.
    """
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(50), nullable=False)  # QUERY, RESPONSE, OVERRIDE, BOUNDARY_VIOLATION_FLAG, ACCESS_DENIED
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=True)
    event_content = Column(Text, nullable=True)
    sources_cited = Column(JSON, nullable=True)  # JSONB equivalent
    confidence_tier = Column(String(20), nullable=True)  # VERY_HIGH, HIGH, etc.
    event_metadata = Column("metadata", JSON, nullable=True)  # JSONB equivalent for audit metadata, mapped to 'metadata' column to avoid reservation conflict
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User")

