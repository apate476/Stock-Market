import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    """Get a required environment variable or raise an error."""
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY") or ""
NEWS_API_KEY: str = os.environ.get("NEWS_API_KEY") or ""
FMP_API_KEY: str = os.environ.get("FMP_API_KEY") or ""
SUPABASE_URL: str = os.environ.get("SUPABASE_URL") or ""
SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY") or ""
EMAIL_SENDER: str = os.environ.get("EMAIL_SENDER") or ""
EMAIL_PASSWORD: str = os.environ.get("EMAIL_PASSWORD") or ""
SLACK_WEBHOOK_URL: str = os.environ.get("SLACK_WEBHOOK_URL") or ""

# Personal watchlist
PERSONAL_TICKERS: list[str] = ["NVDA", "SPCX", "MSFT", "BRK-B", "JPM"]