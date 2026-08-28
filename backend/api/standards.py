from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.repositories.standards_repo import StandardsRepository
from backend.database.repositories.qco_repo import QCORepository
from backend.database.repositories.document_repo import DocumentRepository

router = APIRouter(prefix="/api/standards", tags=["Standards"])


@router.get(
    "/search",
    summary="Search Indian Standards with keyword and metadata filters",
)
def search_standards(
    q: Optional[str] = Query(None, description="Keyword search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    status: Optional[str] = Query(None, description="Filter by status (e.g. Active)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    repo = StandardsRepository(db)
    results = repo.search(
        query=q,
        category=category,
        industry=industry,
        status=status,
        limit=limit,
        offset=offset,
    )
    items = []
    for s in results:
        items.append({
            "id": s.id,
            "is_number": s.is_number,
            "title": s.title,
            "year": s.year,
            "status": s.status,
            "category": s.category,
            "industry": s.industry,
            "committee": s.committee,
            "source_url": s.source_url,
            "amendments_count": len(s.amendments),
        })
    return {
        "total": len(items),
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.get(
    "/{id}",
    summary="Get details of a specific Indian Standard by ID or IS Number",
)
def get_standard_details(
    id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    repo = StandardsRepository(db)
    qco_repo = QCORepository(db)
    doc_repo = DocumentRepository(db)

    # Allow query by either UUID or IS number
    standard = repo.get_by_id(id) or repo.get_by_is_number(id)
    if not standard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Standard with identifier '{id}' not found.",
        )

    qcos = qco_repo.get_by_is_number(standard.is_number)
    chunks = doc_repo.get_chunks_by_standard(standard.id)

    return {
        "id": standard.id,
        "is_number": standard.is_number,
        "title": standard.title,
        "year": standard.year,
        "status": standard.status,
        "scope": standard.scope,
        "category": standard.category,
        "industry": standard.industry,
        "committee": standard.committee,
        "keywords": standard.keywords,
        "publication_date": standard.publication_date,
        "effective_date": standard.effective_date,
        "source_url": standard.source_url,
        "is_demo": standard.is_demo,
        "amendments": [
            {
                "id": a.id,
                "amendment_number": a.amendment_number,
                "title": a.title,
                "effective_date": a.effective_date,
                "notes": a.notes,
                "source_url": a.source_url,
            }
            for a in standard.amendments
        ],
        "qcos": [
            {
                "id": q.id,
                "qco_number": q.qco_number,
                "title": q.title,
                "ministry": q.ministry,
                "status": q.status,
                "enforcement_date": q.enforcement_date,
                "source_url": q.source_url,
            }
            for q in qcos
        ],
        "clauses": [
            {
                "section": c.section,
                "clause": c.clause,
                "page": c.page,
                "content": c.content,
            }
            for c in chunks
        ],
    }
