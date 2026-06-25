import json
import anthropic
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import ANTHROPIC_API_KEY


def analyze_sentiment(article: dict) -> dict:
    """Analyze the sentiment of a financial news article using Claude."""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = f"""Analyze this financial news article and return a JSON response with exactly these fields:
        - sentiment: either "bullish", "bearish", or "neutral"
        - confidence: a number between 0 and 100
        - summary: a 1-2 sentence summary of the article
        - recommendation: either "buy", "hold", or "watch"

        Article title: {article.get('title', '')}
        Article content: {article.get('content', '')}
        
        Return only valid JSON, nothing else."""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = str(message.content[0].text)
        result = json.loads(text)
        logger.info(f"Sentiment analyzed: {result.get('sentiment')} with confidence {result.get('confidence')}")
        return result
    
    except Exception as e:
        logger.error(f"Failed to analyze sentiment: {e}")
        return {"sentiment": "neutral", "confidence": 0, "summary": "", "recommendation": "watch"}