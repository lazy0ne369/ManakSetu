import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_chat_endpoint_valid():
    payload = {
        "query": "Which standard applies to domestic pressure cookers and is it mandatory?",
        "user_role": "industry"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["applicable_standards"]) > 0
    assert data["applicable_standards"][0]["is_number"] == "IS 2347:2017"
    assert data["certification_status"] == "Mandatory"
    assert data["confidence"] == "high"


def test_chat_endpoint_clarification():
    payload = {
        "query": "What BIS certification do I need?"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["needs_clarification"] is True
    assert data["clarification_question"] is not None


def test_standards_search_api():
    response = client.get("/api/standards/search?q=pressure")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("2347" in item["is_number"] for item in data["items"])


def test_standards_detail_api():
    response = client.get("/api/standards/IS%202347:2017")
    assert response.status_code == 200
    data = response.json()
    assert data["is_number"] == "IS 2347:2017"
    assert len(data["clauses"]) > 0
    assert len(data["qcos"]) > 0


def test_compliance_api():
    response = client.get("/api/compliance/pressure%20cooker")
    assert response.status_code == 200
    data = response.json()
    assert data["product"] == "pressure cooker"
    assert len(data["applicable_standards"]) > 0


def test_sources_api():
    response = client.get("/api/sources/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_history_and_feedback_api():
    # 1. Ask a question to generate history
    chat_resp = client.post("/api/chat", json={"query": "What is IS 1293?"})
    assert chat_resp.status_code == 200

    # 2. Check history
    hist_resp = client.get("/api/history?limit=5")
    assert hist_resp.status_code == 200
    logs = hist_resp.json()
    assert len(logs) > 0
    query_id = logs[0]["id"]

    # 3. Submit feedback
    fb_resp = client.post(
        "/api/feedback",
        json={"query_id": query_id, "rating": 5, "comments": "Very clear and helpful!"}
    )
    assert fb_resp.status_code == 201
    fb_data = fb_resp.json()
    assert fb_data["status"] == "success"


def test_ingestion_status_api():
    response = client.get("/api/ingestion/status")
    assert response.status_code == 200
    data = response.json()
    assert data["database"]["total_standards"] >= 6
    assert data["database"]["total_chunks"] >= 20
