from engine.pipeline.state import InvestigationState

def recover_context(state: InvestigationState) -> InvestigationState:
    """
    Stage 3: Context Recovery.
    Restores the case context and active session details.
    """
    case_id = state.get("case_id")
    session_context = state.get("session_context") or {}
    
    # Simulate retrieving case contextual meta from SQL context store
    if case_id:
        session_context["active_case_details"] = {
            "id": case_id,
            "incident_bounds": "Karnataka",
            "scope": "Station"
        }
        
    state["session_context"] = session_context
    
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "CONTEXT_RECOVERY", "output": f"recovered for case: {case_id}"})
    state["reasoning_trace"] = trace
    
    return state
