import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.sources import get_curated_apps, AppStoreReviewSource

client = TestClient(app)

def test_curated_apps_registry():
    apps = get_curated_apps()
    assert len(apps) >= 20
    names = [a["product_name"] for a in apps]
    assert "Spotify" in names
    assert "Zomato" in names
    assert "Swiggy" in names
    assert "Amazon" in names
    assert "Uber" in names
    assert "PhonePe" in names
    assert "Google Maps" in names

@pytest.mark.asyncio
async def test_app_store_search_curated():
    source = AppStoreReviewSource()
    results = await source.search_products("Spotify")
    assert len(results) > 0
    assert any("spotify" in r.product_name.lower() for r in results)

@pytest.mark.asyncio
async def test_app_store_fetch_reviews():
    source = AppStoreReviewSource()
    response = await source.fetch_reviews(product_id="324684580", product_name="Spotify")
    assert response.product.product_name == "Spotify"
    assert len(response.reviews) > 0
    assert response.source_meta.reviews_count > 0
    assert response.source_meta.fetch_timestamp is not None

def test_api_curated_products():
    response = client.get("/api/products/curated")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 20
    assert len(data["products"]) >= 20

def test_api_search_products():
    response = client.get("/api/products/search?q=uber")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any("uber" in r["product_name"].lower() for r in results)

def test_api_analyze_with_product_id():
    response = client.post("/api/analyze", json={"product_id": "324684580", "product_name": "Spotify"})
    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "Spotify"
    assert data["source_meta"] is not None
    assert data["sentiment_summary"]["total_reviews"] > 0
    assert len(data["product_opportunities"]) > 0
    assert len(data["user_requests"]) > 0
    assert len(data["roadmap"]["now"]) + len(data["roadmap"]["next"]) + len(data["roadmap"]["later"]) > 0
    assert "Spotify" in data["product_brief"]["markdown"]
