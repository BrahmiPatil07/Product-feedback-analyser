from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["ai_ready"] is True

def test_get_sample_reviews():
    response = client.get("/api/sample")
    assert response.status_code == 200
    data = response.json()
    assert len(data["reviews"]) == 25
    assert "Zomato" in data["dataset"]

def test_analyze_endpoint_with_raw_text():
    raw_text = """
    1. Delivery was very late, took 2 hours and food was cold!
    2. Loved the food, taste was delicious and fresh!
    3. Payment failed on UPI but money was debited twice.
    """
    response = client.post("/api/analyze", json={"raw_text": raw_text})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment_summary"]["total_reviews"] == 3
    assert len(data["theme_stats"]) == 8
    assert len(data["top_pain_points"]) > 0
    assert "product_brief" in data

def test_analyze_endpoint_empty_error():
    response = client.post("/api/analyze", json={"raw_text": "   "})
    assert response.status_code == 400
