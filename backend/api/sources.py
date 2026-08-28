from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import Source

router = APIRouter(prefix="/api/sources", tags=["Sources & Authority"])


@router.get(
    "/",
    summary="List all authoritative BIS and governmental sources",
)
def list_sources(
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    sources = db.query(Source).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "url": s.url,
            "organization": s.organization,
            "source_type": s.source_type,
            "description": s.description,
            "last_verified": s.last_verified,
        }
        for s in sources
    ]


@router.get(
    "/{id}",
    summary="Get details for a specific source by ID",
)
def get_source(
    id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    source = db.query(Source).filter(Source.id == id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID '{id}' not found.",
        )
    return {
        "id": source.id,
        "name": source.name,
        "url": source.url,
        "organization": source.organization,
        "source_type": source.source_type,
        "description": source.description,
        "last_verified": source.last_verified,
    }
