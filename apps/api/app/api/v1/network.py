from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.case_service import CaseService
from app.services.entity_service import EntityService
from app.schemas.common import StandardResponse

router = APIRouter(prefix="/network", tags=["network"])

@router.get("/cases/{case_id}", response_model=StandardResponse)
async def get_case_network(
    case_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    network = CaseService.get_case_network(db, case_id)
    return {"status": "success", "data": network}

@router.get("/entities/{entity_id}", response_model=StandardResponse)
async def get_entity_network(
    entity_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    network = EntityService.get_entity_network(db, entity_id)
    return {"status": "success", "data": network}
