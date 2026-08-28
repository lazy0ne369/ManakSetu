from typing import List, Dict, Any, Tuple
from backend.rag.schemas import ConfidenceLevel, CitationItem, EvidencePack, ParsedQuery


class ConfidenceScorer:
    """Calculates factual confidence level based on evidence quality and completeness."""

    def calculate(
        self,
        parsed_query: ParsedQuery,
        evidence: EvidencePack,
    ) -> Tuple[ConfidenceLevel, List[CitationItem]]:
        citations: List[CitationItem] = []

        # Build citations directly from evidence excerpts and standards
        seen_citations = set()
        for exc in evidence.document_excerpts:
            key = f"{exc.is_number}:{exc.clause}:{exc.page}"
            if key not in seen_citations:
                seen_citations.add(key)
                citations.append(
                    CitationItem(
                        standard=exc.is_number,
                        clause=exc.clause,
                        section=exc.section,
                        page=exc.page,
                        source_url="https://www.services.bis.gov.in/",
                        excerpt=exc.content[:200] + "..." if len(exc.content) > 200 else exc.content,
                    )
                )

        # Standard citations if not covered
        for std in evidence.standards:
            key = f"{std.is_number}::"
            if key not in seen_citations:
                seen_citations.add(key)
                citations.append(
                    CitationItem(
                        standard=std.is_number,
                        clause=None,
                        section=None,
                        page=None,
                        source_url=std.source_url or "https://www.services.bis.gov.in/",
                        excerpt=std.title,
                    )
                )

        # Confidence heuristic
        has_exact_standard = len(evidence.standards) > 0
        has_qco = len(evidence.qcos) > 0
        has_clauses = len(evidence.document_excerpts) > 0
        is_exact_is_query = bool(parsed_query.is_number)

        if (has_exact_standard and has_clauses and (has_qco or is_exact_is_query)):
            confidence = ConfidenceLevel.HIGH
        elif has_exact_standard or has_clauses:
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW

        return confidence, citations
