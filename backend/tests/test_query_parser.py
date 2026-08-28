import pytest
from backend.rag.query_parser import QueryParser
from backend.rag.classifier import IntentClassifier
from backend.rag.schemas import UserRole, QueryIntent


@pytest.fixture
def parser():
    return QueryParser()


@pytest.fixture
def classifier():
    return IntentClassifier()


def test_industry_pressure_cooker_query(parser, classifier):
    query = "I manufacture stainless steel pressure cookers. Which BIS standard applies and do I need certification?"
    parsed = parser.parse(query)
    intent = classifier.classify(parsed)

    assert parsed.product == "pressure cooker"
    assert parsed.material == "stainless steel"
    assert parsed.user_role == UserRole.INDUSTRY
    assert parsed.needs_clarification is False
    assert intent == QueryIntent.CERTIFICATION


def test_exact_is_number_extraction(parser, classifier):
    query = "What are the test requirements in IS 1293:2019 for 16A plugs?"
    parsed = parser.parse(query)
    intent = classifier.classify(parsed)

    assert parsed.is_number == "IS 1293:2019"
    assert intent in [QueryIntent.STANDARD_LOOKUP, QueryIntent.COMPLIANCE]


def test_consumer_toy_query(parser, classifier):
    query = "Is it safe to buy this plastic toy for a 2 year old without ISI mark?"
    parsed = parser.parse(query)

    assert parsed.product == "toy"
    assert parsed.user_role == UserRole.CONSUMER
    assert parsed.needs_clarification is False


def test_ambiguous_query_clarification(parser):
    query = "What BIS certification do I need?"
    parsed = parser.parse(query)

    assert parsed.needs_clarification is True
    assert parsed.clarification_question is not None


def test_qco_intent_classification(parser, classifier):
    query = "Is there any Quality Control Order issued by DPIIT for PVC cables?"
    parsed = parser.parse(query)
    intent = classifier.classify(parsed)

    assert parsed.product == "pvc cable"
    assert intent == QueryIntent.QCO
