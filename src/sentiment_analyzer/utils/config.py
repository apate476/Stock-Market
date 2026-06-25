import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
FMP_API_KEY = os.environ.get("FMP_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Personal watchlist
PERSONAL_TICKERS: list[str] = ["NVDA", "SPCX", "MSFT", "BRK-B", "JPM"]