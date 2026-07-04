from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.entity import Entity
from app.schemas.search import SearchResponse, SearchResultItem, SimilarCaseResponse, SimilarCaseItem
from typing import List, Optional

class SearchService:
    @staticmethod
    def execute_search(
        db: Session, 
        query: str, 
        entity_type: Optional[str] = None, 
        page: int = 1,
        limit: int = 20
    ) -> SearchResponse:
        """
        Executes a multi-index database search over cases and entities.
        """
        offset = (page - 1) * limit
        results = []
        
        # 1. Search cases
        cases = db.query(Case).filter(
            Case.case_number.ilike(f"%{query}%") |
            Case.case_type.ilike(f"%{query}%") |
            Case.narrative.ilike(f"%{query}%")
        ).offset(offset).limit(limit // 2).all()
        
        for case in cases:
            results.append(SearchResultItem(
                id=case.id,
                type="CASE",
                title=f"Case {case.case_number}",
                description=case.case_type,
                relevance_score=0.9,
                metadata={"case_number": case.case_number, "status": case.status}
            ))

        # 2. Search entities
        entity_query = db.query(Entity).filter(Entity.canonical_name.ilike(f"%{query}%"))
        if entity_type:
            entity_query = entity_query.filter(Entity.entity_type == entity_type)
        entities = entity_query.offset(offset).limit(limit // 2).all()
        
        for entity in entities:
            results.append(SearchResultItem(
                id=entity.id,
                type="ENTITY",
                title=entity.canonical_name,
                description=entity.entity_type,
                relevance_score=0.8,
                metadata={"entity_type": entity.entity_type}
            ))
            
        return SearchResponse(
            query=query,
            results=results,
            total_results=len(results),
            page=page
        )

    @staticmethod
    def find_similar_cases(db: Session, case_id: str) -> SimilarCaseResponse:
        """
        Calculates MO (Modus Operandi) similarity matching.
        This provides a clear interface for the future statistical similarity engine.
        """
        # Fetch the baseline case
        base_case = db.query(Case).filter(Case.id == case_id).first()
        if not base_case:
            return SimilarCaseResponse(case_id=case_id, similar_cases=[])
            
        # Find cases of the same type to simulate similarity comparison
        other_cases = db.query(Case).filter(
            Case.id != case_id,
            Case.case_type == base_case.case_type
        ).limit(3).all()
        
        similar_items = []
        for i, other in enumerate(other_cases):
            similar_items.append(SimilarCaseItem(
                case_id=other.id,
                case_number=other.case_number,
                similarity_score=0.85 - (i * 0.05),
                mo_factors_matched=["Weapon selection", "Target classification", "Access mechanism"]
            ))
            
        return SimilarCaseResponse(
            case_id=case_id,
            similar_cases=similar_items
        )
