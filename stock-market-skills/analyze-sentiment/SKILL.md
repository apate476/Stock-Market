---
name: Analyze Sentiment
description: Use this skill when building, debugging, or improving the analyze_sentiment function in the Stock Market Sentiment Analyzer. Triggers when the user mentions sentiment analysis, Claude API integration, analyzing articles, bullish/bearish scoring, or extracting investment signals from news.
dependencies:
  - anthropic
  - python-dotenv
---

# Analyze Sentiment Skill

## What This Does
Calls Claude API to analyze a financial news article and returns structured sentiment data. This is SKILL 2 in the daily pipeline. Receives articles from SKILL 1 (fetch_news), returns structured sentiment to SKILL 3 (store_results).

## Project Context
- Project: Stock Market Sentiment Analyzer
- File location: src/pipeline/analyze.py
- Receives input from: fetch_financial_news (SKILL 1)
- Passes output to: store_sentiment_result (SKILL 3)

## Required Imports
```python
import os
import json
import anthropic
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

## Run Tests
```bash
pytest tests/unit/test_analyze.py -v
```

## Function Signature
```python
def analyze_sentiment(ticker: str, title: str, description: str) -> dict:
```

## Expected Output Format
```python
{
    "ticker": "AAPL",
    "sentiment": "bullish",       # bullish | bearish | neutral
    "confidence": 82,             # 0-100
    "factors": [                  # list of key reasons
        "strong earnings beat",
        "positive guidance"
    ],
    "summary": "Apple's Q2 earnings exceeded expectations...",
    "recommendation": "BUY"       # BUY | HOLD | WATCH | AVOID
}
```

## Claude Prompt Template
When calling Claude, use this exact prompt structure:
```
You are a financial analyst. Analyze the following news article about {ticker} and return ONLY a JSON object.

Article Title: {title}
Article Description: {description}

Return this exact JSON structure and nothing else:
{{
  "sentiment": "bullish" | "bearish" | "neutral",
  "confidence": <integer 0-100>,
  "factors": [<list of 2-3 key factors as strings>],
  "summary": "<1-2 sentence summary>",
  "recommendation": "BUY" | "HOLD" | "WATCH" | "AVOID"
}}
```

## Rules for This Function
- Never hardcode the API key. Use os.environ.get("ANTHROPIC_API_KEY")
- Always parse Claude's response as JSON. If parsing fails, return neutral sentiment.
- Use model: claude-sonnet-4-6
- Set max_tokens to 500 (response is short JSON only)
- Log every analysis with ticker, sentiment, and confidence score.
- If Claude API fails, return default neutral response and log error. Do not crash pipeline.

## Default Neutral Response (fallback on error)
```python
{
    "ticker": ticker,
    "sentiment": "neutral",
    "confidence": 0,
    "factors": ["analysis unavailable"],
    "summary": "Sentiment analysis could not be completed.",
    "recommendation": "HOLD"
}
```

## Error Handling
- Claude API timeout: return default neutral response, log error
- JSON parse error: return default neutral response, log raw response
- Invalid response format: return default neutral response, log warning

## Testing Requirements
- Unit test: Mock Claude API, verify correct JSON parsing
- Unit test: Handle malformed Claude response
- Unit test: Handle Claude API timeout
- Unit test: Verify all four sentiment values parse correctly
- All tests in: tests/unit/test_analyze.py

## Example Test Pattern
```python
from unittest.mock import patch, MagicMock
from src.pipeline.analyze import analyze_sentiment

def test_analyze_returns_bullish():
    mock_content = '{"sentiment": "bullish", "confidence": 85, "factors": ["earnings beat"], "summary": "Strong quarter.", "recommendation": "BUY"}'
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value.content = [MagicMock(text=mock_content)]
        result = analyze_sentiment("AAPL", "Apple beats earnings", "Apple reported...")
        assert result["sentiment"] == "bullish"
        assert result["confidence"] == 85
```
