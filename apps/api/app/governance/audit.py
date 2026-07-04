from fastapi import Request
from app.core.database import SessionLocal
from app.services.audit_service import AuditService
from typing import Optional, Any

async def emit_audit_event(
    event_type: str,
    request: Request,
    content: str,
    request_audit_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None
) -> str:
    """
    Constructs and persists an AuditEvent in the relational audit log table.
    Ensures structural logging of query actions and responses.
    """
    db = SessionLocal()
    try:
        metadata = {
            "client_host": request.client.host if request.client else "unknown",
            "url_path": request.url.path,
            "method": request.method,
            "request_audit_id_link": request_audit_id
        }
        
        event = AuditService.create_audit_event(
            db=db,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            event_content=content,
            metadata=metadata
        )
        return event.id
    except Exception as e:
        print(f"Error emitting audit event: {e}")
        return ""
    finally:
        db.close()
