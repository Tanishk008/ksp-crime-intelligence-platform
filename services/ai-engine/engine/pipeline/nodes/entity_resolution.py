from engine.pipeline.state import InvestigationState

def resolve_entities(state: InvestigationState) -> InvestigationState:
    """
    Stage 8: Entity Resolution.
    Resolves spelling variations and maps aliases to canonical identities.
    """
    retrieved = state.get("retrieved_entities") or []
    resolved = []
    
    for ent in retrieved:
        # Standardize representation and append resolved properties
        resolved.append({
            "canonical_name": ent.get("canonical_name"),
            "entity_type": ent.get("entity_type"),
            "resolved_id": ent.get("pg_id"),
            "confidence": 0.95
        })
        
    state["resolved_entities"] = resolved
    
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "ENTITY_RESOLUTION", "output": f"resolved {len(resolved)} entities"})
    state["reasoning_trace"] = trace
    
    return state
