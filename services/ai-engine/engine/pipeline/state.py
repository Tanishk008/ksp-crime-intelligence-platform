from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum

class ConfidenceTier(str, Enum):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"

class InvestigationState(TypedDict):
    # Input
    query: str
    language: str                    # "en" | "kn"
    user_id: str
    user_role: str
    case_id: Optional[str]
    conversation_id: str
    session_context: dict

    # Stage outputs
    intent: str                      # "retrieval" | "reasoning"
    investigation_goal: str
    information_needs: List[str]

    # Retrieved evidence
    retrieved_cases: List[dict]
    retrieved_entities: List[dict]
    retrieved_relationships: List[dict]
    conflicts_detected: List[dict]

    # Resolved entities
    resolved_entities: List[dict]

    # Hypotheses (always multiple)
    hypotheses: List[dict]           # [{text, supporting_evidence, disconfirming_evidence, confidence}]
    evidence_validation_results: dict
    confidence_tier: ConfidenceTier

    # Output
    alternative_explanation: Optional[str]
    recommendation: Optional[str]    # diagnosticity gap only — never verdict
    final_response: str
    sources_cited: List[dict]
    reasoning_trace: List[dict]      # All stages + their outputs

    # Governance
    boundary_check_passed: bool
    audit_event_id: Optional[str]
