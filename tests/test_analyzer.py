import pytest
from app.analyzer.rule_engine import RuleBasedAnalyzer
from app.sample_data import SAMPLE_ZOMATO_REVIEWS

@pytest.fixture
def analyzer():
    return RuleBasedAnalyzer()

def test_parse_raw_reviews(analyzer):
    raw_text = """
    1. First review about delivery delayed
    2. Second review about payment failed on UPI
    - Third review with bullet point
    * Fourth review with star bullet
    """
    parsed = analyzer.parse_raw_reviews(raw_text)
    assert len(parsed) == 4
    assert "delivery delayed" in parsed[0]
    assert "payment failed" in parsed[1]
    assert "Third review" in parsed[2]
    assert "Fourth review" in parsed[3]

def test_sentiment_classification_basic(analyzer):
    pos_sent, pos_score = analyzer._calculate_sentiment("Amazing delicious food and super fast delivery, loved it!")
    neg_sent, neg_score = analyzer._calculate_sentiment("Terrible experience, food was cold and rider was extremely rude.")
    neu_sent, neu_score = analyzer._calculate_sentiment("The food was delivered at 7:30 PM.")

    assert pos_sent == "Positive"
    assert pos_score > 0.15
    assert neg_sent == "Negative"
    assert neg_score < -0.15
    assert neu_sent == "Neutral"

def test_sentiment_negation_handling(analyzer):
    # Negation flips positive to negative
    neg_sent, neg_score = analyzer._calculate_sentiment("The food was not good at all, it was never hot.")
    assert neg_sent == "Negative"
    assert neg_score < 0.0

    # Negation flips negative to positive / less negative
    pos_sent, pos_score = analyzer._calculate_sentiment("The delivery was not bad and arrived on time.")
    assert pos_score > -0.15

def test_theme_categorization(analyzer):
    themes_delivery = analyzer._extract_themes("The delivery partner took 2 hours to reach.")
    assert "Delivery" in themes_delivery

    themes_payment = analyzer._extract_themes("Money debited from UPI but payment failed.")
    assert "Payment" in themes_payment

    themes_pricing = analyzer._extract_themes("Too expensive with high surge fee and hidden packaging charges.")
    assert "Pricing" in themes_pricing

    themes_bugs = analyzer._extract_themes("App crashes every time on checkout and freezes on OTP screen.")
    assert "Bugs" in themes_bugs

    themes_support = analyzer._extract_themes("The customer care chatbot was useless and unhelpful.")
    assert "Customer Support" in themes_support

    themes_offers = analyzer._extract_themes("The promo coupon was rejected and discount removed.")
    assert "Offers/Coupons" in themes_offers

def test_full_zomato_sample_analysis(analyzer):
    response = analyzer.analyze_reviews(SAMPLE_ZOMATO_REVIEWS)

    # Validate high-level structure
    assert response.sentiment_summary.total_reviews == 25
    assert response.sentiment_summary.positive_count > 0
    assert response.sentiment_summary.negative_count > 0
    assert len(response.reviews) == 25

    # Validate theme stats
    assert len(response.theme_stats) == 8
    theme_names = [t.theme for t in response.theme_stats]
    assert "Delivery" in theme_names
    assert "Payment" in theme_names
    assert "Pricing" in theme_names
    assert "Customer Support" in theme_names

    # Validate Top 3 Pain Points
    assert len(response.top_pain_points) == 3
    for p in response.top_pain_points:
        assert p.priority in ["High", "Medium", "Low"]
        assert len(p.recommended_feature) > 10
        assert len(p.success_metric) > 10
        assert len(p.root_cause) > 10

    # Validate Product Brief
    brief = response.product_brief
    assert "Executive Summary" in brief.markdown
    assert "Net Sentiment" in brief.markdown
    assert len(brief.action_plan) == 3
    assert len(brief.kpi_targets) == 3

def test_v2_opportunity_scoring_and_chains(analyzer):
    from app.sample_data import SAMPLE_AMAZON_REVIEWS
    response = analyzer.analyze_reviews(SAMPLE_AMAZON_REVIEWS)

    # Validate Product Opportunities
    assert len(response.product_opportunities) > 0
    top_opp = response.product_opportunities[0]
    
    # Validate full opportunity chain
    assert len(top_opp.theme) > 0
    assert len(top_opp.pain_point) > 0
    assert len(top_opp.root_cause_hypothesis) > 0
    assert len(top_opp.product_opportunity) > 0
    assert len(top_opp.feature_recommendation) > 0

    # Validate Opportunity Score Breakdown
    score = top_opp.opportunity_score
    assert 0 <= score.frequency_score <= 30
    assert 0 <= score.severity_score <= 40
    assert 0 <= score.user_impact_score <= 30
    assert 0 <= score.total_score <= 100
    assert score.potential_level in ["Critical Opportunity", "High Opportunity", "Medium Opportunity"]

    # Validate Evidence
    assert top_opp.evidence.review_count > 0
    assert len(top_opp.evidence.supporting_excerpts) > 0
    assert len(top_opp.evidence.reason_for_recommendation) > 0

    # Validate Compact V2 UI Fields
    assert top_opp.opportunity_title is not None and len(top_opp.opportunity_title) > 0
    assert top_opp.impact_badge in ["CRITICAL IMPACT", "HIGH IMPACT", "MEDIUM IMPACT"]
    assert top_opp.users_want_short is not None and len(top_opp.users_want_short) > 0
    assert top_opp.recommended_action_short is not None and len(top_opp.recommended_action_short) > 0

def test_v2_what_users_want_extraction(analyzer):
    from app.sample_data import SAMPLE_SAAS_REVIEWS
    response = analyzer.analyze_reviews(SAMPLE_SAAS_REVIEWS)

    assert len(response.user_requests) > 0
    req_types = [r.request_type for r in response.user_requests]
    assert "Explicit Request" in req_types or "Inferred Need" in req_types

    for req in response.user_requests:
        assert len(req.title) > 0
        assert req.mention_count >= 1
        assert len(req.supporting_excerpts) >= 1
        assert req.roadmap_horizon in ["NOW", "NEXT", "LATER"]

def test_v2_actionable_roadmap_categorization(analyzer):
    from app.sample_data import SAMPLE_ZOMATO_REVIEWS
    response = analyzer.analyze_reviews(SAMPLE_ZOMATO_REVIEWS)

    roadmap = response.roadmap
    assert len(roadmap.now) > 0
    for item in roadmap.now + roadmap.next + roadmap.later:
        assert item.horizon in ["NOW", "NEXT", "LATER"]
        assert item.priority in ["High", "Medium", "Low"]
        assert item.opportunity_score > 0
        assert len(item.success_metric) > 0

