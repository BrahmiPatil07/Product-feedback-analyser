import re
import datetime
from typing import List, Tuple
from app.analyzer.base import BaseFeedbackAnalyzer
from app.analyzer.lexicons import (
    THEMES,
    THEME_KEYWORDS,
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    INTENSIFIERS,
    NEGATION_WORDS,
    THEME_PAIN_INDICATORS,
)
from app.analyzer.recommendations import get_theme_recommendation
from app.analyzer.opportunity_engine import OpportunityEngine
from app.analyzer.request_extractor import RequestExtractor
from app.models import (
    AnalysisResponse,
    ReviewItem,
    SentimentSummary,
    ThemeStat,
    PainPoint,
    ProductBrief,
    ProductOpportunity,
    UserRequestItem,
    ProductRoadmap,
    SentimentType,
    PriorityType,
)

class RuleBasedAnalyzer(BaseFeedbackAnalyzer):
    """
    Robust local rule-based analysis engine.
    Calculates sentiment with negation awareness, categorizes into 8 domain themes,
    ranks critical pain points, models product opportunities, and generates
    actionable 3-horizon roadmaps and executive product briefs.
    """

    def __init__(self):
        self.opportunity_engine = OpportunityEngine()
        self.request_extractor = RequestExtractor()

    def parse_raw_reviews(self, raw_text: str) -> List[str]:
        """Split raw multi-line or bulleted text into individual reviews."""
        if not raw_text or not raw_text.strip():
            return []
        
        # Split by newlines first
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        cleaned_reviews = []
        current_review = []

        for line in lines:
            # Check if line starts with a number or bullet (e.g., '1.', '1)', '-', '*')
            is_new_item = bool(re.match(r"^(\d+[\.\)\-:]|\*|\-|\•)\s+", line))
            if is_new_item:
                if current_review:
                    cleaned_reviews.append(" ".join(current_review))
                    current_review = []
                # Strip leading marker
                cleaned_line = re.sub(r"^(\d+[\.\)\-:]|\*|\-|\•)\s+", "", line).strip()
                if cleaned_line:
                    current_review.append(cleaned_line)
            else:
                current_review.append(line)

        if current_review:
            cleaned_reviews.append(" ".join(current_review))

        # If splitting by bullet didn't produce multiple items, fallback to non-empty lines
        if len(cleaned_reviews) <= 1 and len(lines) > 1:
            return lines

        return [r for r in cleaned_reviews if len(r) > 5]

    def _calculate_sentiment(self, text: str) -> Tuple[SentimentType, float]:
        """
        Calculate sentiment polarity between -1.0 and 1.0 using lexicon,
        negation window, and intensifier multipliers.
        """
        lower_text = text.lower()
        # Clean into tokens while keeping apostrophes for contractions like didn't
        words = re.findall(r"\b[a-z']+\b", lower_text)
        if not words:
            return "Neutral", 0.0

        score = 0.0
        n_words = len(words)

        for i, word in enumerate(words):
            # Check if word is in positive or negative lexicon
            pos_weight = POSITIVE_WORDS.get(word, 0.0)
            neg_weight = NEGATIVE_WORDS.get(word, 0.0)

            if pos_weight == 0.0 and neg_weight == 0.0:
                continue

            word_weight = pos_weight if pos_weight != 0.0 else neg_weight

            # Check previous 3 words for intensifiers and negations
            window_start = max(0, i - 3)
            window = words[window_start:i]

            multiplier = 1.0
            is_negated = False

            for prev_word in window:
                if prev_word in INTENSIFIERS:
                    multiplier *= INTENSIFIERS[prev_word]
                if prev_word in NEGATION_WORDS:
                    is_negated = True

            final_word_score = word_weight * multiplier
            if is_negated:
                # Invert polarity
                final_word_score = -final_word_score * 0.85

            score += final_word_score

        # Normalize score between -1.0 and 1.0
        # Average by word count factor
        normalized = max(-1.0, min(1.0, score / max(2.5, len(words) * 0.35)))

        if normalized > 0.15:
            sentiment: SentimentType = "Positive"
        elif normalized < -0.15:
            sentiment: SentimentType = "Negative"
        else:
            sentiment: SentimentType = "Neutral"

        return sentiment, round(normalized, 3)

    def _extract_themes(self, text: str) -> List[str]:
        """Identify matching themes based on keyword and phrase appearances."""
        lower_text = text.lower()
        matched = []

        for theme, keywords in THEME_KEYWORDS.items():
            for kw in keywords:
                # Use word boundary for short words to avoid false substrings
                if len(kw) <= 4:
                    pattern = rf"\b{re.escape(kw)}\b"
                    if re.search(pattern, lower_text):
                        matched.append(theme)
                        break
                else:
                    if kw in lower_text:
                        matched.append(theme)
                        break

        # Fallback to UI / Order Quality if food or general terms present without specific match
        if not matched:
            if any(w in lower_text for w in ["app", "screen", "button", "slow", "freeze", "desktop", "tab"]):
                matched.append("UI")
            elif any(w in lower_text for w in ["food", "meal", "item", "dish", "product", "box", "package"]):
                matched.append("Order Quality")
            else:
                matched.append("Order Quality")

        return matched

    def _extract_pain_flags(self, text: str, themes: List[str]) -> List[str]:
        """Detect specific pain phrase matches."""
        lower_text = text.lower()
        flags = []
        for theme in themes:
            indicators = THEME_PAIN_INDICATORS.get(theme, [])
            for ind in indicators:
                if ind in lower_text:
                    flags.append(f"{theme}: {ind}")
        return flags

    def analyze_reviews(self, reviews: List[str]) -> AnalysisResponse:
        """Execute complete analysis pipeline over batch of reviews."""
        if not reviews:
            reviews = []

        analyzed_items: List[ReviewItem] = []
        theme_counter = {t: {"count": 0, "pos": 0, "neu": 0, "neg": 0, "severity": 0.0} for t in THEMES}
        pos_total = 0
        neu_total = 0
        neg_total = 0

        for idx, text in enumerate(reviews, start=1):
            cleaned = text.strip()
            if not cleaned:
                continue

            sentiment, score = self._calculate_sentiment(cleaned)
            themes = self._extract_themes(cleaned)
            pain_flags = self._extract_pain_flags(cleaned, themes)

            if sentiment == "Positive":
                pos_total += 1
            elif sentiment == "Negative":
                neg_total += 1
            else:
                neu_total += 1

            for t in themes:
                if t in theme_counter:
                    theme_counter[t]["count"] += 1
                    if sentiment == "Positive":
                        theme_counter[t]["pos"] += 1
                    elif sentiment == "Negative":
                        theme_counter[t]["neg"] += 1
                    else:
                        theme_counter[t]["neu"] += 1

            analyzed_items.append(
                ReviewItem(
                    id=idx,
                    text=cleaned,
                    sentiment=sentiment,
                    sentiment_score=score,
                    themes=themes,
                    pain_flags=pain_flags,
                )
            )

        total_revs = len(analyzed_items)
        if total_revs == 0:
            # Empty fallback
            summary = SentimentSummary(
                total_reviews=0,
                positive_count=0,
                neutral_count=0,
                negative_count=0,
                positive_pct=0.0,
                neutral_pct=0.0,
                negative_pct=0.0,
                net_sentiment_score=0.0,
            )
            brief = ProductBrief(
                title="Product Feedback Analysis Brief",
                executive_summary="No reviews provided for analysis.",
                key_findings=[],
                action_plan=[],
                kpi_targets=[],
                markdown="# Product Feedback Analysis Brief\n\nNo reviews analyzed.",
            )
            return AnalysisResponse(
                sentiment_summary=summary,
                theme_stats=[],
                top_pain_points=[],
                reviews=[],
                product_brief=brief,
                product_opportunities=[],
                user_requests=[],
                roadmap=ProductRoadmap(),
                engine_version="v2.0-product-intelligence",
            )

        pos_pct = round((pos_total / total_revs) * 100, 1)
        neu_pct = round((neu_total / total_revs) * 100, 1)
        neg_pct = round((neg_total / total_revs) * 100, 1)
        net_score = round(pos_pct - neg_pct, 1)

        summary = SentimentSummary(
            total_reviews=total_revs,
            positive_count=pos_total,
            neutral_count=neu_total,
            negative_count=neg_total,
            positive_pct=pos_pct,
            neutral_pct=neu_pct,
            negative_pct=neg_pct,
            net_sentiment_score=net_score,
        )

        # Build ThemeStats
        theme_stats: List[ThemeStat] = []
        for t in THEMES:
            data = theme_counter[t]
            rec = get_theme_recommendation(t)
            weight = rec.get("base_severity_weight", 1.0)
            # Severity formula: emphasizes negative volume and total friction
            sev = round((data["neg"] * 2.5 + data["neu"] * 0.5) * weight, 2)
            data["severity"] = sev

            pct = round((data["count"] / total_revs) * 100, 1) if total_revs > 0 else 0.0
            theme_stats.append(
                ThemeStat(
                    theme=t,
                    count=data["count"],
                    percentage=pct,
                    positive_count=data["pos"],
                    neutral_count=data["neu"],
                    negative_count=data["neg"],
                    severity_score=sev,
                )
            )

        # Sort theme stats by mention count descending
        theme_stats.sort(key=lambda x: x.count, reverse=True)

        # Calculate Top 3 Pain Points (Preserves V1 contract)
        candidates = sorted(
            [t for t in theme_stats if t.count > 0],
            key=lambda x: (x.severity_score, x.negative_count, x.count),
            reverse=True,
        )

        top_candidates = candidates[:3]
        top_pain_points: List[PainPoint] = []

        for rank, cand in enumerate(top_candidates, start=1):
            rec = get_theme_recommendation(cand.theme)
            
            theme_reviews = [
                r.text for r in analyzed_items
                if cand.theme in r.themes and r.sentiment in ["Negative", "Neutral"]
            ]
            if not theme_reviews:
                theme_reviews = [r.text for r in analyzed_items if cand.theme in r.themes]

            quotes = sorted(theme_reviews, key=lambda q: (0 if 30 <= len(q) <= 160 else 1, -len(q)))[:2]

            if rank == 1 or cand.severity_score >= 8.0 or cand.negative_count >= 5:
                priority: PriorityType = "High"
            elif rank == 2 or cand.severity_score >= 4.0 or cand.negative_count >= 2:
                priority: PriorityType = "Medium"
            else:
                priority: PriorityType = "Low"

            top_pain_points.append(
                PainPoint(
                    rank=rank,
                    theme=cand.theme,
                    priority=priority,
                    frequency=cand.count,
                    negative_count=cand.negative_count,
                    severity_score=cand.severity_score,
                    root_cause=rec["root_cause"],
                    representative_quotes=quotes,
                    recommended_feature=rec["recommended_feature"],
                    success_metric=rec["success_metric"],
                )
            )

        # V2: Generate Product Opportunities & Opportunity Scores
        opportunities: List[ProductOpportunity] = self.opportunity_engine.build_opportunities(
            theme_stats=theme_stats,
            reviews=analyzed_items,
            total_reviews=total_revs,
        )

        # V2: Generate 3-Horizon Product Roadmap
        roadmap: ProductRoadmap = self.opportunity_engine.build_roadmap(opportunities)

        # V2: Extract What Users Want (Explicit Feature Requests & Inferred Needs)
        user_requests: List[UserRequestItem] = self.request_extractor.extract_requests(
            reviews=analyzed_items,
            opportunities=opportunities,
        )

        # Generate Executive Product Brief (includes V2 roadmap & opportunity summaries)
        brief = self._generate_product_brief(
            summary=summary,
            theme_stats=theme_stats,
            top_pain_points=top_pain_points,
            opportunities=opportunities,
            roadmap=roadmap,
            user_requests=user_requests,
        )

        return AnalysisResponse(
            sentiment_summary=summary,
            theme_stats=theme_stats,
            top_pain_points=top_pain_points,
            reviews=analyzed_items,
            product_brief=brief,
            product_opportunities=opportunities,
            user_requests=user_requests,
            roadmap=roadmap,
            engine_version="v2.0-product-intelligence",
        )

    def _generate_product_brief(
        self,
        summary: SentimentSummary,
        theme_stats: List[ThemeStat],
        top_pain_points: List[PainPoint],
        opportunities: List[ProductOpportunity],
        roadmap: ProductRoadmap,
        user_requests: List[UserRequestItem],
    ) -> ProductBrief:
        """Generate structured product brief and comprehensive markdown report."""
        now_str = datetime.datetime.now().strftime("%B %d, %Y")
        dominant_theme = theme_stats[0].theme if theme_stats else "N/A"
        dominant_count = theme_stats[0].count if theme_stats else 0

        exec_summary = (
            f"Analysis of {summary.total_reviews} customer feedback reviews reveals a Net Sentiment Score of "
            f"{summary.net_sentiment_score:+0.1f}% ({summary.positive_pct}% positive vs {summary.negative_pct}% negative). "
            f"The primary driver of customer feedback volume is '{dominant_theme}' ({dominant_count} mentions). "
            f"Product Opportunity Scoring (POS) identifies {len(roadmap.now)} critical NOW-horizon initiatives "
            f"that require immediate sprint focus to stem customer churn."
        )

        key_findings = [
            f"**Volume & Sentiment:** Evaluated {summary.total_reviews} reviews ({summary.positive_count} Positive, {summary.neutral_count} Neutral, {summary.negative_count} Negative).",
            f"**Top Opportunity:** '{opportunities[0].theme if opportunities else 'General'}' holds the highest Opportunity Score ({opportunities[0].opportunity_score.total_score if opportunities else 0}/100 - {opportunities[0].opportunity_score.potential_level if opportunities else 'N/A'}).",
            f"**Dominant Theme:** '{dominant_theme}' appeared in {theme_stats[0].percentage if theme_stats else 0}% of all customer reviews.",
            f"**Actionable Horizon:** {len(roadmap.now)} features scheduled for NOW (Sprint 1-2), {len(roadmap.next)} for NEXT, and {len(roadmap.later)} for LATER.",
        ]

        action_plan = []
        kpi_targets = []

        for p in top_pain_points:
            action_plan.append({
                "rank": p.rank,
                "theme": p.theme,
                "priority": p.priority,
                "feature": p.recommended_feature,
                "root_cause": p.root_cause,
            })
            kpi_targets.append(f"**{p.theme}:** {p.success_metric}")

        # Build Markdown Document
        md_lines = [
            f"# Executive Product Brief: Customer Feedback Intelligence (V2)",
            f"**Date:** {now_str} | **Dataset Size:** {summary.total_reviews} reviews | **Net Sentiment Score:** {summary.net_sentiment_score:+0.1f}%\n",
            f"## 1. Executive Summary",
            f"{exec_summary}\n",
            f"## 2. Sentiment Breakdown",
            f"| Metric | Count | Percentage |",
            f"| :--- | :--- | :--- |",
            f"| **Positive Sentiment** | {summary.positive_count} | {summary.positive_pct}% |",
            f"| **Neutral Sentiment** | {summary.neutral_count} | {summary.neutral_pct}% |",
            f"| **Negative Sentiment** | {summary.negative_count} | {summary.negative_pct}% |",
            f"| **Net Sentiment (NPS Proxy)** | - | **{summary.net_sentiment_score:+0.1f}%** |\n",
            f"## 3. Product Opportunity Pipeline & POS Ranking",
            f"| Rank | Theme | Opportunity Score (POS) | Level | Recommended Feature | Horizon |",
            f"| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for o in opportunities:
            md_lines.append(
                f"| #{o.rank} | {o.theme} | **{o.opportunity_score.total_score}/100** | {o.opportunity_score.potential_level} | {o.feature_recommendation} | **{o.roadmap_horizon}** |"
            )

        md_lines.append(f"\n## 4. What Users Want (Top Customer Desires)")
        for req in user_requests[:5]:
            md_lines.append(
                f"- **[{req.request_type}] {req.title}** ({req.mention_count} reviews) ➔ Linked to: *{req.linked_opportunity}* [{req.roadmap_horizon}]"
            )

        md_lines.append(f"\n## 5. Actionable Product Roadmap (3 Horizons)")
        md_lines.append(f"### ⚡ NOW (Immediate Focus)")
        for item in roadmap.now:
            md_lines.append(f"- **[{item.theme}] {item.title}** (POS: {item.opportunity_score}/100) — *Target: {item.success_metric}*")

        md_lines.append(f"\n### ⏳ NEXT (Next Cycle)")
        for item in roadmap.next:
            md_lines.append(f"- **[{item.theme}] {item.title}** (POS: {item.opportunity_score}/100) — *Target: {item.success_metric}*")

        md_lines.append(f"\n### 🔮 LATER (Strategic)")
        for item in roadmap.later:
            md_lines.append(f"- **[{item.theme}] {item.title}** (POS: {item.opportunity_score}/100) — *Target: {item.success_metric}*")

        md_lines.extend([
            f"\n## 6. Measurable Success Metrics (OKRs)",
        ] + [f"- {target}" for target in kpi_targets] + [
            f"\n---\n*Generated by PulsePM Intelligence Engine v2.0 (Autonomous Local Rule Engine)*"
        ])

        markdown_content = "\n".join(md_lines)

        return ProductBrief(
            title="Executive Product Brief: Customer Feedback Intelligence",
            executive_summary=exec_summary,
            key_findings=key_findings,
            action_plan=action_plan,
            kpi_targets=kpi_targets,
            markdown=markdown_content,
        )


