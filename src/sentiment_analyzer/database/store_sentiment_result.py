from supabase import create_client
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

def store_sentiment_result(ticker: str, sentiment_result: dict) -> bool:
    """Store a sentiment analysis result in Supabase."""

    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        data = {
            "ticker": ticker,
            "sentiment": sentiment_result.get("sentiment"),
            "confidence": sentiment_result.get("confidence"),
            "summary": sentiment_result.get("summary")
        }
        client.table("sentiment_results").insert(data).execute()
        logger.info(f"Stored sentiment result for {ticker}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to store sentiment result for {ticker}: {e}")
        return False