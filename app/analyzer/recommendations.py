"""
Product management knowledge base mapping themes and severity to concrete product fixes
and quantifiable success metrics.
"""

THEME_KNOWLEDGE_BASE = {
    "Delivery": {
        "root_cause": "Delivery delays and inaccurate ETAs driven by merchant prep-time variance and suboptimal rider dispatch routing.",
        "recommended_feature": "Dynamic AI Dispatch & Live Kitchen-to-Doorstep Milestone Tracker: Implement predictive preparation time alerts and real-time rider batching.",
        "success_metric": "Reduce Delivery SLA breach complaints by 35% and improve On-Time Delivery (OTD) rate to >94% within 45 days.",
        "base_severity_weight": 1.4
    },
    "Payment": {
        "root_cause": "Payment gateway timeouts causing two-way state mismatch (bank debited but app transaction marked pending/failed).",
        "recommended_feature": "Instant Asynchronous Webhook Polling & Zero-Wait UPI Auto-Retry: Auto-poll bank status with fallback 2-minute instant refund credit.",
        "success_metric": "Reduce double-deduction grievance tickets by 60% and lower checkout payment drop-off from 7.5% to <2.5%.",
        "base_severity_weight": 1.6
    },
    "Pricing": {
        "root_cause": "Opaque checkout fee stacking (surge + platform + packaging charges) triggering last-mile cart abandonment.",
        "recommended_feature": "Transparent All-Inclusive Item Pricing & Clear Fee Itemization: Display estimated doorstep total upfront with breakdown breakdown toggle.",
        "success_metric": "Increase checkout conversion by 4.2% and decrease pricing-related 1-star app store ratings by 30%.",
        "base_severity_weight": 1.2
    },
    "UI": {
        "root_cause": "Cluttered menu layouts, high cognitive load in multi-filter navigation, and unresponsive tap targets on checkout.",
        "recommended_feature": "Streamlined 2-Tap Reorder & Simplified Search Taxonomy: Redesign dish filtering with sticky categories and bottom-sheet cart summary.",
        "success_metric": "Reduce average time-to-order (session to checkout) by 22% and decrease cart abandonment on mobile by 14%.",
        "base_severity_weight": 1.0
    },
    "Customer Support": {
        "root_cause": "Rigid decision-tree chatbots trapping agitated customers in endless loops during active delivery emergencies.",
        "recommended_feature": "1-Click Human Agent Escalation & Smart Context Handoff: Auto-detect high-sentiment frustration keywords to bypass bot instantly.",
        "success_metric": "Lift Customer Satisfaction (CSAT) score from 2.9 to 4.3/5.0 and reduce First Response Time (FRT) from 18 mins to <3 mins.",
        "base_severity_weight": 1.5
    },
    "Order Quality": {
        "root_cause": "Merchant packaging failures causing in-transit liquid spills, thermal dissipation, and missing ancillary items.",
        "recommended_feature": "Merchant Packaging Certification & Digital Pre-Dispatch Item Checklist: QR-sealed spill-proof containers with photo verification.",
        "success_metric": "Reduce damaged/spilled order refund claims by 45% and improve merchant food quality rating by 0.6 stars.",
        "base_severity_weight": 1.4
    },
    "Bugs": {
        "root_cause": "Unhandled memory leaks and unoptimized asset bundles causing runtime crashes on mid-tier Android devices and checkout OTP drops.",
        "recommended_feature": "Hardened Checkout Crash Guard & Silent SMS Retriever API: Auto-capture state on crash and optimize app cold-start payload by 40%.",
        "success_metric": "Achieve 99.8% crash-free sessions across Android/iOS and cut OTP verification drop-outs by 80%.",
        "base_severity_weight": 1.5
    },
    "Offers/Coupons": {
        "root_cause": "Misleading promo banner conditions resulting in coupon invalidation errors at checkout and perceived user deception.",
        "recommended_feature": "Context-Aware Auto-Apply Coupon Engine: Only show eligible offers in cart with clear micro-copy explaining exact minimum cart requirements.",
        "success_metric": "Increase promotional redemption satisfaction by 50% and decrease coupon-related support inquiries by 40%.",
        "base_severity_weight": 1.1
    },
}

def get_theme_recommendation(theme: str) -> dict:
    """Retrieve product fix and success metric for a given theme."""
    default = {
        "root_cause": "Inconsistencies in product flow and user expectations.",
        "recommended_feature": "Enhanced user feedback loop and targeted service improvements.",
        "success_metric": "Improve customer satisfaction score (CSAT) by 25% within one quarter.",
        "base_severity_weight": 1.0
    }
    return THEME_KNOWLEDGE_BASE.get(theme, default)
