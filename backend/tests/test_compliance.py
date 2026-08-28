import pytest
from backend.database.session import SessionLocal
from backend.rag.compliance import ComplianceResolver
from backend.rag.schemas import ParsedQuery


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_compliance_resolution_pressure_cooker(db):
    resolver = ComplianceResolver(db)
    parsed = ParsedQuery(
        original_query="Do I need mandatory BIS license for pressure cookers?",
        product="pressure cooker",
        is_number="IS 2347:2017",
    )
    res = resolver.resolve(parsed)

    assert len(res["applicable_standards"]) > 0
    std = res["applicable_standards"][0]
    assert std.is_number == "IS 2347:2017"
    assert std.mandatory is True
    assert res["certification_status"] == "Mandatory"
    assert len(res["qcos"]) > 0
    assert any(q.qco_number == "S.O. 3968(E)" for q in res["qcos"])


def test_compliance_resolution_electric_iron(db):
    resolver = ComplianceResolver(db)
    parsed = ParsedQuery(
        original_query="Electric iron safety standards",
        product="electric iron",
    )
    res = resolver.resolve(parsed)

    assert len(res["applicable_standards"]) > 0
    assert any("302-2-3" in s.is_number for s in res["applicable_standards"])
    assert res["certification_status"] == "Mandatory"
