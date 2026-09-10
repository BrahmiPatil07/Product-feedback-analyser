"""
Lexicons, taxonomies, and pattern matching rules for sentiment and domain categorization.
Tailored for consumer/food delivery apps (e.g., Zomato, Swiggy, DoorDash) but adaptable to SaaS/e-commerce.
"""

# 8 Core Themes required by user spec
THEMES = [
    "Delivery",
    "Payment",
    "Pricing",
    "UI",
    "Customer Support",
    "Order Quality",
    "Bugs",
    "Offers/Coupons",
]

# High-precision keywords and phrases per theme (Generic across E-Commerce, Food Delivery, SaaS & Mobile Apps)
THEME_KEYWORDS = {
    "Delivery": [
        "delivery", "delayed", "delay", "late", "eta", "driver", "rider", "partner",
        "valet", "on time", "reach", "track", "tracking", "location", "address",
        "took hours", "2 hours", "1 hour", "45 mins", "slow delivery", "waiting",
        "unreachable", "lost", "wrong location", "cancelled by driver", "distance",
        "speed", "express", "dispatch", "doorstep", "shipping", "courier", "courier partner",
        "in transit", "out for delivery", "pickup", "shipment", "package arrival", "delivery date"
    ],
    "Payment": [
        "payment", "upi", "paytm", "gpay", "phonepe", "card", "credit card",
        "debit card", "net banking", "wallet", "charged", "charged twice",
        "double deduction", "money deducted", "deducted", "refund", "refunded",
        "reversal", "transaction", "bank", "failed transaction", "amount",
        "debited", "billing", "checkout payment", "invoice", "auto-debit", "subscription billing"
    ],
    "Pricing": [
        "price", "pricing", "cost", "expensive", "overpriced", "surge", "surge fee",
        "surge charge", "delivery charge", "delivery fee", "platform fee", "hidden charges",
        "handling fee", "packaging charge", "packaging fee", "gst", "taxes", "steep",
        "ripoff", "rip off", "loot", "exorbitant", "costly", "worth", "value for money",
        "cheaper", "subscription price", "tier cost", "renewal price", "premium cost"
    ],
    "UI": [
        "ui", "interface", "design", "layout", "font", "look", "button", "buttons",
        "confusing", "cluttered", "dark mode", "navigation", "search", "filter",
        "filters", "sort", "sorting", "cart ui", "checkout screen", "scrolling",
        "user experience", "ux", "hard to find", "intuitive", "menu", "search bar",
        "tab", "dashboard", "mobile view", "settings screen", "profile page"
    ],
    "Customer Support": [
        "support", "customer support", "customer care", "help center", "chat",
        "chatbot", "bot", "agent", "executive", "representative", "ticket",
        "unhelpful", "rude", "no response", "automated reply", "canned response",
        "resolution", "grievance", "complaint", "call back", "ignore", "loop",
        "bot replies", "helpline", "escalate", "email support", "live agent"
    ],
    "Order Quality": [
        "food", "taste", "quality", "spilled", "spill", "packaging", "package",
        "tampered", "seal", "cold", "ice cold", "stale", "spoiled", "rotten",
        "fresh", "bad taste", "burnt", "undercooked", "raw", "hygiene", "hair",
        "insect", "missing", "wrong item", "item missing", "wrong food", "portion",
        "quantity", "delicious", "yummy", "tasty", "flavour", "flavor", "container",
        "defective", "broken", "damaged item", "fake", "counterfeit", "replica",
        "used product", "scratched", "missing accessory", "poor build"
    ],
    "Bugs": [
        "bug", "bugs", "crash", "crashes", "crashing", "freeze", "freezes",
        "freezing", "stuck", "blank screen", "black screen", "error", "failed to load",
        "not opening", "stuck on splash", "otp", "otp not coming", "location error",
        "glitch", "glitches", "force close", "not responding", "reload", "white screen",
        "server error", "500", "404", "sync failed", "export failed", "login failed"
    ],
    "Offers/Coupons": [
        "coupon", "coupons", "offer", "offers", "discount", "promo", "promo code",
        "code", "voucher", "cashback", "deal", "deals", "gold", "membership",
        "fake discount", "not applied", "invalid code", "coupon failed",
        "misleading offer", "terms and conditions", "scam offer", "expired",
        "prime discount", "cashback rejected", "referral reward"
    ],
}

# Lexicon of positive tokens and associated intensity weights
POSITIVE_WORDS = {
    "excellent": 1.5, "amazing": 1.5, "awesome": 1.4, "fantastic": 1.4,
    "superb": 1.4, "wonderful": 1.3, "outstanding": 1.5, "brilliant": 1.4,
    "delicious": 1.3, "tasty": 1.1, "yummy": 1.1, "fresh": 1.0,
    "fast": 1.0, "quick": 1.0, "prompt": 1.1, "punctual": 1.1, "superfast": 1.4,
    "good": 0.8, "great": 1.2, "loved": 1.2, "love": 1.1, "best": 1.3,
    "smooth": 1.0, "seamless": 1.2, "polite": 1.0, "courteous": 1.1,
    "helpful": 1.1, "clean": 0.9, "neat": 0.8, "perfect": 1.4,
    "satisfied": 1.0, "happy": 1.0, "impressed": 1.2, "worth": 0.9,
    "appreciate": 1.0, "recommend": 1.2, "friendly": 1.0, "hot": 0.7,
    "crispy": 0.8, "easy": 0.8, "convenient": 0.9, "reliable": 1.1,
    "sturdy": 1.0, "genuine": 1.2, "original": 1.1, "durable": 1.2,
}

# Lexicon of negative tokens and associated intensity weights
NEGATIVE_WORDS = {
    "terrible": -1.5, "horrible": -1.5, "worst": -1.6, "pathetic": -1.5,
    "disgusting": -1.5, "useless": -1.4, "waste": -1.4, "loot": -1.4,
    "fraud": -1.6, "scam": -1.6, "cheated": -1.5, "awful": -1.4,
    "bad": -0.9, "poor": -1.0, "late": -1.0, "delayed": -1.0,
    "cold": -0.8, "spilled": -1.2, "spill": -1.1, "stale": -1.3,
    "rotten": -1.5, "spoiled": -1.5, "burnt": -1.1, "undercooked": -1.2,
    "missing": -1.1, "unhelpful": -1.2, "rude": -1.4, "crash": -1.2,
    "crashed": -1.3, "crashing": -1.3, "freeze": -1.1, "glitch": -1.0,
    "bug": -1.0, "failed": -1.1, "fail": -1.0, "failure": -1.1,
    "slow": -0.8, "expensive": -0.9, "overpriced": -1.1, "exorbitant": -1.3,
    "annoying": -1.0, "frustrated": -1.2, "frustrating": -1.2, "disappointed": -1.2,
    "disappointment": -1.2, "hate": -1.3, "unacceptable": -1.4, "horrid": -1.4,
    "never": -0.7, "wrong": -0.9, "error": -1.0, "stuck": -1.0, "ignored": -1.1,
    "defective": -1.4, "broken": -1.3, "fake": -1.5, "counterfeit": -1.6, "damaged": -1.3,
}

# Intensifiers multiplier
INTENSIFIERS = {
    "very": 1.5, "extremely": 2.0, "super": 1.5, "totally": 1.6,
    "completely": 1.6, "absolutely": 1.8, "highly": 1.4, "really": 1.3,
    "so": 1.3, "utterly": 1.9, "terribly": 1.8, "deeply": 1.4,
}

# Negation words that flip polarity
NEGATION_WORDS = {
    "not", "no", "never", "hardly", "barely", "scarcely", "neither",
    "nor", "without", "didn't", "wasn't", "weren't", "couldn't",
    "won't", "wouldn't", "don't", "doesn't", "isn't", "aren't",
    "haven't", "hasn't", "hadn't", "cannot", "cant", "wont"
}

# Theme-specific severity indicators for pain point ranking (Cross-product)
THEME_PAIN_INDICATORS = {
    "Delivery": ["took 2 hours", "late", "delayed", "rider unreachable", "never arrived", "cold food", "lost location", "shipping delayed", "package lost", "delivery failed"],
    "Payment": ["double deduction", "charged twice", "refund not received", "money deducted", "failed payment", "bank debited", "auto-renewal without notice"],
    "Pricing": ["surge fee", "hidden charges", "exorbitant", "loot", "ripoff", "packaging fee high", "unreasonable pricing", "overpriced"],
    "UI": ["cannot find", "confusing", "cluttered", "checkout stuck", "bad layout", "hard to navigate", "search not working"],
    "Customer Support": ["useless bot", "agent disconnected", "no reply", "ticket closed without resolution", "canned response", "rude executive", "no phone support"],
    "Order Quality": ["tampered packaging", "spilled all over", "hair in food", "stale food", "missing items", "wrong order", "defective item", "broken product", "fake duplicate"],
    "Bugs": ["app crashed", "blank screen", "stuck on checkout", "otp failed", "server error", "force close", "sync failed"],
    "Offers/Coupons": ["fake discount", "coupon invalid", "misleading cashback", "code expired immediately", "promo revoked"],
}

# Linguistic patterns indicating explicit user feature requests / suggestions
INTENT_REQUEST_PATTERNS = [
    r"(?:please\s+add|we\s+need|i\s+wish\s+(?:there\s+was|it\s+had)|should\s+have|should\s+allow|why\s+can't\s+we|would\s+be\s+great\s+if|bring\s+back|give\s+(?:an?\s+)?option\s+to|needs?\s+a|option\s+for|feature\s+request|allow\s+us\s+to|make\s+it\s+(?:possible|easier)\s+to)\s+([^.,;!?]+)",
    r"(?:would\s+love\s+to\s+see|can\s+you\s+add|hope\s+you\s+add|add\s+a\s+feature\s+to)\s+([^.,;!?]+)"
]

