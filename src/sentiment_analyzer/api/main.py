from fastapi import FastAPI
from supabase import create_client
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

app = FastAPI()
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

@app.get("/sentiments")
def get_all_sentiments():
    """Return all sentiment results from Supabase."""
    try:
        response = supabase.table("sentiment_results").select("*").execute()
        logger.info("Fetched all sentiment results")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch sentiments: {e}")
        return []
    

@app.get("/sentiments/{ticker}")
def get_sentiment_by_ticker(ticker: str):
    """Return sentiment results for a specific stock ticker."""
    try:
        response = supabase.table("sentiment_results").select("*").eq("ticker", ticker).execute()
        logger.info(f"Fetched sentiment results for {ticker}")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch sentiments for {ticker}: {e}")
        return []