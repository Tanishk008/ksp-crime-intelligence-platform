from engine.pipeline.state import InvestigationState, ConfidenceTier

def assess_confidence(state: InvestigationState) -> InvestigationState:
    """
    Stage 15: Confidence Assessment (Weakest-link principle).
    Calculates final calibrated confidence tier.
    """
    # Downstream confidence cannot exceed the weakest link in evidence validation
    validation = state.get("evidence_validation_results") or {}
    has_conflict = validation.get("conflict_surfaced", False)
    
    if has_conflict:
        # Conflicts downgrade the confidence tier
        state["confidence_tier"] = ConfidenceTier.MODERATE
    else:
        state["confidence_tier"] = ConfidenceTier.HIGH
        
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "CONFIDENCE_ASSESSMENT", "output": f"tier resolved: {state['confidence_tier']}"})
    state["reasoning_trace"] = trace
    
    return state
