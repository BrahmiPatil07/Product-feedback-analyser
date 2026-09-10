"""
Product Opportunity Analysis Engine & Roadmap Generator.
Transforms feedback into structured innovation chains:
Review -> Theme -> Pain Point -> Root Cause Hypothesis -> Product Opportunity -> Feature Recommendation
Calculates Product Opportunity Score (Frequency, Severity, User Impact).
"""

from typing import List, Dict, Tuple
from app.models import (
    ProductOpportunity,
    OpportunityScore,
    Evidence,
    RoadmapItem,
    ProductRoadmap,
    ThemeStat,
    ReviewItem,
    UserRequestItem,
    RoadmapHorizon,
    PriorityType,
)

THEME_OPPORTUNITY_MAP: Dict[str, dict] = {
    "Payment": {
        "opportunity_title": "Instant 120s Refund Bridge",
        "users_want_short": "Instant wallet credit if payment drops or fails at checkout.",
        "recommended_action_short": "Deploy dual-check webhook polling with automated 120s wallet credit fallback.",
        "pain_point": "Payment gateway drops, double deductions, and sluggish refund reconciliation.",
        "root_cause_hypothesis": "Asynchronous webhook callback latency between third-party payment rails (UPI/Cards/Banks) and order checkout state machine.",
        "product_opportunity": "Frictionless Zero-Anxiety Checkout Recovery: Guarantee instant state verification and zero-friction automated balance crediting.",
        "feature_recommendation": "Smart Dual-Check Webhook Polling & Instant 120s Wallet Refund Bridge.",
        "reason_for_recommendation": "Payment failure is a catastrophic funnel drop; providing instant state certainty stops churn and eliminates 60%+ of financial support tickets.",
        "success_metric": "Reduce checkout drop-off due to payment failures by 45% and decrease billing refund inquiries by 60%.",
        "default_horizon": "NOW",
        "base_impact": 1.9,
    },
    "Bugs": {
        "opportunity_title": "Crash-Safe Checkout Guard",
        "users_want_short": "Smooth, crash-free ordering without lost cart sessions or OTP freeze.",
        "recommended_action_short": "Implement crash-safe session state recovery and auto-retry network layer.",
        "pain_point": "Application crashes, frozen checkout views, and authentication/OTP verification timeouts.",
        "root_cause_hypothesis": "Uncaught UI lifecycle state transitions, unoptimized client memory footprints, and fragile SMS gateway timeouts.",
        "product_opportunity": "Bulletproof App Stability & Resilient Offline State Recovery.",
        "feature_recommendation": "Hardened Crash-Safe Session Guard & Auto-Retry Network Layer.",
        "reason_for_recommendation": "Technical crashes directly destroy customer trust; fixing core crashes delivers instant NPS lift and unlocks higher conversion.",
        "success_metric": "Reach 99.85% crash-free sessions and reduce OTP-related drop-offs by 80%.",
        "default_horizon": "NOW",
        "base_impact": 1.8,
    },
    "Delivery": {
        "opportunity_title": "Predictive Dispatch & Live Tracking",
        "users_want_short": "Accurate real-time ETAs and transparent rider milestone tracking.",
        "recommended_action_short": "Integrate dynamic dispatch engine with live milestone micro-tracking.",
        "pain_point": "Unpredictable delivery delays, opaque transit milestones, and inaccurate ETAs.",
        "root_cause_hypothesis": "Static routing heuristics failing to account for real-time merchant preparation variance and dynamic courier traffic congestion.",
        "product_opportunity": "Hyper-Transparent Predictive Dispatch & Real-Time Fulfillment Journey.",
        "feature_recommendation": "Dynamic AI Dispatch Engine with Live Milestone Micro-Tracking.",
        "reason_for_recommendation": "Predictability matters more than absolute speed; providing real-time live milestones reduces customer anxiety and inbound 'Where is my order' tickets.",
        "success_metric": "Improve On-Time Delivery (OTD) SLA to >95% and reduce delivery-related CSAT complaints by 35%.",
        "default_horizon": "NOW",
        "base_impact": 1.6,
    },
    "Customer Support": {
        "opportunity_title": "1-Click Human Agent Escalation",
        "users_want_short": "Instant bypass of unhelpful bot loops to reach a human support agent.",
        "recommended_action_short": "Add sentiment-triggered 1-click human escalation with live context handoff.",
        "pain_point": "Repetitive chatbot decision loops, lack of human agent escalation, and premature ticket closures.",
        "root_cause_hypothesis": "Over-indexing on automated ticket deflection metrics rather than First-Contact Resolution (FCR) and user sentiment.",
        "product_opportunity": "High-Empathy Instant Human Escalation: Empower users with priority support during active order emergencies.",
        "feature_recommendation": "1-Click Sentiment-Triggered Human Escalation & Live Agent Context Handoff.",
        "reason_for_recommendation": "Customers reaching support during an active emergency require immediate human validation; bypassing bot loops prevents public negative app reviews.",
        "success_metric": "Cut First Response Time (FRT) from 18 mins to <2 mins and lift Support CSAT from 2.9 to 4.4/5.0.",
        "default_horizon": "NEXT",
        "base_impact": 1.7,
    },
    "Order Quality": {
        "opportunity_title": "Tamper-Evident Quality Seal",
        "users_want_short": "Hot, undamaged items with verified packaging seals and zero missing dishes.",
        "recommended_action_short": "Establish tamper-evident QR packaging standards and pre-dispatch checklists.",
        "pain_point": "Damaged goods, in-transit spillage, missing items, and counterfeit/poor quality products.",
        "root_cause_hypothesis": "Absence of strict pre-dispatch merchant packaging standards and lack of warehouse/kitchen verification protocols.",
        "product_opportunity": "Guaranteed Quality Seal & Pre-Dispatch Digital Verification Protocol.",
        "feature_recommendation": "Tamper-Evident QR Packaging Standards & Merchant Item Pre-Checklist.",
        "reason_for_recommendation": "Physical product quality is the ultimate retention driver; enforcing packaging certification prevents return overhead and negative reviews.",
        "success_metric": "Reduce damaged item and replacement claims by 40% within 60 days.",
        "default_horizon": "NEXT",
        "base_impact": 1.5,
    },
    "Pricing": {
        "opportunity_title": "Upfront All-Inclusive Pricing",
        "users_want_short": "Zero surprise platform fees or surge markups at final checkout.",
        "recommended_action_short": "Display itemized all-inclusive doorstep total upfront throughout discovery.",
        "pain_point": "Opaque checkout fee stacking (surge, packaging, platform fees) causing last-minute cart abandonment.",
        "root_cause_hypothesis": "Fragmented pricing fee models presented abruptly at final checkout rather than transparently throughout the discovery funnel.",
        "product_opportunity": "Transparent All-Inclusive Value Display: Upfront itemized pricing without surprise last-mile markups.",
        "feature_recommendation": "Upfront Estimated Doorstep Total & Transparent Fee Breakdown Toggle.",
        "reason_for_recommendation": "Eliminating surprise charges builds long-term user goodwill and prevents last-second cart abandonment.",
        "success_metric": "Increase checkout completion rate by 4.5% and decrease pricing-related 1-star reviews by 30%.",
        "default_horizon": "NEXT",
        "base_impact": 1.3,
    },
    "UI": {
        "opportunity_title": "Streamlined 2-Tap Discovery",
        "users_want_short": "Simple sticky navigation with fast 2-tap search and reordering.",
        "recommended_action_short": "Introduce contextual sticky quick-filters and redesigned cart drawer.",
        "pain_point": "Cluttered navigation, hidden filter toggles, and unresponsive mobile tap targets.",
        "root_cause_hypothesis": "Feature bloat and deep multi-level menu hierarchies creating high cognitive load for high-intent shoppers.",
        "product_opportunity": "Streamlined 2-Tap Discovery: Simplified search taxonomy with persistent sticky filters.",
        "feature_recommendation": "Contextual Quick-Filters & Redesigned Bottom-Sheet Cart Summary.",
        "reason_for_recommendation": "Speed-to-purchase directly correlates with GMV; simplifying navigation eliminates friction for returning high-value users.",
        "success_metric": "Reduce average time-to-order by 25% and increase search-to-cart conversion by 12%.",
        "default_horizon": "LATER",
        "base_impact": 1.1,
    },
    "Offers/Coupons": {
        "opportunity_title": "Smart Auto-Applied Savings",
        "users_want_short": "Automatic application of best eligible discount codes directly in cart.",
        "recommended_action_short": "Implement context-aware auto-apply coupon engine with clear deficit micro-copy.",
        "pain_point": "Misleading promotional coupon terms, invalidation errors, and frustrating checkout promo exclusions.",
        "root_cause_hypothesis": "Complex merchant-funded promo rules decoupled from user cart state until final order validation.",
        "product_opportunity": "Smart Auto-Applied Savings: Real-time contextual promo eligibility that applies maximum savings automatically.",
        "feature_recommendation": "Context-Aware Auto-Apply Coupon Engine with Transparent Cart Deficit Micro-Copy.",
        "reason_for_recommendation": "Promotional clarity prevents disappointment at the purchase threshold and eliminates friction around expired or invalid codes.",
        "success_metric": "Boost promotion redemption satisfaction by 50% and reduce discount-related support inquiries by 40%.",
        "default_horizon": "LATER",
        "base_impact": 1.2,
    },
}

class OpportunityEngine:
    """Engine responsible for calculating Opportunity Scores, building chains, and roadmaps."""

    @staticmethod
    def calculate_opportunity_score(
        frequency: int,
        total_reviews: int,
        negative_count: int,
        neutral_count: int,
        base_impact: float,
    ) -> OpportunityScore:
        """
        Calculate transparent Product Opportunity Score (0-100).
        Frequency Score (0-30), Severity Score (0-40), User Impact Score (0-30).
        """
        tot = max(total_reviews, 1)
        freq_ratio = min(1.0, (frequency / tot) * 2.2)
        frequency_score = round(freq_ratio * 30.0, 1)

        freq = max(frequency, 1)
        neg_ratio = (negative_count * 1.0 + neutral_count * 0.3) / freq
        severity_score = round(min(1.0, neg_ratio * 1.1) * 40.0, 1)

        # Impact normalized (base_impact ranges ~1.0 to 1.9)
        norm_impact = min(1.0, base_impact / 1.9)
        user_impact_score = round(norm_impact * 30.0, 1)

        total = min(100, int(round(frequency_score + severity_score + user_impact_score)))

        if total >= 75:
            level = "Critical Opportunity"
        elif total >= 50:
            level = "High Opportunity"
        else:
            level = "Medium Opportunity"

        return OpportunityScore(
            frequency_score=frequency_score,
            severity_score=severity_score,
            user_impact_score=user_impact_score,
            total_score=total,
            potential_level=level,
        )

    def build_opportunities(
        self,
        theme_stats: List[ThemeStat],
        reviews: List[ReviewItem],
        total_reviews: int,
    ) -> List[ProductOpportunity]:
        """Construct ranked Product Opportunity chains for all active themes."""
        opportunities: List[ProductOpportunity] = []

        # Filter active themes with mentions
        active_themes = [t for t in theme_stats if t.count > 0]
        # Sort by friction & count
        active_themes.sort(key=lambda t: (t.severity_score, t.negative_count, t.count), reverse=True)

        for rank, stat in enumerate(active_themes, start=1):
            theme_meta = THEME_OPPORTUNITY_MAP.get(stat.theme, {
                "opportunity_title": f"Streamlined {stat.theme} Flow",
                "users_want_short": f"Seamless and friction-free experience with {stat.theme}.",
                "recommended_action_short": f"Optimize service workflows and feedback loops for {stat.theme}.",
                "pain_point": f"Customer friction and inconsistencies in {stat.theme}.",
                "root_cause_hypothesis": f"Service layer gaps and user expectation mismatches in {stat.theme}.",
                "product_opportunity": f"Optimize and streamline {stat.theme} experience.",
                "feature_recommendation": f"Enhanced {stat.theme} Management & Feedback Loop.",
                "reason_for_recommendation": f"Resolves critical user feedback regarding {stat.theme}.",
                "success_metric": f"Improve {stat.theme} satisfaction ratings by 30%.",
                "default_horizon": "NEXT",
                "base_impact": 1.2,
            })

            score = self.calculate_opportunity_score(
                frequency=stat.count,
                total_reviews=total_reviews,
                negative_count=stat.negative_count,
                neutral_count=stat.neutral_count,
                base_impact=theme_meta["base_impact"],
            )

            # Determine horizon based on score & default
            if score.total_score >= 70 or stat.negative_count >= 3:
                horizon: RoadmapHorizon = "NOW"
            elif score.total_score >= 45:
                horizon: RoadmapHorizon = "NEXT"
            else:
                horizon: RoadmapHorizon = "LATER"

            # Determine impact badge
            if score.total_score >= 75:
                impact_badge = "CRITICAL IMPACT"
            elif score.total_score >= 50:
                impact_badge = "HIGH IMPACT"
            else:
                impact_badge = "MEDIUM IMPACT"

            # Gather supporting review excerpts
            supporting_reviews = [
                r.text for r in reviews
                if stat.theme in r.themes and r.sentiment in ["Negative", "Neutral"]
            ]
            if not supporting_reviews:
                supporting_reviews = [r.text for r in reviews if stat.theme in r.themes]

            excerpts = sorted(supporting_reviews, key=lambda q: len(q))[:3]

            evidence = Evidence(
                review_count=stat.count,
                percentage=stat.percentage,
                theme=stat.theme,
                supporting_excerpts=excerpts,
                reason_for_recommendation=theme_meta["reason_for_recommendation"],
            )

            opportunities.append(
                ProductOpportunity(
                    id=rank,
                    rank=rank,
                    theme=stat.theme,
                    pain_point=theme_meta["pain_point"],
                    root_cause_hypothesis=theme_meta["root_cause_hypothesis"],
                    product_opportunity=theme_meta["product_opportunity"],
                    feature_recommendation=theme_meta["feature_recommendation"],
                    opportunity_score=score,
                    evidence=evidence,
                    success_metric=theme_meta["success_metric"],
                    roadmap_horizon=horizon,
                    opportunity_title=theme_meta.get("opportunity_title", f"{stat.theme} Initiative"),
                    impact_badge=impact_badge,
                    users_want_short=theme_meta.get("users_want_short", f"Improved {stat.theme} experience."),
                    recommended_action_short=theme_meta.get("recommended_action_short", theme_meta["feature_recommendation"]),
                )
            )

        return opportunities

    def build_roadmap(
        self,
        opportunities: List[ProductOpportunity],
    ) -> ProductRoadmap:
        """Categorize opportunities into actionable 3-horizon Roadmap."""
        now_items: List[RoadmapItem] = []
        next_items: List[RoadmapItem] = []
        later_items: List[RoadmapItem] = []

        item_id = 1
        for opp in opportunities:
            priority: PriorityType = (
                "High" if opp.opportunity_score.total_score >= 70
                else "Medium" if opp.opportunity_score.total_score >= 45
                else "Low"
            )

            item = RoadmapItem(
                id=item_id,
                title=opp.feature_recommendation,
                theme=opp.theme,
                description=opp.product_opportunity,
                horizon=opp.roadmap_horizon,
                priority=priority,
                opportunity_score=opp.opportunity_score.total_score,
                success_metric=opp.success_metric,
                reason=opp.evidence.reason_for_recommendation,
            )
            item_id += 1

            if opp.roadmap_horizon == "NOW":
                now_items.append(item)
            elif opp.roadmap_horizon == "NEXT":
                next_items.append(item)
            else:
                later_items.append(item)

        # Ensure balanced distribution if all fell into one horizon
        if not now_items and next_items:
            now_items.append(next_items.pop(0))
        if not next_items and later_items:
            next_items.append(later_items.pop(0))

        return ProductRoadmap(
            now=now_items,
            next=next_items,
            later=later_items,
        )

