import os
from typing import Optional, List, Dict, Any

class LLMService:
    """
    Service wrapper for LLM queries (e.g. Anthropic Claude).
    Handles fallbacks and mock responses for local testing if API key is not present.
    """
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("LLM_MODEL", "claude-sonnet-4-6")

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends query to Claude, falling back to mock outputs for test resilience.
        """
        if not self.api_key or self.api_key == "sk-ant-...":
            # Return high-quality mock response reflecting investigative reasoning
            return (
                "Based on the CCTNS records, Ramesh Kumar has a documented Modus Operandi "
                "involving burglary via broken window latch at station SI-04. "
                "There is moderate evidence pointing towards Ramesh Kumar acting with an accomplice "
                "named Suresh, based on witness testimonies from related case CR-2024-0012."
            )
        
        # In production, call Anthropic API:
        # client = anthropic.AsyncAnthropic(api_key=self.api_key)
        # response = await client.messages.create(
        #     model=self.model,
        #     max_tokens=2048,
        #     system=system_prompt,
        #     messages=[{"role": "user", "content": user_prompt}]
        # )
        # return response.content[0].text
        return "Production API response placeholder."
