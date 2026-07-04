def get_confidence_display(score: float) -> str:
    """
    Translates a 0.0 to 1.0 confidence score into the mandated 5-dot scale.
    ●●●●● = Very High
    ●●●●○ = High
    ●●●○○ = Moderate
    ●●○○○ = Low
    ●○○○○ = Very Low
    """
    if score >= 0.9:
        return "●●●●●"
    elif score >= 0.7:
        return "●●●●○"
    elif score >= 0.5:
        return "●●●○○"
    elif score >= 0.3:
        return "●●○○○"
    else:
        return "●○○○○"

def annotate_confidence(response_data: dict) -> dict:
    """
    Ensures every AI response has the correct confidence annotation schema.
    If the response already contains confidence, we translate or format it.
    If not, we default to Moderate.
    """
    if "data" in response_data:
        data = response_data["data"]
        # Recursively annotate lists or dicts of messages
        if isinstance(data, dict):
            _annotate_item(data)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    _annotate_item(item)
    else:
        _annotate_item(response_data)
        
    return response_data

def _annotate_item(item: dict):
    if "role" in item and item["role"] == "ASSISTANT":
        # Calculate or default the dots representation
        score = item.get("confidence_score")
        if score is not None:
            item["confidence_dots"] = get_confidence_display(float(score))
        elif "confidence_tier" in item and item["confidence_tier"]:
            # Map tier string to dots
            tier_map = {
                "VERY_HIGH": "●●●●●",
                "HIGH": "●●●●○",
                "MODERATE": "●●●○○",
                "LOW": "●●○○○",
                "VERY_LOW": "●○○○○"
            }
            item["confidence_dots"] = tier_map.get(item["confidence_tier"], "●●●○○")
        else:
            # Mandated default if not specified
            item["confidence_tier"] = "MODERATE"
            item["confidence_dots"] = "●●●○○"
