import pytest
from app.governance.boundary_check import check_input_boundary, check_boundary_violations

def test_input_boundary_violation():
    # Restricted input queries
    violation_caste = check_input_boundary("which caste is the suspect?")
    assert violation_caste.detected
    assert violation_caste.severity == "HIGH"
    
    violation_religion = check_input_boundary("ಯಾವ ಧರ್ಮ (what religion) details?")
    assert violation_religion.detected
    assert violation_religion.severity == "HIGH"
    
    # Safe query
    safe = check_input_boundary("list cases matching theft narrative")
    assert not safe.detected
    assert safe.severity == "NONE"

def test_output_boundary_violation():
    # Restricted output patterns
    violation_score = check_boundary_violations({"response": "The risk score for recidivism is 90%"})
    assert violation_score.detected
    assert violation_score.severity == "HIGH"
    
    # Low-severity field check (flagged but let through)
    violation_low = check_boundary_violations({"name": "Ramesh", "caste": "unknown"})
    assert violation_low.detected
    assert violation_low.severity == "LOW"
    
    # Safe output
    safe = check_boundary_violations({"status": "success", "response": "Ramesh Kumar was present at coordinate lat/lng."})
    assert not safe.detected
    assert safe.severity == "NONE"
