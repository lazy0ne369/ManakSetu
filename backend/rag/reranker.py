import re
from typing import List, Dict, Any
from backend.rag.schemas import ParsedQuery


class Reranker:
    """Reranks candidate evidence chunks based on exact query term alignment, clause match, and entity coverage."""

    def rerank(
        self,
        query: str,
        parsed_query: ParsedQuery,
        candidates: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        query_terms = set(re.findall(r"\w+", query.lower()))
        reranked = []

        for item in candidates:
            payload = item.get("payload") or {}
            content = (item.get("content") or payload.get("content", "")).lower()
            is_number = (payload.get("is_number") or "").lower()
            clause = (payload.get("clause") or "").lower()

            base_score = item.get("fused_score", 0.0)
            score_boost = 0.0

            # 1. Exact IS number match boost
            if parsed_query.is_number and parsed_query.is_number.lower() in is_number:
                score_boost += 0.35

            # 2. Exact product match boost
            if parsed_query.product and parsed_query.product.lower() in content:
                score_boost += 0.25

            # 3. Material match boost
            if parsed_query.material and parsed_query.material.lower() in content:
                score_boost += 0.15

            # 4. Keyword overlap ratio
            matched_terms = [t for t in query_terms if t in content]
            overlap_ratio = len(matched_terms) / max(len(query_terms), 1)
            score_boost += overlap_ratio * 0.20

            # 5. Clause header penalty / boost
            if "clause" in query.lower() and clause and clause in query.lower():
                score_boost += 0.30

            final_score = base_score + score_boost

            reranked.append({
                **item,
                "reranked_score": final_score,
            })

        reranked.sort(key=lambda x: x["reranked_score"], reverse=True)
        return reranked[:top_k]
