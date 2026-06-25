from newsapi import NewsApiClient
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import NEWS_API_KEY

def fetch_financial_news(ticker: str) -> list[dict]:
    """Fetch latest financial news articles for a given stock ticker."""
    try:
        client = NewsApiClient(api_key=NEWS_API_KEY)
        response = client.get_everything(q=ticker, language="en", sort_by="publishedAt", page_size=10)
        articles = response.get("articles", [])
        logger.info(f"Fetched {len(articles)} articles for {ticker}")
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch news for {ticker}: {e}")
        return []
    