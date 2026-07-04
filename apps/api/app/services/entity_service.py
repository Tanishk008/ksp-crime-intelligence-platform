from sqlalchemy.orm import Session
from app.models.entity import Entity, EntityAlias, CaseEntityLink
from app.models.case import Case
from typing import List, Optional, Dict, Any

class EntityService:
    @staticmethod
    def get_entity(db: Session, entity_id: str) -> Optional[Entity]:
        return db.query(Entity).filter(Entity.id == entity_id).first()

    @staticmethod
    def get_entity_profile(db: Session, entity_id: str) -> Optional[Dict[str, Any]]:
        entity = EntityService.get_entity(db, entity_id)
        if not entity:
            return None
        aliases = db.query(EntityAlias).filter(EntityAlias.entity_id == entity_id).all()
        return {
            "entity": entity,
            "aliases": aliases
        }

    @staticmethod
    def get_entity_cases(db: Session, entity_id: str) -> List[Case]:
        links = db.query(CaseEntityLink).filter(CaseEntityLink.entity_id == entity_id).all()
        case_ids = [link.case_id for link in links]
        if not case_ids:
            return []
        return db.query(Case).filter(Case.id.in_(case_ids)).all()

    @staticmethod
    def search_entities(db: Session, query: str) -> List[Entity]:
        return db.query(Entity).filter(Entity.canonical_name.ilike(f"%{query}%")).all()

    @staticmethod
    def resolve_entities(db: Session, query: str) -> Dict[str, Any]:
        """
        Gathers resolution candidates from SQL indices.
        """
        candidates = []
        aliases = db.query(EntityAlias).filter(EntityAlias.alias_text.ilike(f"%{query}%")).all()
        entity_ids = set()
        
        for alias in aliases:
            if alias.entity_id not in entity_ids:
                entity_ids.add(alias.entity_id)
                entity = EntityService.get_entity(db, alias.entity_id)
                if entity:
                    candidates.append({
                        "entity_id": entity.id,
                        "canonical_name": entity.canonical_name,
                        "entity_type": entity.entity_type,
                        "alias_matched": alias.alias_text,
                        "confidence": float(alias.confidence) if alias.confidence else 0.5
                    })
                    
        confidence = max([c["confidence"] for c in candidates]) if candidates else 0.0
        return {
            "candidates": candidates,
            "confidence": confidence
        }

    @staticmethod
    def get_entity_network(db: Session, entity_id: str) -> Dict[str, Any]:
        """
        Generates abstract ego network structure of depth 2.
        """
        entity = EntityService.get_entity(db, entity_id)
        if not entity:
            return {"nodes": [], "edges": []}
            
        nodes = [
            {
                "data": {
                    "id": entity_id,
                    "label": entity.canonical_name,
                    "type": entity.entity_type
                }
            }
        ]
        edges = []
        
        # Level 1: Find connected cases
        links = db.query(CaseEntityLink).filter(CaseEntityLink.entity_id == entity_id).all()
        for link in links:
            case = db.query(Case).filter(Case.id == link.case_id).first()
            if case:
                nodes.append({
                    "data": {
                        "id": case.id,
                        "label": case.case_number,
                        "type": "CASE"
                    }
                })
                edges.append({
                    "data": {
                        "id": f"edge-{entity_id[:4]}-{case.id[:4]}",
                        "source": entity_id,
                        "target": case.id,
                        "label": link.role
                    }
                })
                
                # Level 2: Find other entities in those same cases
                other_links = db.query(CaseEntityLink).filter(
                    CaseEntityLink.case_id == case.id,
                    CaseEntityLink.entity_id != entity_id
                ).limit(5).all()
                for o_link in other_links:
                    other_entity = EntityService.get_entity(db, o_link.entity_id)
                    if other_entity:
                        other_node_id = other_entity.id
                        if not any(n["data"]["id"] == other_node_id for n in nodes):
                            nodes.append({
                                "data": {
                                    "id": other_node_id,
                                    "label": other_entity.canonical_name,
                                    "type": other_entity.entity_type
                                }
                            })
                        edges.append({
                            "data": {
                                "id": f"edge-{case.id[:4]}-{other_node_id[:4]}",
                                "source": case.id,
                                "target": other_node_id,
                                "label": o_link.role
                            }
                        })
                        
        return {"nodes": nodes, "edges": edges}

