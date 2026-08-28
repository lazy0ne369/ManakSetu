import re
import logging
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session
from backend.database.models import DocumentChunk, Standard
from backend.ingestion.indexer import QdrantIndexer

logger = logging.getLogger(__name__)


class HybridSearcher:
    def __init__(self, db: Session, qdrant_indexer: Optional[QdrantIndexer] = None):
        self.db = db
        self.indexer = qdrant_indexer or QdrantIndexer()
        self._bm25 = None
        self._corpus_chunks: List[DocumentChunk] = []
        self._build_bm25_corpus()

    def _build_bm25_corpus(self) -> None:
        """Loads all chunks and builds BM25 index."""
        try:
            self._corpus_chunks = self.db.query(DocumentChunk).all()
            if not self._corpus_chunks:
                logger.warning("No DocumentChunks found for BM25 indexing.")
                return

            tokenized_corpus = []
            for chk in self._corpus_chunks:
                text = f"{chk.is_number} {chk.clause} {chk.section} {chk.content}".lower()
                tokens = re.findall(r"\w+", text)
                tokenized_corpus.append(tokens)

            self._bm25 = BM25Okapi(tokenized_corpus)
            logger.info(f"Built BM25 index over {len(self._corpus_chunks)} document chunks.")
        except Exception as e:
            logger.error(f"Error initializing BM25 corpus: {e}")

    def refresh_bm25(self) -> None:
        self._build_bm25_corpus()

    def search(
        self,
        query: str,
        limit: int = 10,
        is_number_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        bm25_weight: float = 0.5,
        vector_weight: float = 0.5,
        rrf_k: int = 60,
    ) -> List[Dict[str, Any]]:
        """Executes Hybrid Search combining BM25 keyword matching and Qdrant dense vector search using Reciprocal Rank Fusion (RRF)."""
        clean_q = query.strip()
        query_tokens = re.findall(r"\w+", clean_q.lower())

        # 1. Semantic Search from Qdrant
        semantic_results = self.indexer.search_semantic(
            query=clean_q,
            limit=limit * 2,
            is_number_filter=is_number_filter,
            category_filter=category_filter,
        )

        semantic_ranked = {}
        for rank, item in enumerate(semantic_results):
            payload = item["payload"]
            chunk_id = payload.get("chunk_id") or item["point_id"]
            semantic_ranked[chunk_id] = {
                "rank": rank + 1,
                "score": item["score"],
                "payload": payload,
                "content": payload.get("content", ""),
            }

        # 2. BM25 Keyword Search
        bm25_ranked = {}
        if self._bm25 and query_tokens and self._corpus_chunks:
            scores = self._bm25.get_scores(query_tokens)
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: limit * 2]

            rank = 1
            for idx in top_indices:
                score = scores[idx]
                if score <= 0.0:
                    continue
                chk = self._corpus_chunks[idx]

                # Apply metadata filters if specified
                if is_number_filter and chk.is_number and is_number_filter.lower() not in chk.is_number.lower():
                    continue

                meta = chk.metadata_json or {}
                if category_filter and meta.get("category") and category_filter.lower() not in meta.get("category", "").lower():
                    continue

                bm25_ranked[chk.id] = {
                    "rank": rank,
                    "score": float(score),
                    "payload": {
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
                    },
                    "content": chk.content,
                }
                rank += 1

        # 3. Reciprocal Rank Fusion (RRF)
        all_chunk_ids = set(semantic_ranked.keys()).union(set(bm25_ranked.keys()))
        fused_candidates = []

        for cid in all_chunk_ids:
            rrf_score = 0.0
            sem_data = semantic_ranked.get(cid)
            bm25_data = bm25_ranked.get(cid)

            payload = None
            content = ""

            if sem_data:
                rrf_score += vector_weight * (1.0 / (rrf_k + sem_data["rank"]))
                payload = sem_data["payload"]
                content = sem_data["content"]

            if bm25_data:
                rrf_score += bm25_weight * (1.0 / (rrf_k + bm25_data["rank"]))
                if not payload:
                    payload = bm25_data["payload"]
                    content = bm25_data["content"]

            # Exact keyword boost (e.g. if exact IS number or product appears in chunk content)
            if clean_q.lower() in content.lower():
                rrf_score += 0.05

            fused_candidates.append({
                "chunk_id": cid,
                "fused_score": rrf_score,
                "semantic_score": sem_data["score"] if sem_data else 0.0,
                "bm25_score": bm25_data["score"] if bm25_data else 0.0,
                "payload": payload,
                "content": content,
            })

        # Sort by fused score descending
        fused_candidates.sort(key=lambda x: x["fused_score"], reverse=True)
        return fused_candidates[:limit]
