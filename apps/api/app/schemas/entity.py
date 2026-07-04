from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class EntityBase(BaseModel):
    canonical_name: str
    entity_type: str  # PERSON, VEHICLE, ORGANIZATION, PHONE, LOCATION
    neo4j_node_id: Optional[str] = None

class EntityCreate(EntityBase):
    pass

class EntityAliasResponse(BaseModel):
    id: str
    entity_id: str
    alias_text: str
    script: Optional[str] = None
    source_case_id: Optional[str] = None
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True

class EntityResponse(EntityBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EntityDetailResponse(EntityResponse):
    aliases: List[EntityAliasResponse] = []
    case_links: List[Dict[str, Any]] = []
    relationships: List[Dict[str, Any]] = []

class EntityResolutionResult(BaseModel):
    candidates: List[Dict[str, Any]]
    confidence: float
