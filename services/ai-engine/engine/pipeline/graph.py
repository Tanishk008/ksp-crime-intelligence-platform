from langgraph.graph import StateGraph, END
from engine.pipeline.state import InvestigationState
from engine.pipeline.nodes.intent import classify_intent
from engine.pipeline.nodes.context import recover_context
from engine.pipeline.nodes.retrieval import retrieve_evidence
from engine.pipeline.nodes.entity_resolution import resolve_entities
from engine.pipeline.nodes.hypothesis import generate_hypotheses
from engine.pipeline.nodes.evaluation import evaluate_evidence
from engine.pipeline.nodes.confidence import assess_confidence
from engine.pipeline.nodes.composition import compose_response

def build_graph():
    workflow = StateGraph(InvestigationState)
    
    # Register all 8 main pipeline nodes
    workflow.add_node("intent", classify_intent)
    workflow.add_node("context", recover_context)
    workflow.add_node("retrieval", retrieve_evidence)
    workflow.add_node("entity_resolution", resolve_entities)
    workflow.add_node("hypothesis", generate_hypotheses)
    workflow.add_node("evaluation", evaluate_evidence)
    workflow.add_node("confidence", assess_confidence)
    workflow.add_node("composition", compose_response)
    
    workflow.set_entry_point("intent")
    
    # Intent links directly to context recovery
    workflow.add_edge("intent", "context")
    workflow.add_edge("context", "retrieval")
    workflow.add_edge("retrieval", "entity_resolution")
    
    # Conditional routing based on classification intent
    def route_by_intent(state: InvestigationState):
        if state.get("intent") == "reasoning":
            return "hypothesis"
        return "composition"
        
    workflow.add_conditional_edges(
        "entity_resolution",
        route_by_intent,
        {
            "hypothesis": "hypothesis",
            "composition": "composition"
        }
    )
    
    # Reasoning track execution sequence
    workflow.add_edge("hypothesis", "evaluation")
    workflow.add_edge("evaluation", "confidence")
    workflow.add_edge("confidence", "composition")
    
    workflow.add_edge("composition", END)
    
    return workflow.compile()

