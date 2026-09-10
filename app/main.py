import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from app.models import ReviewInput, AnalysisResponse
from app.analyzer.rule_engine import RuleBasedAnalyzer
from app.sample_data import (
    SAMPLE_ZOMATO_REVIEWS,
    SAMPLE_AMAZON_REVIEWS,
    SAMPLE_SAAS_REVIEWS,
)

# Initialize FastAPI application
app = FastAPI(
    title="Product Feedback Intelligence Platform API",
    description="Portfolio-grade feedback intelligence platform: Sentiment, Themes, Opportunity Chains, What Users Want, and 3-Horizon Roadmaps.",
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

# Instantiate analysis engine
analyzer = RuleBasedAnalyzer()

# API Routes
@app.get("/api/health")
def health_check():
    """Service health check endpoint."""
    return {
        "status": "healthy",
        "service": "Product Feedback Intelligence Platform",
        "engine": "v2.0-product-intelligence",
        "ai_ready": True
    }

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
def analyze_feedback(payload: ReviewInput):
    """
    Analyze customer feedback reviews.
    Accepts either raw pasted text or structured list of reviews.
    """
    reviews_to_analyze = []

    if payload.reviews and len(payload.reviews) > 0:
        reviews_to_analyze = [r.strip() for r in payload.reviews if r and r.strip()]
    elif payload.raw_text and payload.raw_text.strip():
        reviews_to_analyze = analyzer.parse_raw_reviews(payload.raw_text)

    if not reviews_to_analyze:
        raise HTTPException(
            status_code=400,
            detail="No valid review text provided. Please paste reviews or provide a list."
        )

    # Perform analysis
    result = analyzer.analyze_reviews(reviews_to_analyze)
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

