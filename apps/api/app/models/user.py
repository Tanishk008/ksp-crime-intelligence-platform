import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship
from .base import Base

def generate_uuid():
    return str(uuid.uuid4())

class District(Base):
    __tablename__ = "districts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    
    stations = relationship("Station", back_populates="district")

class Station(Base):
    __tablename__ = "stations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    district_id = Column(String(36), ForeignKey("districts.id"))
    
    # Point type not directly supported without GeoAlchemy2, using String for WKT for now.
    location = Column(String(255)) 

    district = relationship("District", back_populates="stations")
    users = relationship("User", back_populates="station")
    cases = relationship("Case", back_populates="station")

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    badge_number = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)
    rank = Column(String(50))
    station_id = Column(String(36), ForeignKey("stations.id"))
    district_id = Column(String(36), ForeignKey("districts.id"))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_login = Column(DateTime, nullable=True)

    station = relationship("Station", back_populates="users")
