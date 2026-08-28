import pytest
from backend.database.session import SessionLocal
from backend.rag.hybrid_search import HybridSearcher
from backend.rag.reranker import Reranker
from backend.rag.query_parser import QueryParser


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_hybrid_search_pressure_cooker(db):
    searcher = HybridSearcher(db)
    results = searcher.search("pressure cooker safety valve proof pressure", limit=5)

    assert len(results) > 0
    top_result = results[0]
    payload = top_result.get("payload", {})
    assert "IS 2347:2017" in payload.get("is_number", "")


def test_hybrid_search_exact_is_filter(db):
    searcher = HybridSearcher(db)
    results = searcher.search("ratings and dimensions", is_number_filter="IS 1293:2019", limit=5)

    assert len(results) > 0
    for r in results:
        assert "IS 1293" in r["payload"]["is_number"]


def test_reranker_boost(db):
    parser = QueryParser()
    reranker = Reranker()
    searcher = HybridSearcher(db)

    query = "IS 2347 proof pressure testing"
    parsed = parser.parse(query)
    candidates = searcher.search(query, limit=5)
    reranked = reranker.rerank(query, parsed, candidates, top_k=3)

    assert len(reranked) > 0
    top_payload = reranked[0]["payload"]
    assert "IS 2347:2017" in top_payload.get("is_number", "")
