from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.database.models import QueryLog, Session as DbSession, Feedback


class QueryLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, title: str = "New Conversation", user_id: Optional[str] = None) -> DbSession:
        session = DbSession(title=title, user_id=user_id)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def log_query(
        self,
        user_query: str,
        role_type: str = "consumer",
        intent: Optional[str] = None,
        parsed_entities: Optional[Dict[str, Any]] = None,
        raw_response: Optional[Dict[str, Any]] = None,
        confidence: str = "MEDIUM",
        needs_clarification: bool = False,
        clarification_question: Optional[str] = None,
        citations: Optional[List[Dict[str, Any]]] = None,
        execution_time_ms: Optional[int] = None,
        session_id: Optional[str] = None,
    ) -> QueryLog:
        log = QueryLog(
            session_id=session_id,
            user_query=user_query,
            role_type=role_type,
            intent=intent,
            parsed_entities=parsed_entities,
            raw_response=raw_response,
            confidence=confidence,
            needs_clarification=needs_clarification,
            clarification_question=clarification_question,
            citations=citations,
            execution_time_ms=execution_time_ms,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_history(self, limit: int = 50, session_id: Optional[str] = None) -> List[QueryLog]:
        stmt = self.db.query(QueryLog)
        if session_id:
            stmt = stmt.filter(QueryLog.session_id == session_id)
        return stmt.order_by(desc(QueryLog.created_at)).limit(limit).all()

    def add_feedback(self, query_log_id: str, rating: int, comments: Optional[str] = None) -> Feedback:
        fb = Feedback(query_log_id=query_log_id, rating=rating, comments=comments)
        self.db.add(fb)
        self.db.commit()
        self.db.refresh(fb)
        return fb
