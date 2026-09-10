"""
1-Click Launcher for Product Feedback Analyser
Runs the FastAPI server and serves the dashboard locally.
"""

import sys
import webbrowser
import uvicorn

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"

    print("=" * 65)
    print("🚀 PulsePM: Product Feedback Analyser (V2)")
    print("   Portfolio-Grade Sentiment & Theme Analysis System")
    print("=" * 65)
    print(f"📡 Server starting on : {url}")
    print(f"📖 API Documentation : {url}/docs")
    print(f"🎯 Offline Rule Engine: Ready (0 API Keys required)")
    print("=" * 65)

    # Open browser automatically if running interactively
    if "--no-browser" not in sys.argv:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
