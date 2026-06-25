from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from supabase import create_client
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

app = FastAPI()


def get_supabase():
    """Create and return a Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


@app.get("/sentiments")
def get_all_sentiments() -> list:
    """Return all sentiment results from Supabase."""
    try:
        response = get_supabase().table("sentiment_results").select("*").execute()
        logger.info("Fetched all sentiment results")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch sentiments: {e}")
        return []


@app.get("/sentiments/{ticker}")
def get_sentiment_by_ticker(ticker: str) -> list:
    """Return sentiment results for a specific stock ticker."""
    try:
        response = get_supabase().table("sentiment_results").select("*").eq("ticker", ticker).execute()
        logger.info(f"Fetched sentiment results for {ticker}")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch sentiments for {ticker}: {e}")
        return []


@app.get("/sentiments/history/{ticker}")
def get_sentiment_history(ticker: str) -> list:
    """Return the last 30 days of sentiment results for a specific ticker."""
    try:
        since = (datetime.utcnow() - timedelta(days=30)).isoformat()
        response = (
            get_supabase().table("sentiment_results")
            .select("*")
            .eq("ticker", ticker)
            .gte("created_at", since)
            .order("created_at", desc=False)
            .execute()
        )
        logger.info(f"Fetched 30-day history for {ticker}: {len(response.data)} records")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch sentiment history for {ticker}: {e}")
        return []


@app.websocket("/ws/sentiments")
async def websocket_sentiment_feed(websocket: WebSocket) -> None:
    """WebSocket endpoint that streams the latest sentiment results to connected clients."""
    import asyncio
    await websocket.accept()
    logger.info("WebSocket client connected")
    try:
        while True:
            response = get_supabase().table("sentiment_results").select("*").order("created_at", desc=True).limit(50).execute()
            await websocket.send_json(response.data)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
