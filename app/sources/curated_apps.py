"""
Curated App Registry & Offline Fallback Reviews.
Contains pre-mapped metadata and Apple App Store Track IDs for 22 tier-1 applications
across Food, Quick Commerce, E-Commerce, Fintech, Ride Hailing, Streaming, and Social domains.
"""

from typing import List, Dict, Optional

CURATED_APPS: List[Dict] = [
    # Food & Quick Commerce
    {
        "product_id": "434613896",
        "product_name": "Zomato",
        "full_name": "Zomato: Food Delivery & Dining",
        "category": "Food & Grocery",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/c2/91/b1/c291b19d-1e9c-f614-ae13-6bb94f706a1a/AppIcon-0-0-1x_U007ephone-0-1-0-sRGB-85-220.png/100x100bb.jpg",
        "developer": "Zomato Media Pvt. Ltd.",
        "rating": 4.7,
        "badge": "Popular",
    },
    {
        "product_id": "989540920",
        "product_name": "Swiggy",
        "full_name": "Swiggy: Food Instamart Dineout",
        "category": "Food & Grocery",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/3a/b8/8b/3ab88b64-1a2b-9c4c-e230-1565dd6470a1/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "BUNDL TECHNOLOGIES",
        "rating": 4.4,
        "badge": "Trending",
    },
    {
        "product_id": "960335206",
        "product_name": "Blinkit",
        "full_name": "Blinkit: Groceries & more",
        "category": "Food & Grocery",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/bf/ee/a9/bfeea96c-e7dc-9671-45c6-b9752f19f801/AppIcon-0-0-1x_U007ephone-0-1-0-sRGB-85-220.png/100x100bb.jpg",
        "developer": "BLINK COMMERCE",
        "rating": 4.7,
        "badge": "10-Min",
    },
    {
        "product_id": "1575323645",
        "product_name": "Zepto",
        "full_name": "Zepto: Groceries in minutes",
        "category": "Food & Grocery",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/a8/30/c9/a830c92f-e5aa-6548-e946-ba866548bb70/Default-0-0-1x_U007emarketing-0-7-0-85-220.png/100x100bb.jpg",
        "developer": "KIRANAKART",
        "rating": 4.7,
        "badge": "Quick Comm",
    },

    # E-Commerce & Retail
    {
        "product_id": "1478350915",
        "product_name": "Amazon",
        "full_name": "Amazon India Shop, Pay, miniTV",
        "category": "E-Commerce",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/38/de/b7/38deb703-d67b-d7f3-eba0-9723503eb8b9/AppIcon-0-0-1x_U007epad-0-1-0-sRGB-0-85-220.png/100x100bb.jpg",
        "developer": "Amazon",
        "rating": 4.6,
        "badge": "Global Leader",
    },
    {
        "product_id": "742044692",
        "product_name": "Flipkart",
        "full_name": "Flipkart - Online Shopping App",
        "category": "E-Commerce",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/92/50/1f/92501f3e-b9a5-ed02-bb25-a40c81b05653/AppIcon-fk-0-0-1x_U007epad-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "Flipkart Internet",
        "rating": 4.6,
        "badge": "E-Commerce",
    },
    {
        "product_id": "907394059",
        "product_name": "Myntra",
        "full_name": "Myntra - Fashion Shopping App",
        "category": "E-Commerce",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/af/87/fa/af87fa19-9d6c-aa3a-2103-add2bb7395e5/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "Myntra Designs",
        "rating": 4.7,
        "badge": "Fashion",
    },
    {
        "product_id": "1457958492",
        "product_name": "Meesho",
        "full_name": "Meesho: Online Shopping",
        "category": "E-Commerce",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/87/57/05/87570565-deac-353f-cc05-9ef1aa08a04e/AppIcon-0-0-1x_U007ephone-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "Meesho Inc.",
        "rating": 4.6,
        "badge": "Social Commerce",
    },

    # Mobility & Ride Hailing
    {
        "product_id": "368677368",
        "product_name": "Uber",
        "full_name": "Uber - Request a ride",
        "category": "Ride Hailing",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/8f/15/52/8f15523c-afce-94bc-2d05-c1b8eb41f577/AppIcon-0-0-1x_U007emarketing-0-8-0-0-85-220.png/100x100bb.jpg",
        "developer": "Uber Technologies",
        "rating": 4.8,
        "badge": "Mobility",
    },
    {
        "product_id": "539179365",
        "product_name": "Ola",
        "full_name": "Ola: Book Cab, Auto, Bike Taxi",
        "category": "Ride Hailing",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/2f/a1/34/2fa13424-bd72-6d06-06fc-aa71d8949387/AppIcon-0-0-1x_U007emarketing-0-5-0-sRGB-0-85-220.png/100x100bb.jpg",
        "developer": "ANI Technologies",
        "rating": 4.6,
        "badge": "Cabs & Auto",
    },

    # Fintech & Payments
    {
        "product_id": "1170055821",
        "product_name": "PhonePe",
        "full_name": "PhonePe: UPI, Gold, Insurance",
        "category": "Fintech",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/7f/3d/3c/7f3d3c97-f3f7-7c2a-0223-8388a2de1f21/AppIcon-0-0-1x_U007emarketing-0-6-0-85-220.png/100x100bb.jpg",
        "developer": "PhonePe Private Limited",
        "rating": 4.7,
        "badge": "Fintech UPI",
    },
    {
        "product_id": "1193357041",
        "product_name": "Google Pay",
        "full_name": "Google Pay: Save, Pay, Manage",
        "category": "Fintech",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/72/80/41/7280412d-8a61-b5e6-e0f5-9eb2ba644dcc/GPayAppIcon-0-0-1x_U007ephone-0-0-0-1-0-0-0-85-220.png/100x100bb.jpg",
        "developer": "Google LLC",
        "rating": 4.6,
        "badge": "UPI & Banking",
    },
    {
        "product_id": "473941634",
        "product_name": "Paytm",
        "full_name": "Paytm: Secure UPI Payments",
        "category": "Fintech",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/5c/bc/a5/5cbca589-b886-4108-92b0-568407edc509/AppIcon-0-0-1x_U007ephone-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "One97 Communications",
        "rating": 4.7,
        "badge": "Wallet & UPI",
    },

    # Streaming & Media
    {
        "product_id": "324684580",
        "product_name": "Spotify",
        "full_name": "Spotify: Music and Podcasts",
        "category": "Streaming & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/6d/e0/d6/6de0d66e-e40d-1cb9-a6cc-031808eeab93/AppIcon-0-0-1x_U007epad-0-1-0-0-sRGB-85-220.png/100x100bb.jpg",
        "developer": "Spotify AB",
        "rating": 4.6,
        "badge": "Audio Streaming",
    },
    {
        "product_id": "363590051",
        "product_name": "Netflix",
        "full_name": "Netflix",
        "category": "Streaming & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/0f/c6/b7/0fc6b7ab-2d8e-b79c-012d-db6701b071d7/AppIcon-0-0-1x_U007epad-0-1-0-sRGB-0-85-220.png/100x100bb.jpg",
        "developer": "Netflix, Inc.",
        "rating": 4.7,
        "badge": "OTT Video",
    },
    {
        "product_id": "544007664",
        "product_name": "YouTube",
        "full_name": "YouTube: Watch, Listen, Stream",
        "category": "Streaming & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/be/49/dd/be49dddb-168f-685c-49a7-d7358d2b6684/logo_youtube_2024_q4_color-0-0-1x_U007emarketing-0-0-0-7-0-0-0-85-220.png/100x100bb.jpg",
        "developer": "Google LLC",
        "rating": 4.6,
        "badge": "Video Platform",
    },

    # Social & Media
    {
        "product_id": "389801252",
        "product_name": "Instagram",
        "full_name": "Instagram",
        "category": "Social & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/5a/18/99/5a189914-fa88-fab3-7ce2-506a624d2fbf/Prod-0-0-1x_U007epad-0-1-0-sRGB-85-220.png/100x100bb.jpg",
        "developer": "Instagram, Inc.",
        "rating": 4.7,
        "badge": "Social",
    },
    {
        "product_id": "310633997",
        "product_name": "WhatsApp",
        "full_name": "WhatsApp Messenger",
        "category": "Social & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/06/ee/d1/06eed185-996b-bd98-b5c4-36b365f93e08/AppIcon-0-0-1x_U007epad-0-0-0-1-0-0-sRGB-0-85-220.png/100x100bb.jpg",
        "developer": "WhatsApp LLC",
        "rating": 4.6,
        "badge": "Messaging",
    },
    {
        "product_id": "447188370",
        "product_name": "Snapchat",
        "full_name": "Snapchat: Chat with friends",
        "category": "Social & Media",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/00/59/bb/0059bb41-25d1-e054-dd32-979ff089b7cb/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/100x100bb.jpg",
        "developer": "Snap, Inc.",
        "rating": 4.7,
        "badge": "Stories & AR",
    },

    # Professional & Learning & Navigation
    {
        "product_id": "288429040",
        "product_name": "LinkedIn",
        "full_name": "LinkedIn: Community & Career",
        "category": "Professional & Learning",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/33/84/08/338408be-ec36-20d0-8d6f-727a92af5481/AppIcon-0-0-1x_U007emarketing-0-8-0-85-220.png/100x100bb.jpg",
        "developer": "LinkedIn Corporation",
        "rating": 4.7,
        "badge": "Professional",
    },
    {
        "product_id": "570060128",
        "product_name": "Duolingo",
        "full_name": "Duolingo: Language & Chess",
        "category": "Professional & Learning",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/1c/19/70/1c19704d-b48e-5c5d-78d5-d1d5ed601474/AppIcon-0-0-1x_U007epad-0-1-85-220.png/100x100bb.jpg",
        "developer": "Duolingo Inc.",
        "rating": 4.7,
        "badge": "EdTech",
    },
    {
        "product_id": "585027354",
        "product_name": "Google Maps",
        "full_name": "Google Maps: Navigation & Transit",
        "category": "Navigation & Maps",
        "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/6b/92/a1/6b92a154-ea3c-029f-85a4-96ed19a5f685/maps_2025-0-0-1x_U007epad-0-0-0-1-0-0-sRGB-0-0-85-220.png/100x100bb.jpg",
        "developer": "Google LLC",
        "rating": 4.7,
        "badge": "Maps & GPS",
    },
]

# Offline fallback authentic review datasets for resilience
SPOTIFY_FALLBACK_REVIEWS = [
    "The new UI update completely ruined my customized playlists and hides the search bar inside another tab. Very confusing design.",
    "Constant audio playback stuttering and songs stop playing abruptly when the phone screen is locked. Please fix this bug!",
    "Spotify Premium subscription price was increased again, yet offline downloading keeps failing and un-downloading my saved songs.",
    "Sound quality on High Bitrate is outstanding! The weekly Discover playlist recommendations are remarkably accurate.",
    "Customer support chatbot is completely unhelpful. It took 3 days and multiple emails to get a refund for an accidental double charge.",
    "Please add an option to disallow explicit songs without completely disabling artist radio recommendations.",
    "The lyrics feature constantly loses sync with the singer's voice by 4-5 seconds. Very annoying during karaoke.",
    "Super clean desktop player interface! Connecting between my MacBook, iPhone, and smart speaker works seamlessly.",
    "Too many unskippable podcast advertisements even on my paid Premium subscription tier! Why am I paying if ads still play?",
    "Search filter for genres and moods is broken on the latest update. It keeps reloading to the home tab.",
    "App crashes repeatedly whenever I connect to my car via Bluetooth. Had to reinstall twice.",
    "Great collaborative playlist feature! My friends and I had a blast creating a road trip mix together.",
    "Payment was deducted from my UPI account for Premium renewal but account stayed Free tier for 24 hours.",
    "We need a feature to block specific artists from ever appearing in algorithmically generated mixes.",
    "Battery drain is huge on iOS 17. Spotify drains 30% battery in just 45 minutes of background playback."
]

SWIGGY_FALLBACK_REVIEWS = [
    "Ordered lunch at 1 PM, driver took 75 minutes to reach because the app gave him a completely wrong map pin. Food arrived cold.",
    "Swiggy One membership promises free delivery, but surge charges and handling fees of 55 rupees were added at checkout.",
    "Payment debited from Google Pay wallet twice, order status said cancelled, and now support is telling me to wait 5-7 days.",
    "Food packaging from restaurant was leaking oil and the paper box was crushed. Very poor courier handling.",
    "Instant 15-minute delivery on Instamart! Rider was courteous and delivered fresh fruits right to my door.",
    "Chat support closed my ticket regarding stale biryani without letting me attach photo proof or speaking to an executive.",
    "App crashes every time I tap on the discount coupon section. Extremely laggy checkout flow.",
    "Delicious butter chicken and hot garlic naan, packaging was sealed tight with security stickers.",
    "Promo code SWIGGYIT showed 100 off on restaurant page, but disappeared on the final payment gateway screen.",
    "Please add a filter to show only 100% vegetarian pure veg restaurants without mixing them in general search results."
]

UBER_FALLBACK_REVIEWS = [
    "Driver accepted the ride and stood still 2 km away for 20 minutes waiting for me to cancel so he could pocket the cancellation fee.",
    "Fare surged from 250 to 580 rupees just because it started drizzling! Price gouging is getting out of hand.",
    "App crashed twice while selecting payment option and charged my credit card without generating a trip PIN.",
    "Driver was very professional, car was spotless and AC was cooling nicely. Reached airport right on schedule.",
    "Support bot repeatedly refused to refund the cancellation fee despite driver refusing to move. Need direct human support.",
    "GPS tracking showed driver moving on a highway in opposite direction. ETA kept jumping from 5 mins to 25 mins.",
    "Please add an option to request quiet rides or drivers with high ratings only.",
    "Payment failed on UPI at end of trip, had to pay cash, and now Uber has marked the trip unpaid with an outstanding balance.",
    "Super smooth booking experience and driver arrived in 3 minutes. Clean sedan and polite driver.",
    "Frequent OTP verification delays cause rides to be cancelled at pickup points."
]


def get_curated_apps() -> List[Dict]:
    """Retrieve list of all 22 curated applications."""
    return CURATED_APPS


def get_app_by_id(product_id: str) -> Optional[Dict]:
    """Find a curated app by its Apple App Store Track ID."""
    for app in CURATED_APPS:
        if app["product_id"] == str(product_id):
            return app
    return None


def get_curated_reviews_fallback(product_name: str) -> List[str]:
    """Provide authentic fallback reviews for resilient offline demo mode."""
    name_lower = product_name.lower().strip()
    if "spotify" in name_lower:
        return SPOTIFY_FALLBACK_REVIEWS
    elif "swiggy" in name_lower or "blinkit" in name_lower or "zepto" in name_lower:
        return SWIGGY_FALLBACK_REVIEWS
    elif "uber" in name_lower or "ola" in name_lower:
        return UBER_FALLBACK_REVIEWS
    else:
        from app.sample_data import SAMPLE_ZOMATO_REVIEWS
        return SAMPLE_ZOMATO_REVIEWS
