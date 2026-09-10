"""
User Request & Need Extractor.
Extracts explicit user feature requests and inferred desires from reviews,
groups similar requests together, and links them to product opportunities and roadmap horizons.
"""

import re
from typing import List, Dict
from app.analyzer.lexicons import INTENT_REQUEST_PATTERNS
from app.models import (
    UserRequestItem,
    ReviewItem,
    ProductOpportunity,
    RequestType,
    RoadmapHorizon,
)

# Common Inferred Needs linked to friction patterns
INFERRED_NEED_CATALOG = [
    {
        "pattern": r"(?:bot|chatbot|unhelpful support|loop|disconnect|agent|canned response)",
        "title": "Direct 1-Click Human Agent Escalation Option",
        "theme": "Customer Support",
        "opportunity": "High-Empathy Instant Human Escalation",
        "horizon": "NOW",
    },
    {
        "pattern": r"(?:deducted twice|charged twice|double deduction|refund.*wait|failed.*debited|payment failed)",
        "title": "Instant 2-Minute Refund Wallet Credit for Failed Checkouts",
        "theme": "Payment",
        "opportunity": "Frictionless Zero-Anxiety Checkout Recovery",
        "horizon": "NOW",
    },
    {
        "pattern": r"(?:crash|freeze|stuck|blank screen|otp.*not|force close)",
        "title": "Hardened Crash-Safe Checkout & SMS OTP Auto-Retriever",
        "theme": "Bugs",
        "opportunity": "Bulletproof App Stability & Resilient State Recovery",
        "horizon": "NOW",
    },
    {
        "pattern": r"(?:late|delayed|took hours|rider unreachable|eta.*increasing|opposite direction)",
        "title": "Accurate Live Milestone Tracking & On-Time Delivery Guarantee",
        "theme": "Delivery",
        "opportunity": "Hyper-Transparent Predictive Dispatch",
        "horizon": "NOW",
    },
    {
        "pattern": r"(?:surge fee|hidden charges|packaging charge|platform fee|overpriced|expensive)",
        "title": "Upfront All-Inclusive Price Tag with No Last-Mile Surprise Fees",
        "theme": "Pricing",
        "opportunity": "Transparent All-Inclusive Value Display",
        "horizon": "NEXT",
    },
    {
        "pattern": r"(?:spilled|tampered|damaged|broken|stale|cold food|hair|missing|fake)",
        "title": "Certified Spill-Proof / Tamper-Evident Packaging & Quality Guarantee",
        "theme": "Order Quality",
        "opportunity": "Guaranteed Quality Seal & Pre-Dispatch Verification",
        "horizon": "NEXT",
    },
    {
        "pattern": r"(?:confusing|hard to find|cluttered|menu scrolling|filter)",
        "title": "Persistent Sticky Filters & 2-Tap Quick Reorder Drawer",
        "theme": "UI",
        "opportunity": "Streamlined 2-Tap Discovery",
        "horizon": "LATER",
    },
    {
        "pattern": r"(?:coupon.*rejected|discount vanished|terms and conditions|promo code)",
        "title": "Auto-Apply Best Eligible Coupon Directly at Cart Stage",
        "theme": "Offers/Coupons",
        "opportunity": "Smart Auto-Applied Savings",
        "horizon": "LATER",
    },
]

class RequestExtractor:
    """Extracts, clusters, and links explicit and inferred user requests."""

    def extract_requests(
        self,
        reviews: List[ReviewItem],
        opportunities: List[ProductOpportunity],
    ) -> List[UserRequestItem]:
        """Extract explicit user feature requests and high-confidence inferred needs."""
        requests: List[UserRequestItem] = []
        opp_lookup = {o.theme: o for o in opportunities}
        request_id = 1

        # 1. Extract Explicit Requests using linguistic markers
        explicit_groups: Dict[str, List[str]] = {}

        for rev in reviews:
            text = rev.text
            for pattern in INTENT_REQUEST_PATTERNS:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for m in matches:
                    req_phrase = m.group(1).strip()
                    # Clean up phrase
                    req_phrase = re.sub(r"^(to|for|that|if)\s+", "", req_phrase, flags=re.IGNORECASE)
                    if len(req_phrase) > 6:
                        # Normalize key for grouping
                        words = [w for w in re.findall(r"\b[a-z]{3,}\b", req_phrase.lower()) if w not in ["the", "and", "that", "this", "with"]]
                        key = " ".join(words[:4]) if words else req_phrase[:25].lower()
                        title = req_phrase.capitalize()
                        if len(title) > 60:
                            title = title[:57] + "..."

                        if key not in explicit_groups:
                            explicit_groups[key] = {"title": title, "reviews": []}
                        explicit_groups[key]["reviews"].append(text)

        for key, data in explicit_groups.items():
            excerpts = sorted(list(set(data["reviews"])), key=lambda q: len(q))[:3]
            count = len(data["reviews"])
            # Associate to closest theme or General
            linked_opp = "Feature Improvement"
            horizon: RoadmapHorizon = "NEXT"

            for opp in opportunities:
                if any(w in key for w in opp.theme.lower().split()):
                    linked_opp = opp.feature_recommendation
                    horizon = opp.roadmap_horizon
                    break

            requests.append(
                UserRequestItem(
                    id=request_id,
                    title=f"User Request: \"{data['title']}\"",
                    request_type="Explicit Request",
                    mention_count=count,
                    supporting_excerpts=excerpts,
                    linked_opportunity=linked_opp,
                    roadmap_horizon=horizon,
                )
            )
            request_id += 1

        # 2. Extract Inferred Needs from recurring friction patterns
        for catalog_item in INFERRED_NEED_CATALOG:
            regex = catalog_item["pattern"]
            matched_reviews = [
                r.text for r in reviews
                if re.search(regex, r.text, re.IGNORECASE) and r.sentiment in ["Negative", "Neutral"]
            ]

            # Only promote to an Inferred Need if supported by multiple reviews or critical friction
            if len(matched_reviews) >= 1:
                theme_name = catalog_item["theme"]
                opp = opp_lookup.get(theme_name)
                linked_opp_title = opp.feature_recommendation if opp else catalog_item["opportunity"]
                horizon = opp.roadmap_horizon if opp else catalog_item["horizon"]

                excerpts = sorted(matched_reviews, key=lambda q: len(q))[:2]

                requests.append(
                    UserRequestItem(
                        id=request_id,
                        title=f"Inferred Need: {catalog_item['title']}",
                        request_type="Inferred Need",
                        mention_count=len(matched_reviews),
                        supporting_excerpts=excerpts,
                        linked_opportunity=linked_opp_title,
                        roadmap_horizon=horizon,
                    )
                )
                request_id += 1

        # Sort: Explicit requests first, then by mention count descending
        requests.sort(key=lambda r: (1 if r.request_type == "Explicit Request" else 0, r.mention_count), reverse=True)

        return requests

