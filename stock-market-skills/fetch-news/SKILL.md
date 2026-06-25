---
name: Fetch Financial News
description: Use this skill when building, debugging, or improving the fetch_financial_news function in the Stock Market Sentiment Analyzer. Triggers when the user mentions fetching news, NewsAPI, getting articles, or pulling financial data for stocks.
dependencies:
  - requests
  - newsapi-python
  - python-dotenv
---

# Fetch Financial News Skill

## What This Does
Fetches the latest financial news articles for a list of stock tickers using NewsAPI. This is SKILL 1 in the daily pipeline. It runs first every morning at 7 AM via Airflow.

## Project Context
- Project: Stock Market Sentiment Analyzer
- File location: src/pipeline/fetch_news.py
- Called by: Airflow DAG (dag.py) at 7 AM daily
- Passes output to: analyze_sentiment (SKILL 2)

## Function Signature
```python
def fetch_financial_news(tickers: list[str], num_articles: int = 10) -> dict[str, list[dict]]:
```

## Expected Output Format
```python
{
    "AAPL": [
        {
            "title": "Apple Reports Record Revenue",
            "description": "Apple Inc. reported...",
            "url": "https://...",
            "published_at": "2026-06-25T07:00:00Z"
        }
    ],
    "TSLA": [...]
}
```

## Required Imports
```python
import os
import requests
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"
```

## Run Tests
```bash
pytest tests/unit/test_fetch_news.py -v
```

## Rules for This Function
- Never hardcode API keys. Always use os.environ.get("NEWS_API_KEY")
- If NewsAPI fails, return empty list for that ticker and log the error. Do not crash.
- Deduplicate articles by URL to avoid analyzing the same story twice.
- Log how many articles were fetched per ticker.
- Always test with a mock NewsAPI response, never call the real API in tests.

## Error Handling
- NewsAPI rate limit hit: log warning, return empty dict, continue pipeline
- Invalid ticker: log warning, skip ticker, continue
- Network timeout: retry once after 5 seconds, then fail gracefully

## Testing Requirements
- Unit test: Mock NewsAPI response, verify correct parsing
- Unit test: Handle empty response (no articles found)
- Unit test: Handle NewsAPI error (401, 429, 500)
- All tests in: tests/unit/test_fetch_news.py

## Example Test Pattern
```python
from unittest.mock import patch, MagicMock
from src.pipeline.fetch_news import fetch_financial_news

def test_fetch_news_returns_articles():
    mock_response = {
        "articles": [
            {"title": "Test", "description": "Test desc", "url": "http://test.com", "publishedAt": "2026-06-25"}
        ]
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        result = fetch_financial_news(["AAPL"], 1)
        assert "AAPL" in result
        assert len(result["AAPL"]) == 1
```
