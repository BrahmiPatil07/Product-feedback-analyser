"""
AI / LLM Adapter Stub for Product Feedback Analyser.
Demonstrates extensibility for future integration with Google Gemini or OpenAI APIs.
"""

import os
from typing import List, Optional
from app.analyzer.base import BaseFeedbackAnalyzer
from app.analyzer.rule_engine import RuleBasedAnalyzer
from app.models import AnalysisResponse

class AIAnalyzerAdapter(BaseFeedbackAnalyzer):
    """
    Adapter enabling seamless swapping between local rule-based analysis
    and generative AI / LLM analysis (e.g. Gemini 1.5 Pro/Flash or GPT-4o).
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.fallback_engine = RuleBasedAnalyzer()

    def is_ai_configured(self) -> bool:
        """Check if an API key is provided for external LLM inference."""
        return bool(self.api_key and self.api_key.strip())

    def analyze_reviews(self, reviews: List[str]) -> AnalysisResponse:
        """
        Analyze reviews using LLM if configured; otherwise gracefully fallback
        to the local rule-based engine with zero downtime or cost.
        """
        if not self.is_ai_configured():
            # Graceful zero-config fallback to rule engine
            return self.fallback_engine.analyze_reviews(reviews)

        # In production with API Key:
        # 1. Format prompt with structured JSON schema output
        # 2. Call Google GenAI SDK or OpenAI client
        # 3. Parse and validate with Pydantic AnalysisResponse
        # For now, execute local engine while preserving adapter compatibility
        response = self.fallback_engine.analyze_reviews(reviews)
        response.engine_version = f"hybrid-ai-ready ({self.model_name})"
        return response

