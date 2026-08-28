import pytest
from backend.database.session import SessionLocal
from backend.rag.retriever import RAGOrchestrator
from backend.rag.schemas import ConfidenceLevel, UserRole


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_rag_pipeline_industry_flow(db):
    orchestrator = RAGOrchestrator(db)
    response = orchestrator.process_query(
        "I manufacture stainless steel pressure cookers. Which BIS standard applies and do I need certification?",
        user_role_override="industry",
    )

    assert response.needs_clarification is False
    assert len(response.applicable_standards) > 0
    assert response.applicable_standards[0].is_number == "IS 2347:2017"
    assert response.certification_status == "Mandatory"
    assert len(response.qcos) > 0
    assert len(response.key_requirements) > 0
    assert len(response.compliance_steps) > 0
    assert len(response.sources) > 0
    assert response.confidence == ConfidenceLevel.HIGH


def test_rag_pipeline_consumer_flow(db):
    orchestrator = RAGOrchestrator(db)
    response = orchestrator.process_query(
        "How do I check if my electrical iron is BIS certified and safe to use at home?",
        user_role_override="consumer",
    )

    assert response.needs_clarification is False
    assert len(response.applicable_standards) > 0
    assert any("302-2-3" in s.is_number for s in response.applicable_standards)
    assert response.confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM]


def test_rag_pipeline_exact_is_search(db):
    orchestrator = RAGOrchestrator(db)
    response = orchestrator.process_query("What is IS 694:2010?")

    assert response.needs_clarification is False
    assert len(response.applicable_standards) > 0
    assert response.applicable_standards[0].is_number == "IS 694:2010"
    assert response.confidence == ConfidenceLevel.HIGH


def test_rag_pipeline_ambiguity_handling(db):
    orchestrator = RAGOrchestrator(db)
    response = orchestrator.process_query("What BIS certification do I need?")

    assert response.needs_clarification is True
    assert response.clarification_question is not None
    assert response.confidence == ConfidenceLevel.LOW
