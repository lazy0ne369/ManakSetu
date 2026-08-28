from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.repositories.query_log_repo import QueryLogRepository

router = APIRouter(prefix="/api/history", tags=["Conversation History"])


@router.get(
    "",
    summary="Get conversation and query history logs",
)
def get_query_history(
    session_id: Optional[str] = Query(None, description="Optional session ID filter"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    repo = QueryLogRepository(db)
    logs = repo.get_history(limit=limit, session_id=session_id)
    return [
        {
            "id": l.id,
            "session_id": l.session_id,
            "user_query": l.user_query,
            "role_type": l.role_type,
            "intent": l.intent,
            "confidence": l.confidence,
            "needs_clarification": l.needs_clarification,
            "clarification_question": l.clarification_question,
            "citations": l.citations,
            "execution_time_ms": l.execution_time_ms,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }
        for l in logs
    ]
