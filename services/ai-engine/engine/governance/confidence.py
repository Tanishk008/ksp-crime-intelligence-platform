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
        return "●●●●●" # Very High
    elif score >= 0.7:
        return "●●●●○" # High
    elif score >= 0.5:
        return "●●●○○" # Moderate
    elif score >= 0.3:
        return "●●○○○" # Low
    else:
        return "●○○○○" # Very Low
