from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.entity import CaseEntityLink, Entity
from typing import List, Optional, Dict, Any

class CaseService:
    @staticmethod
    def get_case(db: Session, case_id: str) -> Optional[Case]:
        return db.query(Case).filter(Case.id == case_id).first()

    @staticmethod
    def list_active_cases(db: Session, skip: int = 0, limit: int = 100, station_id: str = None) -> List[Case]:
        query = db.query(Case).filter(Case.status == "ACTIVE")
        if station_id:
            query = query.filter(Case.station_id == station_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_case_entities(db: Session, case_id: str) -> List[Dict[str, Any]]:
        """
        Gets list of entities linked to a case.
        """
        links = db.query(CaseEntityLink).filter(CaseEntityLink.case_id == case_id).all()
        results = []
        for link in links:
            entity = db.query(Entity).filter(Entity.id == link.entity_id).first()
            if entity:
                results.append({
                    "id": entity.id,
                    "canonical_name": entity.canonical_name,
                    "entity_type": entity.entity_type,
                    "role": link.role,
                    "confidence": float(link.confidence) if link.confidence else 1.0
                })
        return results

    @staticmethod
    def get_case_timeline(db: Session, case_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves ordered timeline events for a case.
        """
        case = CaseService.get_case(db, case_id)
        if not case:
            return []
        
        return [
            {
                "id": f"evt-{case_id[:8]}-1",
                "case_id": case_id,
                "event_type": "FIRST_INFORMATION_REPORT",
                "description": f"FIR filed for {case.case_type} at station {case.station_id or 'unknown'}",
                "event_date": case.created_at,
                "has_conflict": False
            },
            {
                "id": f"evt-{case_id[:8]}-2",
                "case_id": case_id,
                "event_type": "INCIDENT_REPORTED",
                "description": f"Incident occurred at {case.incident_address or 'incident location'}",
                "event_date": case.incident_date if case.incident_date else case.created_at,
                "has_conflict": False
            }
        ]

    @staticmethod
    def get_case_network(db: Session, case_id: str) -> Dict[str, Any]:
        """
        Returns a cytoscape-compatible network graph from Neo4j/Relational DB.
        """
        entities = CaseService.get_case_entities(db, case_id)
        
        nodes = [
            {
                "data": {
                    "id": case_id,
                    "label": f"Case {case_id[:8]}",
                    "type": "CASE"
                }
            }
        ]
        edges = []
        
        for ent in entities:
            nodes.append({
                "data": {
                    "id": ent["id"],
                    "label": ent["canonical_name"],
                    "type": ent["entity_type"]
                }
            })
            edges.append({
                "data": {
                    "id": f"edge-{case_id[:4]}-{ent['id'][:4]}",
                    "source": ent["id"],
                    "target": case_id,
                    "label": ent["role"]
                }
            })
            
        return {"nodes": nodes, "edges": edges}

