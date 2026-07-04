import pytest
from app.governance.confidence import annotate_confidence, get_confidence_display

def test_confidence_translation():
    assert get_confidence_display(0.95) == "●●●●●"
    assert get_confidence_display(0.75) == "●●●●○"
    assert get_confidence_display(0.55) == "●●●○○"
    assert get_confidence_display(0.35) == "●●○○○"
    assert get_confidence_display(0.15) == "●○○○○"

def test_response_confidence_annotation():
    response = {
        "status": "success",
        "role": "ASSISTANT",
        "confidence_score": 0.85
    }
    
    annotated = annotate_confidence(response)
    assert annotated["confidence_dots"] == "●●●●○"

    # Default mapping when tier is specified
    response_tier = {
        "status": "success",
        "role": "ASSISTANT",
        "confidence_tier": "VERY_HIGH"
    }
    annotated_tier = annotate_confidence(response_tier)
    assert annotated_tier["confidence_dots"] == "●●●●●"
