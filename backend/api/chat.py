from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.rag.retriever import RAGOrchestrator
from backend.rag.schemas import StructuredResponse

router = APIRouter(prefix="/api", tags=["Chat & RAG"])


class ChatRequest(BaseModel):
    query: str = Field(..., description="User natural language question about standards or certification", min_length=1)
    user_role: Optional[str] = Field("consumer", description="User role: 'consumer' or 'industry'")
    session_id: Optional[str] = Field(None, description="Optional conversation session ID")


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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG pipeline: {str(e)}",
        )
