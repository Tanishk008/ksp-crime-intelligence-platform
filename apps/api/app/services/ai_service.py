import os
import httpx
from typing import Dict, Any

# In a deployed Catalyst environment, this would point to the AI Engine AppSail URL
AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://localhost:8001/api/v1/reason")

async def get_ai_reasoning(query: str, case_id: str, language: str = "en") -> Dict[str, Any]:
    """
    Calls the AI Engine to process a reasoning query.
    """
    payload = {
        "query": query,
        "case_id": case_id,
        "language": language
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AI_ENGINE_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            print(f"Error calling AI Engine: {exc}")
            return {
                "status": "error",
                "confidence": "●○○○○",
                "response": "Could not connect to the AI Reasoning service.",
                "sources": [],
                "error_details": str(exc)
            }
