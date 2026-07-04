from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models.case import Case
from app.schemas.common import StandardResponse
from typing import Optional

router = APIRouter(prefix="/map", tags=["map"])

@router.get("/hotspots", response_model=StandardResponse)
async def get_hotspots(
    district: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    cases = db.query(Case).all()
    hotspots = []
    for c in cases:
        if c.incident_location:
            hotspots.append({
                "lat": 12.9716,  # Mock coordinate in Karnataka bounds
                "lng": 77.5946,
                "intensity": 0.8
            })
    return {"status": "success", "data": hotspots}

@router.get("/incidents", response_model=StandardResponse)
async def get_incidents(
    bounds: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    cases = db.query(Case).all()
    incidents = []
    for c in cases:
        incidents.append({
            "id": c.id,
            "case_number": c.case_number,
            "type": c.case_type,
            "lat": 12.9716,
            "lng": 77.5946,
            "status": c.status
        })
    return {"status": "success", "data": incidents}

