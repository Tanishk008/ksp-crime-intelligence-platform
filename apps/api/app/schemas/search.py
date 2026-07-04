from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SearchResultItem(BaseModel):
    id: str
    type: str  # CASE, ENTITY
    title: str
    description: Optional[str] = None
    relevance_score: float
    metadata: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total_results: int
    page: int

class SimilarCaseItem(BaseModel):
    case_id: str
    case_number: str
    similarity_score: float
    mo_factors_matched: List[str]

class SimilarCaseResponse(BaseModel):
    case_id: str
    similar_cases: List[SimilarCaseItem]
