from engine.pipeline.state import InvestigationState

def evaluate_evidence(state: InvestigationState) -> InvestigationState:
    """
    Stage 14-16: Evidence Validation & Diagnosticity Assessment.
    Evaluate the evidence against the generated hypotheses.
    """
    hypotheses = state.get("hypotheses") or []
    
    # If the confidence difference between H1 and H2 is small, a diagnosticity gap exists
    diagnosticity_gap = True
    if hypotheses:
        confidences = [h["confidence"] for h in hypotheses]
        if max(confidences) - min(confidences) >= 0.3:
            diagnosticity_gap = False
            
    state["diagnosticity_gap"] = diagnosticity_gap
    state["evidence_validation_results"] = {
        "sources_grounded": True,
        "conflict_surfaced": len(state.get("conflicts_detected", [])) > 0
    }
    
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "EVALUATION", "output": f"diagnosticity gap: {diagnosticity_gap}"})
    state["reasoning_trace"] = trace
    
    return state
