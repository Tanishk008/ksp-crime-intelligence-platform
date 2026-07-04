def check_exclusions(query: str, response: str) -> str:
    """
    Enforces the hard exclusions defined in the KSP Blueprint:
    1. No person-level predictive risk scoring.
    2. No narrative offender profiling.
    3. No demographic-correlated suspicion.
    """
    # Simple keyword-based scaffolding for the governance layer
    forbidden_terms = [
        "risk score", 
        "probability of reoffending", 
        "predictive risk", 
        "caste", 
        "religion",
        "community identity"
    ]
    
    query_lower = query.lower()
    response_lower = response.lower()
    
    for term in forbidden_terms:
        if term in query_lower or term in response_lower:
            return f"VIOLATION_DETECTED: {term}"
            
    return "CLEAN"
