from sqlalchemy import Column, String, DateTime, Text, text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base
from .user import generate_uuid

class Alert(Base):
    """
    Early warning alerts, per Phase 9 Section 4.5 & 10.1.
    """
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    alert_type = Column(String(50), nullable=False)  # HOTSPOT_THRESHOLD, PATTERN_SPIKE, EARLY_WARNING
    severity = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH
    district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    station_id = Column(String(36), ForeignKey("stations.id"), nullable=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    confidence_tier = Column(String(20), nullable=True)
    supporting_data = Column(JSON, nullable=True)  # JSONB equivalent
    acknowledged_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    district = relationship("District")
    station = relationship("Station")
    acknowledged_user = relationship("User", foreign_keys=[acknowledged_by])

