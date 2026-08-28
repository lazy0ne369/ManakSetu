import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from backend.config.settings import settings
from backend.ingestion.embedder import Embedder
from backend.database.session import SessionLocal
from backend.database.models import DocumentChunk, Standard

logger = logging.getLogger(__name__)


_shared_qdrant_client: Optional[QdrantClient] = None


def get_shared_qdrant_client() -> QdrantClient:
    """Returns a shared QdrantClient instance to avoid file locking conflicts in local embedded mode."""
    global _shared_qdrant_client
    if _shared_qdrant_client is None:
        if settings.QDRANT_URL:
            logger.info(f"Connecting to remote Qdrant at {settings.QDRANT_URL}")
            _shared_qdrant_client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
            )
        else:
            storage_path = settings.QDRANT_STORAGE_PATH
            if not os.path.exists(storage_path):
                os.makedirs(storage_path, exist_ok=True)
            logger.info(f"Initializing local persistent Qdrant at {storage_path}")
            _shared_qdrant_client = QdrantClient(path=storage_path)
    return _shared_qdrant_client


class QdrantIndexer:
    def __init__(self, client: Optional[QdrantClient] = None):
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.dimension = settings.EMBEDDING_DIMENSION
        self.embedder = Embedder(dimension=self.dimension)
        self.client = client or get_shared_qdrant_client()
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Creates the Qdrant collection if it does not exist."""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                logger.info(f"Creating Qdrant collection '{self.collection_name}' with dim={self.dimension}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.dimension, distance=Distance.COSINE),
                )
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")
            raise

    def index_chunks(self, chunks_data: List[Dict[str, Any]]) -> int:
        """Indexes a batch of chunks into Qdrant."""
        if not chunks_data:
            return 0

        points = []
        for item in chunks_data:
            point_id = item.get("point_id") or str(uuid.uuid4())
            content = item.get("content", "")
            vector = item.get("vector") or self.embedder.embed_text(content)

            payload = {
                "chunk_id": item.get("chunk_id", point_id),
                "document_id": item.get("document_id"),
                "standard_id": item.get("standard_id"),
                "is_number": item.get("is_number"),
                "section": item.get("section"),
                "clause": item.get("clause"),
                "page": item.get("page", 1),
                "category": item.get("category"),
                "industry": item.get("industry"),
                "document_type": item.get("document_type", "standard"),
                "status": item.get("status", "Active"),
                "source": item.get("source", "BIS Official"),
                "content": content,
            }

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )
        logger.info(f"Successfully indexed {len(points)} chunks into Qdrant collection '{self.collection_name}'")
        return len(points)

    def sync_database_chunks_to_qdrant(self) -> int:
        """Synchronizes all DocumentChunks from PostgreSQL/SQLite to Qdrant."""
        db = SessionLocal()
        try:
            chunks = db.query(DocumentChunk).all()
            if not chunks:
                logger.warning("No DocumentChunks found in database to index.")
                return 0

            chunks_to_index = []
            for chk in chunks:
                point_id = chk.qdrant_point_id or str(uuid.uuid4())
                chk.qdrant_point_id = point_id

                meta = chk.metadata_json or {}
                chunks_to_index.append({
                    "point_id": point_id,
                    "chunk_id": chk.id,
                    "document_id": chk.document_id,
                    "standard_id": chk.standard_id,
                    "is_number": chk.is_number,
                    "section": chk.section,
                    "clause": chk.clause,
                    "page": chk.page,
                    "category": meta.get("category"),
                    "industry": meta.get("industry"),
                    "document_type": "standard",
                    "status": meta.get("document_status", "Active"),
                    "source": meta.get("source", "BIS Official"),
                    "content": chk.content,
                })

            indexed_count = self.index_chunks(chunks_to_index)
            db.commit()
            return indexed_count
        finally:
            db.close()

    def search_semantic(
        self,
        query: str,
        limit: int = 5,
        score_threshold: Optional[float] = None,
        is_number_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Semantic search against Qdrant collection with optional metadata filtering."""
        query_vector = self.embedder.embed_text(query)

        filter_conditions = []
        if is_number_filter:
            filter_conditions.append(
                FieldCondition(key="is_number", match=MatchValue(value=is_number_filter))
            )
        if category_filter:
            filter_conditions.append(
                FieldCondition(key="category", match=MatchValue(value=category_filter))
            )

        query_filter = Filter(must=filter_conditions) if filter_conditions else None

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold,
        ).points

        formatted = []
        for hit in results:
            formatted.append({
                "point_id": hit.id,
                "score": float(hit.score),
                "payload": hit.payload,
            })
        return formatted


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer = QdrantIndexer()
    count = indexer.sync_database_chunks_to_qdrant()
    print(f"Indexed {count} chunks into Qdrant.")
    test_search = indexer.search_semantic("pressure cooker safety valve proof test")
    print(f"Found {len(test_search)} test search results:")
    for r in test_search[:2]:
        print(f"  Score {r['score']:.3f} | {r['payload'].get('is_number')} Cl. {r['payload'].get('clause')}")
