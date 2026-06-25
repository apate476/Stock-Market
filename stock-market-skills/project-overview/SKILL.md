---
name: Stock Market Sentiment Analyzer Project
description: Use this skill for any task related to the Stock Market Sentiment Analyzer project. Triggers when the user mentions the project, asks about the pipeline, wants to add features, debug code, write tests, or work on any part of this codebase.
dependencies:
  - anthropic
  - fastapi
  - uvicorn
  - supabase
  - newsapi-python
  - apache-airflow
  - pandas
  - python-dotenv
  - pytest
  - pytest-cov
  - pylint
  - mypy
  - requests
---

# Stock Market Sentiment Analyzer — Project Overview Skill

## What This Project Does
An automated system that fetches financial news daily, analyzes sentiment using Claude AI, stores results in Supabase, and delivers personalized investment insights via email and a React dashboard.

## Pipeline Flow (in order)
```
7:00 AM — Airflow triggers the pipeline
    |
    v
SKILL 1: fetch_financial_news()
    Fetches news from NewsAPI for top 10 stocks + user watchlist
    |
    v
SKILL 2: analyze_sentiment()
    Claude analyzes each article → bullish/bearish/neutral + confidence + recommendation
    |
    v
SKILL 3: store_sentiment_result()
    Saves results to Supabase sentiment_results table
    |
    v
SKILL 4: send_email_digest()
    Queries Supabase, formats HTML email, sends at 7:15 AM
    |
    v
FastAPI WebSocket pushes updates to React dashboard
```

## Project Structure
```
stock-market-sentiment/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   ├── auth.py              # Supabase auth
│   │   └── routes/
│   │       ├── stocks.py
│   │       ├── sentiment.py
│   │       └── users.py
│   ├── pipeline/
│   │   ├── dag.py               # Airflow DAG
│   │   ├── fetch_news.py        # SKILL 1
│   │   ├── analyze.py           # SKILL 2
│   │   ├── store.py             # SKILL 3
│   │   └── email_digest.py      # SKILL 4
│   ├── models/
│   │   ├── sentiment.py         # Pydantic models
│   │   └── user.py
│   └── utils/
│       ├── logger.py            # Logging setup
│       └── config.py            # Environment variables
├── tests/
│   ├── unit/
│   └── integration/
├── frontend/
│   └── src/
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Backend API | FastAPI |
| Pipeline | Apache Airflow |
| AI | Anthropic Claude API (claude-sonnet-4-6) |
| News | NewsAPI |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Frontend | React + Chart.js |
| Real-time | WebSocket |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Testing | pytest + coverage |

## Coding Conventions
- All functions must have type hints
- All functions must have a docstring explaining what they do
- Use `snake_case` for variables and functions
- Use `UPPER_CASE` for constants
- Maximum function length: 50 lines. If longer, split into smaller functions.
- Every function that calls an external API must handle errors gracefully and never raise exceptions to the caller

## Logging Setup
Use the shared logger from utils/logger.py. Never use print() statements.
```python
from src.utils.logger import get_logger
logger = get_logger(__name__)

# Usage:
logger.info("Fetched 10 articles for AAPL")
logger.warning("NewsAPI rate limit approaching")
logger.error("Failed to connect to Supabase: {error}")
```

## Environment Variables
All secrets live in .env (never committed to git). Access via:
```python
import os
from dotenv import load_dotenv
load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
```

## Standard Imports for Pipeline Files
```python
import os
import logging
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
```

## Testing Conventions
- All tests in tests/ folder
- Unit tests mock ALL external APIs (NewsAPI, Claude, Supabase, SMTP)
- Never call real APIs in tests
- Coverage target: 80%+
- Run tests: `pytest tests/ --cov=src --cov-report=term-missing`
- Run single file: `pytest tests/unit/test_fetch_news.py -v`

## CI/CD Rules
- Every push to any branch runs linter + type checker + all tests
- Only merge to main if all checks pass
- Deploy only triggers on merge to main
- Never push API keys (use environment variables and .gitignore)

## Default Stock List (Top 10)
```python
DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", "AMZN", "META", "NFLX", "JPM", "SPY"]
```

## Database Tables
- `users` — user profiles, watchlists, preferences
- `sentiment_results` — daily sentiment analysis per stock
- `daily_digests` — email send history

## How to Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in your API keys in .env

# Run FastAPI server
uvicorn src.api.main:app --reload

# Run tests
pytest tests/ --cov=src

# Run pipeline manually (without Airflow)
python src/pipeline/dag.py
```
