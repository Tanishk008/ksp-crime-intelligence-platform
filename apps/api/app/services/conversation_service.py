from sqlalchemy.orm import Session
from ..models.conversation import Conversation, Message
from datetime import datetime
from typing import List, Dict, Any

class ConversationService:
    @staticmethod
    def create_conversation(db: Session, user_id: str, case_id: str = None) -> Conversation:
        conversation = Conversation(user_id=user_id, case_id=case_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(db: Session, conversation_id: str) -> Conversation:
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()

    @staticmethod
    def get_messages(db: Session, conversation_id: str) -> List[Message]:
        return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

    @staticmethod
    def add_message(
        db: Session, 
        conversation_id: str, 
        role: str, 
        content: str, 
        content_kannada: str = None,
        confidence_tier: str = None,
        sources: Any = None,
        reasoning_trace_id: str = None,
        has_conflict: bool = False
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            content_kannada=content_kannada,
            confidence_tier=confidence_tier,
            sources=sources,
            reasoning_trace_id=reasoning_trace_id,
            has_conflict=has_conflict
        )
        db.add(message)
        
        # Update conversation last activity
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.last_activity = datetime.utcnow()
            
        db.commit()
        db.refresh(message)
        return message
