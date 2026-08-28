from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import DocumentChunk, Standard, Document
from backend.ingestion.indexer import QdrantIndexer
from backend.knowledge.seed_data import seed_database

router = APIRouter(prefix="/api/ingestion", tags=["Ingestion & Admin"])


@router.post(
    "/run",
    summary="Trigger database seeding and vector index synchronization",
)
def run_ingestion(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    try:
        # Seed database if not populated
        seed_database(db)
        # Sync chunks to Qdrant
        indexer = QdrantIndexer()
        indexed_count = indexer.sync_database_chunks_to_qdrant()
        return {
            "status": "success",
            "message": f"Successfully ingested and indexed {indexed_count} chunks into Qdrant.",
            "indexed_chunks": indexed_count,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}",
        )


@router.get(
    "/status",
    summary="Get ingestion and vector database status",
)
def get_ingestion_status(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    total_standards = db.query(Standard).count()
    total_docs = db.query(Document).count()
    total_chunks = db.query(DocumentChunk).count()

    qdrant_status = "connected"
    collection_points = 0
    try:
        indexer = QdrantIndexer()
        info = indexer.client.get_collection(indexer.collection_name)
        collection_points = info.points_count
    except Exception as e:
        qdrant_status = f"unavailable: {str(e)}"

    return {
        "database": {
            "total_standards": total_standards,
            "total_documents": total_docs,
            "total_chunks": total_chunks,
        },
        "vector_store": {
            "status": qdrant_status,
            "collection_name": "bis_standards_chunks",
            "points_count": collection_points,
        },
    }
