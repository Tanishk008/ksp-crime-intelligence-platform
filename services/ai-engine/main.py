from fastapi import FastAPI
from pydantic import BaseModel
import os
from engine.pipeline.graph import build_graph

app = FastAPI(
    title="KSP AI Engine", 
    description="LangGraph pipeline on Catalyst AppSail"
)

class QueryRequest(BaseModel):
    query: str
    case_id: str = None
    language: str = "en"

# Initialize graph once at startup
reasoning_graph = build_graph()

@app.post("/api/v1/reason")
async def reason_query(request: QueryRequest):
    # Prepare the initial state
    initial_state = {
        "query": request.query,
        "case_id": request.case_id,
        "language": request.language,
        "intent": None,
        "evidence": [],
        "hypotheses": [],
        "diagnosticity_gap": None,
        "confidence_score": 1,
        "final_response": None
    }
    
    # Run the compiled StateGraph
    try:
        final_state = await reasoning_graph.ainvoke(initial_state)
        response_data = final_state.get("final_response", {})
        
        # Enforce governance substrate verification
        from engine.governance.exclusion_filter import check_exclusions
        check_res = check_exclusions(request.query, response_data.get("text", ""))
        if check_res.startswith("VIOLATION_DETECTED"):
            return {
                "status": "violation",
                "confidence": "●○○○○",
                "response": "This query or generated response violates platform governance guidelines.",
                "sources": []
            }
            
        return {
            "status": "success",
            "confidence": response_data.get("confidence", "Moderate"),
            "confidence_dots": response_data.get("confidence_dots", 3),
            "response": response_data.get("text", ""),
            "sources": []
        }
    except Exception as e:
        return {
            "status": "error",
            "confidence": "●○○○○",
            "response": f"AI Engine pipeline error: {str(e)}",
            "sources": []
        }

@app.get("/health")
def health():
    return {"status": "ai-engine is running on Catalyst"}

if __name__ == "__main__":
    import uvicorn
    # Catalyst AppSail typically sets X-ZOHO-CATALYST-PORT
    port = int(os.environ.get("X_ZOHO_CATALYST_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
