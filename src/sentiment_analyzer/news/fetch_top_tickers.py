import requests
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import FMP_API_KEY

FMP_MOST_ACTIVE_URL = "https://financialmodelingprep.com/api/v3/stock_market/actives"


def fetch_top_tickers() -> list[str]:
    """Fetch the top 10 most actively traded stock tickers by volume from FMP."""
    try:
        response = requests.get(FMP_MOST_ACTIVE_URL, params={"apikey": FMP_API_KEY})
        response.raise_for_status()
        data = response.json()
        tickers = [stock["symbol"] for stock in data[:10]]
        logger.info(f"Fetched top tickers: {tickers}")
        return tickers
    except Exception as e:
        logger.error(f"Failed to fetch top tickers: {e}")
        return []
