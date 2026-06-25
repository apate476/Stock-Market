---
name: Store Sentiment Result
description: Use this skill when building, debugging, or improving the store_sentiment_result function in the Stock Market Sentiment Analyzer. Triggers when the user mentions storing data, Supabase integration, saving sentiment results, database writes, or data persistence.
dependencies:
  - supabase
  - python-dotenv
---

# Store Sentiment Result Skill

## What This Does
Saves a sentiment analysis result to the Supabase database. This is SKILL 3 in the daily pipeline. Receives structured sentiment from SKILL 2 (analyze_sentiment). Data stored here powers the dashboard and historical trend analysis.

## Project Context
- Project: Stock Market Sentiment Analyzer
- File location: src/pipeline/store.py
- Receives input from: analyze_sentiment (SKILL 2)
- Data used by: FastAPI dashboard endpoints, daily email digest (SKILL 4)

## Required Imports
```python
import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_KEY")
)
```

## Run Tests
```bash
pytest tests/unit/test_store.py -v
```

## Function Signature
```python
def store_sentiment_result(ticker: str, sentiment: dict, date: str) -> bool:
```

## Supabase Table: sentiment_results
```sql
id            uuid PRIMARY KEY DEFAULT gen_random_uuid()
ticker        text NOT NULL
date          date NOT NULL
sentiment     text NOT NULL
confidence    int NOT NULL
factors       text[]
summary       text
recommendation text
article_url   text
created_at    timestamp DEFAULT now()
```

## Rules for This Function
- Never hardcode Supabase credentials. Use os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY")
- Use the Supabase Python client: from supabase import create_client
- Retry 3 times on failure with exponential backoff (1s, 2s, 4s) before giving up
- Log every successful write and every failure
- Return True on success, False on failure. Never raise exceptions from this function.
- Check for duplicate entries (same ticker + date) before inserting to avoid duplicates

## Retry Pattern
```python
import time

def store_with_retry(data: dict, max_retries: int = 3) -> bool:
    for attempt in range(max_retries):
        try:
            # attempt Supabase insert
            return True
        except Exception as e:
            wait = 2 ** attempt
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait}s")
            time.sleep(wait)
    logger.error("All retry attempts failed")
    return False
```

## Error Handling
- Supabase connection fails: retry 3 times, return False, log error
- Duplicate entry: skip insert, log info, return True (not an error)
- Invalid data format: log error, return False, do not retry

## Testing Requirements
- Unit test: Mock Supabase client, verify correct data structure sent
- Unit test: Handle Supabase connection failure, verify retry logic
- Unit test: Handle duplicate entry gracefully
- Unit test: Verify returns True on success, False on failure
- All tests in: tests/unit/test_store.py

## Example Test Pattern
```python
from unittest.mock import patch, MagicMock
from src.pipeline.store import store_sentiment_result

def test_store_returns_true_on_success():
    mock_sentiment = {
        "sentiment": "bullish",
        "confidence": 85,
        "factors": ["earnings beat"],
        "summary": "Strong quarter.",
        "recommendation": "BUY"
    }
    with patch("supabase.create_client") as mock_client:
        mock_client.return_value.table.return_value.insert.return_value.execute.return_value = MagicMock()
        result = store_sentiment_result("AAPL", mock_sentiment, "2026-06-25")
        assert result == True
```
