import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
from app.models import (
    ReviewInput,
    AnalysisResponse,
    ProductSearchResult,
    ReviewFetchResponse,
)
from app.analyzer.rule_engine import RuleBasedAnalyzer
from app.sources import AppStoreReviewSource, get_curated_apps
from app.sample_data import (
    SAMPLE_ZOMATO_REVIEWS,
    SAMPLE_AMAZON_REVIEWS,
    SAMPLE_SAAS_REVIEWS,
)

# Initialize FastAPI application
app = FastAPI(
    title="Product Feedback Intelligence Platform API",
    description="Portfolio-grade feedback intelligence platform: Multi-App Selector, Live Public Review Retrieval, Opportunity Scoring, What Users Want, and 3-Horizon Roadmaps.",
    version="2.0.0",
)

# Enable CORS for local testing and external embedding
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate analysis engine & public review source
analyzer = RuleBasedAnalyzer()
review_source = AppStoreReviewSource()

# API Routes
@app.get("/api/health")
def health_check():
    """Service health check endpoint."""
    return {
        "status": "healthy",
        "service": "Product Feedback Intelligence Platform",
        "engine": "v2.0-product-intelligence",
        "ai_ready": True,
        "review_source": "Apple App Store Public RSS + Curated Registry"
    }

@app.get("/api/products/curated")
def get_popular_products():
    """Retrieve catalog of 22 curated tier-1 apps across domains."""
    return {
        "count": len(get_curated_apps()),
        "products": get_curated_apps(),
    }

@app.get("/api/products/search", response_model=List[ProductSearchResult])
async def search_products(q: str = "", country: str = "in"):
    """Search for apps/products via local curated registry and live iTunes Search API."""
    results = await review_source.search_products(query=q, country=country)
    return results

@app.get("/api/products/{product_id}/reviews", response_model=ReviewFetchResponse)
async def fetch_product_reviews(product_id: str, name: Optional[str] = "App", country: str = "in"):
    """Retrieve the latest public reviews for a product from Apple App Store RSS feed."""
    response = await review_source.fetch_reviews(
        product_id=product_id,
        product_name=name or "App",
        country=country,
    )
    return response

@app.get("/api/sample")
def get_sample_reviews(dataset: Optional[str] = "zomato"):
    """Retrieve pre-loaded authentic sample reviews across domains (Zomato, Amazon, SaaS)."""
    dataset_key = (dataset or "zomato").lower().strip()
    if dataset_key in ["amazon", "ecommerce", "flipkart"]:
        return {
            "dataset": "Amazon E-Commerce Reviews (20 samples)",
            "domain": "E-Commerce / Retail",
            "reviews": SAMPLE_AMAZON_REVIEWS,
        }
    elif dataset_key in ["saas", "software", "b2b"]:
        return {
            "dataset": "SaaS Productivity App Reviews (15 samples)",
            "domain": "SaaS / B2B Software",
            "reviews": SAMPLE_SAAS_REVIEWS,
        }
    else:
        return {
            "dataset": "Zomato Customer Reviews (25 samples)",
            "domain": "Food Delivery / Consumer",
            "reviews": SAMPLE_ZOMATO_REVIEWS,
        }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_feedback(payload: ReviewInput):
    """
    Analyze customer feedback reviews.
    Accepts:
    1. Direct product_id: Automatically fetches latest public reviews and analyzes them.
    2. reviews: List of review strings.
    3. raw_text: Multi-line or bulleted review text.
    """
    reviews_to_analyze = []
    source_meta = payload.source_meta
    product_name = payload.product_name
    product_category = payload.product_category
    product_icon_url = payload.product_icon_url

    # Case 1: Automatic live review retrieval if product_id provided and no text given
    if payload.product_id and not payload.reviews and not payload.raw_text:
        fetch_result = await review_source.fetch_reviews(
            product_id=payload.product_id,
            product_name=payload.product_name or "Selected Product",
        )
        reviews_to_analyze = fetch_result.reviews
        source_meta = fetch_result.source_meta.model_dump()
        product_name = fetch_result.product.product_name
        product_category = fetch_result.product.category
        product_icon_url = fetch_result.product.icon_url

    # Case 2: Structured reviews provided
    elif payload.reviews and len(payload.reviews) > 0:
        reviews_to_analyze = [r.strip() for r in payload.reviews if r and r.strip()]

    # Case 3: Raw pasted text provided
    elif payload.raw_text and payload.raw_text.strip():
        reviews_to_analyze = analyzer.parse_raw_reviews(payload.raw_text)

    if not reviews_to_analyze:
        raise HTTPException(
            status_code=400,
            detail="No valid reviews found. Please select a product or paste customer reviews."
        )

    # Perform analysis
    result = analyzer.analyze_reviews(
        reviews=reviews_to_analyze,
        product_name=product_name,
        product_category=product_category,
        product_icon_url=product_icon_url,
        source_meta=source_meta,
    )
    return result

# Mount static files for frontend dashboard
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    def serve_frontend():
        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found"}
