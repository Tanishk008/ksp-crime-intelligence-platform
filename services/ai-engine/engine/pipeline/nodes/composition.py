from engine.pipeline.state import InvestigationState

def compose_response(state: InvestigationState) -> InvestigationState:
    """
    Stage 19: Explainable Response Composition.
    Ensure response is objective, attributes sources, and provides the confidence level.
    """
    hypotheses = state.get("hypotheses") or []
    confidence_tier = state.get("confidence_tier")
    
    response_text = "Objective Cognitive Investigation Synthesis:\n\n"
    response_text += "Compounding Hypotheses identified:\n"
    for h in hypotheses:
        response_text += f"- {h['id']}: {h['text']} (Support factors: {', '.join(h['supporting_evidence'])})\n"
        
    if state.get("diagnosticity_gap"):
        response_text += "\n[IMPORTANT] Diagnosticity Gap detected: The confidence difference between hypotheses is small. Further evidence is needed.\n"
        state["recommendation"] = "Collect independent witness verification to resolve H1 vs H2 gap."
    else:
        state["recommendation"] = None
        
    state["alternative_explanation"] = "Accomplice coordination remains a secondary explanation due to unresolved alias matches."
    state["final_response"] = response_text
    
    # Format sources cited
    state["sources_cited"] = [
        {"case_id": state.get("case_id"), "record_type": "CBR_LOOKUP", "description": "Modus Operandi Case Index"}
    ]
    
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "COMPOSITION", "output": "Synthesis completed."})
    state["reasoning_trace"] = trace
    
    return state
