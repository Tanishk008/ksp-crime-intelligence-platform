import re
from dataclasses import dataclass

EXCLUDED_FIELD_NAMES = frozenset({
    "caste", "jati", "tribe", "community", "religion", "faith",
    "gothra", "denomination", "sect", "ethnicity",
    # Kannada equivalents
    "ಜಾತಿ", "ಧರ್ಮ", "ಸಮುದಾಯ",
})

EXCLUDED_OUTPUT_PATTERNS = [
    r"risk\s+score",
    r"danger\s+rating",
    r"threat\s+level\s+\d",
    r"probability\s+of\s+recidivism",
    r"likely\s+to\s+(re)?offend",
]

EXCLUDED_INPUT_PHRASES = [
    "which caste", "which religion", "which community",
    "ಯಾವ ಜಾತಿ", "ಯಾವ ಧರ್ಮ",
    "risk score for", "danger level of",
]

@dataclass
class ViolationResult:
    detected: bool
    severity: str   # "NONE" | "LOW" | "HIGH"
    matched_pattern: str | None

def check_boundary_violations(response_data: dict) -> ViolationResult:
    """
    Checks a response dict for excluded category content.
    HIGH severity = suppress response immediately.
    LOW severity = flag for review, allow through.
    """
    response_text = str(response_data).lower()

    for pattern in EXCLUDED_OUTPUT_PATTERNS:
        if re.search(pattern, response_text, re.IGNORECASE):
            return ViolationResult(True, "HIGH", pattern)

    for field in EXCLUDED_FIELD_NAMES:
        if field in response_text:
            return ViolationResult(True, "LOW", field)

    return ViolationResult(False, "NONE", None)

def check_input_boundary(query: str) -> ViolationResult:
    """
    Checks an incoming query for excluded category requests.
    Called before the query enters the AI pipeline.
    """
    query_lower = query.lower()
    for phrase in EXCLUDED_INPUT_PHRASES:
        if phrase in query_lower:
            return ViolationResult(True, "HIGH", phrase)
    return ViolationResult(False, "NONE", None)
