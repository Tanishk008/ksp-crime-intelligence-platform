from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.search_service import SearchService
from app.schemas.search import SearchResponse, SimilarCaseResponse
from app.schemas.common import StandardResponse
from typing import Optional

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/", response_model=StandardResponse)
async def execute_search(
    q: str = Query(..., min_length=1),
    type: Optional[str] = Query(None, description="ENTITY or CASE"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    results = SearchService.execute_search(db, query=q, entity_type=type, page=page)
    return {"status": "success", "data": results}

@router.get("/similar", response_model=StandardResponse)
async def find_similar_cases(
    case_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    results = SearchService.find_similar_cases(db, case_id=case_id)
    return {"status": "success", "data": results}
