from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.repositories.query_log_repo import QueryLogRepository

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


class FeedbackRequest(BaseModel):
    query_id: str = Field(..., description="ID of the QueryLog message")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comments: Optional[str] = Field(None, description="Optional user comments or feedback")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Submit user feedback for an AI response",
)
def submit_feedback(
    req: FeedbackRequest,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    repo = QueryLogRepository(db)
    try:
        fb = repo.add_feedback(
            query_log_id=req.query_id,
            rating=req.rating,
            comments=req.comments,
        )
        return {
            "status": "success",
            "feedback_id": fb.id,
            "query_id": fb.query_log_id,
            "rating": fb.rating,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to record feedback: {str(e)}",
        )
