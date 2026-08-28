from typing import List, Dict, Any
from backend.rag.schemas import EvidencePack, EvidenceExcerpt, ApplicableStandardItem, QCOItem


class EvidenceConstructor:
    """Assembles authoritative, bounded EvidencePack containing only verified standards, QCOs, and retrieved chunks."""

    def build_pack(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        compliance_data: Dict[str, Any],
        sources_list: List[Dict[str, Any]],
    ) -> EvidencePack:
        excerpts: List[EvidenceExcerpt] = []
        for item in retrieved_chunks:
            payload = item.get("payload") or {}
            content = item.get("content") or payload.get("content", "")
            is_num = payload.get("is_number") or "IS Standard"
            clause = payload.get("clause")
            section = payload.get("section")
            page = payload.get("page", 1)
            score = item.get("reranked_score") or item.get("fused_score", 0.0)

            excerpts.append(
                EvidenceExcerpt(
                    is_number=is_num,
                    section=str(section) if section else None,
                    clause=str(clause) if clause else None,
                    page=int(page) if page else None,
                    content=content,
                    score=float(score),
                    source=payload.get("source", "BIS Official"),
                )
            )

        return EvidencePack(
            standards=compliance_data.get("applicable_standards", []),
            qcos=compliance_data.get("qcos", []),
            certification_schemes=compliance_data.get("certification_schemes", []),
            amendments=compliance_data.get("amendments", []),
            document_excerpts=excerpts,
            sources=sources_list,
        )
