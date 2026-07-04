from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, text
from sqlalchemy.orm import relationship
from .base import Base
from .user import generate_uuid

class Report(Base):
    """
    Generated reports, per Phase 9 Section 4.5.
    """
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=True)
    title = Column(String(300), nullable=False)
    content_json = Column(JSON, nullable=True)  # JSONB equivalent for structured content
    pdf_path = Column(String(500), nullable=True)  # Path in Zoho Catalyst File Store
    status = Column(String(20), default="DRAFT")  # DRAFT, GENERATED
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    creator = relationship("User")
    case = relationship("Case")
