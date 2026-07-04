from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IRAGService(ABC):
    """
    Contract interface for the RAG retrieval pipeline, per RAG CONTRACT requirements.
    This architecture isolates AI reasoning orchestration from specific vector or graph databases.
    """
    
    @abstractmethod
    def retrieve(self, query: str, case_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Generic retrieval of raw semantic blocks.
        """
        pass

    @abstractmethod
    def retrieve_context(self, query: str, case_id: Optional[str] = None) -> str:
        """
        Retrieves context as a compiled formatted string ready for LLM consumption.
        """
        pass

    @abstractmethod
    def retrieve_entities(self, query: str, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves graph/semantic entities related to the query.
        """
        pass

    @abstractmethod
    def retrieve_documents(self, query: str, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves CCTNS case file details or unstructured document chunks.
        """
        pass


class PlaceholderRAGService(IRAGService):
    """
    Placeholder implementation of IRAGService to isolate reasoning testing
    until the separate RAG engineering track completes implementation.
    """
    
    def retrieve(self, query: str, case_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        return [
            {
                "id": "doc-placeholder-1",
                "text": "First Information Report filed at station regarding theft.",
                "score": 0.89,
                "metadata": {"case_id": case_id, "record_type": "FIR"}
            }
        ]

    def retrieve_context(self, query: str, case_id: Optional[str] = None) -> str:
        return "PLACEHOLDER RETRIEVED CONTEXT: Relevant incident logs show suspect activity at target coordinates."

    def retrieve_entities(self, query: str, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            {
                "id": "ent-placeholder-1",
                "canonical_name": "Ramesh Kumar",
                "entity_type": "PERSON",
                "pg_id": "uuid-ramesh",
                "role": "ACCUSED"
            }
        ]

    def retrieve_documents(self, query: str, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            {
                "id": "case-file-1",
                "title": "FIR CR-2024-0012",
                "path": "fir_files/CR-2024-0012.pdf"
            }
        ]
