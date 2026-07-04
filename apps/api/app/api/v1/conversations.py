import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.conversation_service import ConversationService
from app.services.ai_service import get_ai_reasoning
from app.schemas.conversation import (
    ConversationCreate, 
    ConversationResponse, 
    MessageCreate, 
    MessageResponse, 
    ConversationDetailResponse
)
from app.schemas.common import StandardResponse
from app.models.user import User

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=StandardResponse)
async def create_conversation(
    request: ConversationCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    conversation = ConversationService.create_conversation(db, user_id=user.id, case_id=request.case_id)
    return {
        "status": "success", 
        "data": ConversationResponse.from_attributes(conversation)
    }

@router.get("/", response_model=StandardResponse)
async def list_conversations(
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    # Retrieve all conversations for this user
    from app.models.conversation import Conversation
    conversations = db.query(Conversation).filter(Conversation.user_id == user.id).all()
    return {
        "status": "success", 
        "data": [ConversationResponse.from_attributes(c) for c in conversations]
    }

@router.get("/{conversation_id}", response_model=StandardResponse)
async def get_conversation(
    conversation_id: str, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    conversation = ConversationService.get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = ConversationService.get_messages(db, conversation_id)
    
    return {
        "status": "success",
        "data": ConversationDetailResponse(
            conversation=ConversationResponse.from_attributes(conversation),
            messages=[MessageResponse.from_attributes(m) for m in messages]
        )
    }

@router.get("/{conversation_id}/messages", response_model=StandardResponse)
async def list_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    conversation = ConversationService.get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = ConversationService.get_messages(db, conversation_id)
    return {
        "status": "success",
        "data": [MessageResponse.from_attributes(m) for m in messages]
    }

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: str,
    request: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    conversation = ConversationService.get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 1. Save user query message to database
    ConversationService.add_message(
        db=db,
        conversation_id=conversation_id,
        role="USER",
        content=request.query
    )

    # 2. Return SSE Stream yielding reasoning progress followed by the final answer
    async def sse_event_generator():
        # Yield reasoning steps to keep investigator engaged (RPD theory / reducing cognitive load)
        steps = [
            {"stage": "INTENT", "content": "Analyzing query intent..."},
            {"stage": "RETRIEVAL", "content": "Querying local case records (CBR)..."},
            {"stage": "HYPOTHESIS", "content": "Formulating competing hypotheses..."},
            {"stage": "EVALUATION", "content": "Validating evidence and estimating confidence..."}
        ]
        for step in steps:
            yield f"data: {json.dumps(step)}\n\n"
            await asyncio.sleep(0.3)

        # Call the actual AI engine
        try:
            ai_response = await get_ai_reasoning(
                query=request.query,
                case_id=conversation.case_id,
                language=request.language
            )
            
            # Save AI response message to database
            ConversationService.add_message(
                db=db,
                conversation_id=conversation_id,
                role="ASSISTANT",
                content=ai_response.get("response", ""),
                confidence_tier=ai_response.get("confidence", "Moderate"),
                sources=ai_response.get("sources", []),
                has_conflict=ai_response.get("status") == "violation"
            )
            
            final_payload = {
                "stage": "COMPOSITION",
                "status": "success",
                "confidence": ai_response.get("confidence", "Moderate"),
                "confidence_dots": ai_response.get("confidence_dots", 3),
                "response": ai_response.get("response", ""),
                "sources": ai_response.get("sources", [])
            }
            yield f"data: {json.dumps(final_payload)}\n\n"
        except Exception as e:
            error_payload = {
                "stage": "ERROR",
                "status": "error",
                "response": f"Error running reasoning engine: {str(e)}"
            }
            yield f"data: {json.dumps(error_payload)}\n\n"

    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    conversation = ConversationService.get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    db.delete(conversation)
    db.commit()
    return


