import time
import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.rag.schemas import (
    ParsedQuery,
    StructuredResponse,
    UserRole,
    QueryIntent,
)
from backend.rag.query_parser import QueryParser
from backend.rag.classifier import IntentClassifier
from backend.rag.hybrid_search import HybridSearcher
from backend.rag.reranker import Reranker
from backend.rag.compliance import ComplianceResolver
from backend.rag.evidence import EvidenceConstructor
from backend.rag.confidence import ConfidenceScorer
from backend.rag.generator import LLMGenerator
from backend.database.repositories.standards_repo import StandardsRepository
from backend.database.repositories.query_log_repo import QueryLogRepository

logger = logging.getLogger(__name__)


class RAGOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.parser = QueryParser()
        self.classifier = IntentClassifier()
        self.hybrid_searcher = HybridSearcher(db)
        self.reranker = Reranker()
        self.compliance_resolver = ComplianceResolver(db)
        self.evidence_constructor = EvidenceConstructor()
        self.confidence_scorer = ConfidenceScorer()
        self.generator = LLMGenerator()
        self.query_log_repo = QueryLogRepository(db)

    def process_query(
        self,
        query: str,
        user_role_override: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> StructuredResponse:
        """Full End-to-End RAG Query Execution Pipeline."""
        start_time = time.time()
        logger.info(f"Processing user query: '{query}' (Role override: {user_role_override})")

        # 1. Query Understanding & Entity Extraction
        parsed: ParsedQuery = self.parser.parse(query, user_role_override=user_role_override)
        parsed.intent = self.classifier.classify(parsed)
        logger.info(f"Parsed entity: product='{parsed.product}', is_number='{parsed.is_number}', role='{parsed.user_role.value}', intent='{parsed.intent.value}'")

        # 2. Check for Ambiguity / Clarification early exit
        if parsed.needs_clarification:
            resp = self.generator.generate(parsed, None, None, [])
            execution_time = int((time.time() - start_time) * 1000)
            self.query_log_repo.log_query(
                user_query=query,
                role_type=parsed.user_role.value,
                intent=parsed.intent.value,
                parsed_entities=parsed.model_dump(),
                raw_response=resp.model_dump(),
                confidence=resp.confidence.value,
                needs_clarification=True,
                clarification_question=resp.clarification_question,
                citations=[],
                execution_time_ms=execution_time,
                session_id=session_id,
            )
            return resp

        # 3. Hybrid Retrieval (Qdrant semantic + BM25 keyword + metadata filtering)
        candidates = self.hybrid_searcher.search(
            query=parsed.original_query,
            limit=10,
            is_number_filter=parsed.is_number,
        )

        # 4. Candidate Reranking
        top_evidence_chunks = self.reranker.rerank(
            query=parsed.original_query,
            parsed_query=parsed,
            candidates=candidates,
            top_k=5,
        )

        # 5. Regulatory & Compliance Resolution
        valid_evidence_chunks = [
            c for c in top_evidence_chunks
            if c.get("reranked_score", 0.0) >= 0.15 or c.get("fused_score", 0.0) >= 0.035
        ]

        retrieved_is_numbers = [
            c["payload"]["is_number"]
            for c in valid_evidence_chunks
            if c.get("payload") and c["payload"].get("is_number")
        ]
        retrieved_is_numbers = list(dict.fromkeys(retrieved_is_numbers))

        compliance_data = self.compliance_resolver.resolve(
            parsed_query=parsed,
            retrieved_is_numbers=retrieved_is_numbers,
        )

        # 6. Authoritative Sources List
        sources_list = [
            {"name": "Bureau of Indian Standards", "url": "https://www.services.bis.gov.in/"},
            {"name": "Ministry of Commerce and Industry (DPIIT)", "url": "https://dpiit.gov.in/"},
        ]

        # 7. Evidence Pack Construction
        evidence_pack = self.evidence_constructor.build_pack(
            retrieved_chunks=valid_evidence_chunks,
            compliance_data=compliance_data,
            sources_list=sources_list,
        )

        # 8. Confidence Scoring & Citation Extraction
        confidence, citations = self.confidence_scorer.calculate(parsed, evidence_pack)

        # 9. LLM / Grounded Response Generation
        response = self.generator.generate(
            parsed_query=parsed,
            evidence=evidence_pack,
            confidence=confidence,
            citations=citations,
        )

        # 10. Log Query Execution
        execution_time = int((time.time() - start_time) * 1000)
        self.query_log_repo.log_query(
            user_query=query,
            role_type=parsed.user_role.value,
            intent=parsed.intent.value,
            parsed_entities=parsed.model_dump(),
            raw_response=response.model_dump(),
            confidence=response.confidence.value,
            needs_clarification=response.needs_clarification,
            clarification_question=response.clarification_question,
            citations=[c.model_dump() for c in response.sources],
            execution_time_ms=execution_time,
            session_id=session_id,
        )

        return response
