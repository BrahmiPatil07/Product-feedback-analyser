# PulsePM — Product Feedback Intelligence Platform ⚡

> **A portfolio-grade Product Intelligence & Opportunity Discovery platform built with Python (FastAPI), modern responsive Vanilla CSS/JS, and an offline-first rule engine with an extensible AI/LLM architecture.**
> **Works across any consumer app or B2B software (Zomato, Swiggy, Amazon, Flipkart, SaaS platforms).**

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)
![Zero API Cost](https://img.shields.io/badge/Cost-100%25%20Free%20%26%20Offline-brightgreen.svg)
![Architecture](https://img.shields.io/badge/Architecture-Clean%20%2F%20Adapter%20Pattern-blueviolet.svg)
![Tests](https://img.shields.io/badge/Tests-12%20Passed-success.svg)

---

## 📌 Problem & Value Proposition
Product Managers and Engineering leads often drown in hundreds of fragmented app store reviews, support tickets, and NPS comments. 

**PulsePM (V2)** transforms raw feedback into an actionable, prioritized **Product Innovation Engine**:
1. **Generic Cross-Domain Analysis**: Works seamlessly for Food Delivery (Zomato, Swiggy), E-Commerce (Amazon, Flipkart), and SaaS platforms (B2B software).
2. **Product Opportunity Pipeline**: Maps the full innovation chain:
   $$\text{Review Evidence} \longrightarrow \text{Domain Theme} \longrightarrow \text{Pain Point} \longrightarrow \text{Root Cause Hypothesis} \longrightarrow \text{Product Opportunity} \longrightarrow \text{Feature Recommendation}$$
3. **Product Opportunity Score (POS)**: Ranks every opportunity on a transparent 0–100 scale based on:
   - **Frequency Score (0–30)**: Volume and proportion of affected users.
   - **Severity Score (0–40)**: Friction intensity and negative sentiment density.
   - **User Impact Score (0–30)**: Criticality to core retention and conversion funnels.
4. **Empirical Evidence**: Every recommendation is backed by exact review counts, percentage of feedback, verbatim customer voices, and explicit PM rationale.
5. **"What Users Want" Discovery**: Automatically separates **Explicit Feature Requests** (asked by users) from **Inferred Needs** (friction-derived desires) with quote evidence.
6. **Actionable 3-Horizon Product Roadmap**: Organizes feature initiatives into **⚡ NOW** (immediate sprint blockers), **⏳ NEXT** (next cycle UX & flow wins), and **🔮 LATER** (strategic horizon & scale).
7. **Executive Product Brief**: Downloadable and copyable PM summary with OKR target sheets.

---

## 🏛️ System Architecture

PulsePM follows clean architectural principles with an **Adapter Pattern**, separating intelligence engines from presentation:

```
                          ┌───────────────────────────────┐
                          │     Frontend Dashboard UI     │
                          │   HTML5 + Vanilla CSS + JS    │
                          │ (Roadmap, Opportunities, WUW) │
                          └───────────────┬───────────────┘
                                          │ HTTP REST (JSON)
                                          ▼
                          ┌───────────────────────────────┐
                          │      FastAPI REST Server      │
                          │     (/api/analyze, /sample)   │
                          └───────────────┬───────────────┘
                                          │
                         ┌────────────────▼────────────────┐
                         │    <<BaseFeedbackAnalyzer>>     │
                         │      (Abstract Interface)       │
                         └───────┬──────────────────┬──────┘
                                 │                  │
           ┌─────────────────────▼───┐          ┌───▼─────────────────────┐
           │   RuleBasedAnalyzer     │          │   AIAnalyzerAdapter     │
           │  (Offline Rule Engine)  │          │ (Stub for Gemini/OpenAI │
           └──────────────┬──────────┘          │  Extensible Integration)│
                          │                     └─────────────────────────┘
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
┌───────────────┐ ┌───────────────┐ ┌─────────────────┐
│ Opportunity   │ │ Request       │ │ Lexicons &      │
│ Engine (POS)  │ │ Extractor     │ │ Recommendations │
└───────────────┘ └───────────────┘ └─────────────────┘
```

---

## ✨ Key Capabilities & Features

### 1. Multi-Domain Sample Datasets (1-Click Instant Demo)
* 🍕 **Zomato (Food Delivery)**: 25 authentic reviews spanning delivery delays, cold food, payment double deductions, and support bot loops.
* 📦 **Amazon (E-Commerce / Retail)**: 20 authentic reviews covering counterfeit items, shipping courier delays, return policy disputes, and search filters.
* 💻 **SaaS (Productivity App)**: 15 authentic reviews covering CSV export failures, auto-renewal price jumps, dark mode requests, and SAML SSO support.

### 2. Product Opportunity Scoring (POS) Model
Unlike basic sentiment tools, PulsePM evaluates business viability through the **Product Opportunity Score (0–100)**:
$$\text{POS} = \min(100, \text{Frequency Score (0–30)} + \text{Severity Score (0–40)} + \text{User Impact Score (0–30)})$$
* Categorizes opportunities into **Critical Opportunity**, **High Opportunity**, or **Medium Opportunity**.
* Accompanied by full evidence: supporting review count, %, verbatim quotes, and recommendation rationale.

### 3. "What Users Want" (Explicit Requests vs. Inferred Needs)
* **Explicit Requests**: Extracts feature suggestions directly requested by users (*"please add dark mode"*, *"we need a filter for third-party sellers"*, *"should allow scheduled delivery"*).
* **Inferred Needs**: Discovers latent product needs derived from recurring user friction (*"1-Click Human Support Escalation"* derived from bot loops).
* Filterable in real-time with review count badges and linked roadmap initiatives.

### 4. 3-Horizon Actionable Roadmap
* **⚡ NOW**: Critical fixes and payment/checkout blocker mitigations.
* **⏳ NEXT**: Flow optimizations, transparency enhancements, and quality seals.
* **🔮 LATER**: Strategic platform redesigns, automated coupon engines, and scale features.

### 5. Preserved Core Analytics
* Sentiment distribution Donut Chart with Net Sentiment Score (% Positive − % Negative).
* 8-theme mention frequency & friction bars.
* Top 3 prioritized pain points with High/Medium/Low priority badges.
* Interactive Review Explorer with live keyword search, sentiment filter pills, and theme selector.
* Executive Product Brief with 1-click Markdown copy and print/PDF formatting.

---

## 🚀 Quickstart (1-Minute Setup)

### 1. Clone & Install
```bash
git clone https://github.com/your-username/product-feedback-analyser.git
cd "product-feedback-analyser"
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python run.py
```
* Dashboard URL: **`http://127.0.0.1:8000`**
* Interactive API Documentation: **`http://127.0.0.1:8000/docs`**

---

## 🧪 Automated Testing (12/12 Passed)

Run the test suite:
```bash
python -m pytest -v
```

### Verified Test Cases:
* `test_parse_raw_reviews`: Multi-line and bulleted string ingestion.
* `test_sentiment_classification_basic`: Polarity detection for positive, neutral, negative text.
* `test_sentiment_negation_handling`: Contextual negation flips (*"not good"*, *"not bad"*).
* `test_theme_categorization`: Accurate tagging across all 8 domain taxonomies.
* `test_full_zomato_sample_analysis`: End-to-end pipeline analysis on 25 reviews.
* `test_v2_opportunity_scoring_and_chains`: Validation of Opportunity Score (POS) formula and evidence structure.
* `test_v2_what_users_want_extraction`: Verification of explicit user requests vs. inferred needs extraction.
* `test_v2_actionable_roadmap_categorization`: 3-horizon NOW / NEXT / LATER roadmap assignment.
* `test_health_check`: Service availability and engine readiness.
* `test_get_sample_reviews`: Multi-dataset delivery (Zomato, Amazon, SaaS).
* `test_analyze_endpoint_with_raw_text`: REST API POST contract.
* `test_analyze_endpoint_empty_error`: Graceful 400 error handling.

---

## 📁 Repository Structure

```
product feedback ana/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI REST API & static server
│   ├── models.py                   # Pydantic schemas (Opportunity, Roadmap, UserRequest, etc.)
│   ├── sample_data.py              # Multi-domain datasets (Zomato, Amazon, SaaS)
│   └── analyzer/
│       ├── __init__.py
│       ├── base.py                 # Abstract Base Class (Adapter Pattern)
│       ├── rule_engine.py          # Master analysis orchestrator
│       ├── opportunity_engine.py   # POS Calculator, Opportunity Chains & Roadmap Builder
│       ├── request_extractor.py    # Explicit requests vs Inferred needs extractor
│       ├── lexicons.py             # Cross-domain theme taxonomies & intent patterns
│       ├── recommendations.py      # Knowledge base for PM fixes & success metrics
│       └── ai_adapter.py           # Future LLM/AI expansion adapter
├── static/
│   ├── index.html                  # Accessible UI with Opportunity, WUW & Roadmap sections
│   ├── css/
│   │   └── styles.css              # Custom Vanilla CSS design system (Dark Mode Glassmorphism)
│   └── js/
│       ├── charts.js               # Pure SVG donut chart & animated theme bars
│       └── app.js                  # Frontend state, dataset switcher, POS renderers
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py            # Unit tests for POS, requests, roadmap, and NLP
│   └── test_api.py                 # API integration tests
├── run.py                          # 1-command startup script
├── requirements.txt                # Lightweight dependencies
└── README.md                       # Documentation & portfolio guide
```

---

## 💼 LinkedIn & Portfolio Showcase Points

* **Strategic Product Thinking**: Demonstrates understanding of how unstructured user voice translates into structured product opportunities, Opportunity Scores (Frequency × Severity × Impact), and a 3-horizon execution roadmap.
* **Separation of Explicit vs. Inferred Needs**: Shows maturity in product discovery by distinguishing what users literally say from the underlying system friction.
* **Clean Code & Architecture**: Pure Python & Vanilla CSS/JS without framework bloat, 100% test coverage, and offline-first reliability.

---

## 📄 License
MIT License. Free for educational, portfolio, and commercial use.
