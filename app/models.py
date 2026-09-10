from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

SentimentType = Literal["Positive", "Neutral", "Negative"]
PriorityType = Literal["High", "Medium", "Low"]
RoadmapHorizon = Literal["NOW", "NEXT", "LATER"]
RequestType = Literal["Explicit Request", "Inferred Need"]

class ReviewInput(BaseModel):
    """Input payload for feedback analysis."""
    raw_text: Optional[str] = Field(None, description="Pasted multi-line review text")
    reviews: Optional[List[str]] = Field(None, description="List of review strings")
    product_name: Optional[str] = Field(None, description="Name of the selected product / app")
    product_icon_url: Optional[str] = Field(None, description="URL of the app icon")
    product_category: Optional[str] = Field(None, description="App category or industry")
    source_meta: Optional[Dict] = Field(None, description="Review provenance metadata")
    product_id: Optional[str] = Field(None, description="App Store Track ID if fetching directly")

class ProductSearchResult(BaseModel):
    """Product result from public app search or curated list."""
    product_id: str
    product_name: str
    category: str = "General"
    icon_url: Optional[str] = None
    developer: Optional[str] = None
    rating: Optional[float] = None
    source: str = "Apple App Store (Public RSS)"

class ReviewSourceMeta(BaseModel):
    """Metadata describing where reviews originated from."""
    source_name: str
    product_name: str
    product_id: Optional[str] = None
    product_icon_url: Optional[str] = None
    product_category: Optional[str] = None
    reviews_count: int
    fetch_timestamp: str
    is_live_data: bool = True
    fallback_reason: Optional[str] = None

class ReviewFetchResponse(BaseModel):
    """Payload returned when fetching reviews for a selected product."""
    product: ProductSearchResult
    source_meta: ReviewSourceMeta
    reviews: List[str]

class ReviewItem(BaseModel):
    """Individual analyzed review."""
    id: int
    text: str
    sentiment: SentimentType
    sentiment_score: float = Field(..., description="Calculated polarity between -1.0 and 1.0")
    themes: List[str] = Field(default_factory=list, description="Categorized themes for this review")
    pain_flags: List[str] = Field(default_factory=list, description="Triggered pain keywords")

class ThemeStat(BaseModel):
    """Mention counts and sentiment distribution per theme."""
    theme: str
    count: int
    percentage: float
    positive_count: int = 0
    neutral_count: int = 0
    negative_count: int = 0
    severity_score: float = 0.0

class PainPoint(BaseModel):
    """Identified critical pain point."""
    rank: int
    theme: str
    priority: PriorityType
    frequency: int
    negative_count: int
    severity_score: float
    root_cause: str
    representative_quotes: List[str]
    recommended_feature: str
    success_metric: str

class SentimentSummary(BaseModel):
    """Overall sentiment metrics."""
    total_reviews: int
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_pct: float
    neutral_pct: float
    negative_pct: float
    net_sentiment_score: float = Field(..., description="% Positive minus % Negative")

class OpportunityScore(BaseModel):
    """Structured breakdown of Product Opportunity Score (POS)."""
    frequency_score: float = Field(..., description="Normalized score based on mention frequency (0-30)")
    severity_score: float = Field(..., description="Score based on pain severity & negative ratio (0-40)")
    user_impact_score: float = Field(..., description="Criticality to user journey & retention (0-30)")
    total_score: int = Field(..., description="Overall Opportunity Score (0-100)")
    potential_level: Literal["Critical Opportunity", "High Opportunity", "Medium Opportunity"]

class Evidence(BaseModel):
    """Empirical evidence backing a recommendation."""
    review_count: int
    percentage: float
    theme: str
    supporting_excerpts: List[str]
    reason_for_recommendation: str

class ProductOpportunity(BaseModel):
    """
    Full opportunity chain:
    Review -> Theme -> Pain Point -> Root Cause Hypothesis -> Product Opportunity -> Feature Recommendation
    """
    id: int
    rank: int
    theme: str
    pain_point: str
    root_cause_hypothesis: str
    product_opportunity: str
    feature_recommendation: str
    opportunity_score: OpportunityScore
    evidence: Evidence
    success_metric: str
    roadmap_horizon: RoadmapHorizon
    # Compact V2 UI Fields
    opportunity_title: Optional[str] = Field(None, description="Short 3-6 word punchy title")
    impact_badge: Optional[str] = Field("HIGH IMPACT", description="HIGH IMPACT, MEDIUM IMPACT, or LOW IMPACT")
    users_want_short: Optional[str] = Field(None, description="One short sentence summarizing user desire")
    recommended_action_short: Optional[str] = Field(None, description="One short sentence summarizing recommended action")


class UserRequestItem(BaseModel):
    """Extracted user feature request or inferred desire."""
    id: int
    title: str
    request_type: RequestType
    mention_count: int
    supporting_excerpts: List[str]
    linked_opportunity: str
    roadmap_horizon: RoadmapHorizon

class RoadmapItem(BaseModel):
    """Item placed on the actionable product roadmap."""
    id: int
    title: str
    theme: str
    description: str
    horizon: RoadmapHorizon
    priority: PriorityType
    opportunity_score: int
    success_metric: str
    reason: str
    what_users_want: Optional[str] = Field(None, description="Short sentence summarizing user desire")
    recommended_action: Optional[str] = Field(None, description="Concrete recommended product action")
    why_prioritized: Optional[str] = Field(None, description="PM rationale for roadmap placement")
    review_count: Optional[int] = Field(None, description="Number of supporting reviews")
    problem: Optional[str] = Field(None, description="Underlying customer problem / friction")

class ProductRoadmap(BaseModel):
    """3-Horizon Actionable Product Roadmap."""
    now: List[RoadmapItem] = Field(default_factory=list, description="Immediate sprint / blocker items")
    next: List[RoadmapItem] = Field(default_factory=list, description="Next cycle enhancements & optimizations")
    later: List[RoadmapItem] = Field(default_factory=list, description="Strategic & platform scale items")

class ProductBrief(BaseModel):
    """Executive product brief summary."""
    title: str
    executive_summary: str
    key_findings: List[str]
    action_plan: List[dict]
    kpi_targets: List[str]
    markdown: str
    product_name: Optional[str] = "Generic Product"
    review_source: Optional[str] = "Public Customer Reviews"
    fetch_timestamp: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Complete structured response returned to client."""
    sentiment_summary: SentimentSummary
    theme_stats: List[ThemeStat]
    top_pain_points: List[PainPoint]
    reviews: List[ReviewItem]
    product_brief: ProductBrief
    # V2 Additions
    product_opportunities: List[ProductOpportunity] = Field(default_factory=list)
    user_requests: List[UserRequestItem] = Field(default_factory=list)
    roadmap: ProductRoadmap = Field(default_factory=ProductRoadmap)
    engine_version: str = "v2.0-product-intelligence"
    # V2 Generic Product Provenance Metadata
    product_name: Optional[str] = Field("Generic Product", description="Analyzed product name")
    product_category: Optional[str] = Field("Consumer Software", description="Analyzed product category")
    product_icon_url: Optional[str] = Field(None, description="App icon URL")
    source_meta: Optional[ReviewSourceMeta] = Field(None, description="Provenance of analyzed reviews")

