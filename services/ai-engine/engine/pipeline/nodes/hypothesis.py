from engine.pipeline.state import InvestigationState

def generate_hypotheses(state: InvestigationState) -> InvestigationState:
    """
    Stage 13: Multiple Hypothesis Generation.
    Generates competing explanations for the event to prevent cognitive tunnel vision bias.
    """
    hypotheses = [
        {
            "id": "H1", 
            "text": "Subject acted independently with a planned MO.", 
            "supporting_evidence": ["Weapon consistency", "No other visual tracks"],
            "disconfirming_evidence": ["Witness claims second motor vehicle heard"],
            "confidence": 0.75
        },
        {
            "id": "H2", 
            "text": "Subject acted in coordination with an accomplice.", 
            "supporting_evidence": ["Witness claims second motor vehicle heard"],
            "disconfirming_evidence": ["No accomplice matching aliases resolved"],
            "confidence": 0.40
        }
    ]
    
    state["hypotheses"] = hypotheses
    
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "HYPOTHESIS_GENERATION", "output": f"generated {len(hypotheses)} hypotheses"})
    state["reasoning_trace"] = trace
    
    return state
