import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.rag.retriever import RAGOrchestrator
from backend.rag.schemas import StructuredResponse
from backend.config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chat & RAG"])


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        description="User natural language question about standards or certification",
        min_length=1,
        max_length=2000,
    )
    user_role: Optional[str] = Field(
        "consumer",
        pattern=r"^(consumer|industry|auditor)$",
        description="User role: 'consumer', 'industry', or 'auditor'",
    )
    session_id: Optional[str] = Field(
        None,
        max_length=128,
        pattern=r"^[a-zA-Z0-9_\-]+$",
        description="Optional alphanumeric conversation session ID",
    )


@router.post(
    "/chat",
    response_model=StructuredResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question about BIS standards, QCOs, or certification",
)
def chat_endpoint(
    req: ChatRequest,
    db: Session = Depends(get_db),
) -> StructuredResponse:
    """Processes natural-language queries through the hybrid RAG pipeline."""
    try:
        orchestrator = RAGOrchestrator(db)
        response = orchestrator.process_query(
            query=req.query,
            user_role_override=req.user_role,
            session_id=req.session_id,
        )
        return response
    except Exception as e:
        logger.error(f"Error executing RAG pipeline for query '{req.query[:80]}': {e}", exc_info=True)
        detail_msg = f"Error executing RAG pipeline: {str(e)}" if settings.DEBUG else "Unable to process compliance query. Please try again."
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail_msg,
        )
