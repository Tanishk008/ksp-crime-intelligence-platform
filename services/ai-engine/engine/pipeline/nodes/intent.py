from engine.pipeline.state import InvestigationState

def classify_intent(state: InvestigationState) -> InvestigationState:
    """
    Stage 1: Intent Understanding.
    Classifies the user query as 'retrieval' (simple lookup) or 'reasoning' (complex pattern matching).
    """
    query = state.get("query", "")
    if any(word in query.lower() for word in ["why", "how", "analyze", "explain", "possibility", "conflict", "contradict"]):
        state["intent"] = "reasoning"
    else:
        state["intent"] = "retrieval"
        
    state["investigation_goal"] = "Assess behavioral linkages or entity profiles."
    state["information_needs"] = ["Semantic case contexts", "Known alias matching", "Spatial temporal events"]
    
    # Append trace
    trace = state.get("reasoning_trace") or []
    trace.append({"stage": "INTENT", "output": f"classified as: {state['intent']}"})
    state["reasoning_trace"] = trace
    
    return state
