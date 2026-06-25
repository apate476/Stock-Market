# Stock Market Sentiment Analyzer

An automated AI-powered system that fetches financial news daily, analyzes sentiment using Claude AI, and delivers personalized investment insights via a morning email digest and a real-time dashboard.

Built by [Arya Patel](https://github.com/apate476).

---

## What It Does

- Fetches financial news every morning at 7 AM via NewsAPI
- Tracks your personal watchlist + top 10 most actively traded stocks
- Uses Claude AI to score each article as bullish, bearish, or neutral
- Stores results in Supabase for historical trend analysis
- Sends a morning email digest with investment signals before the market opens
- Displays a real-time React dashboard showing 30-day sentiment trends

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10, FastAPI |
| Scheduler | Apache Airflow |
| AI | Anthropic Claude API |
| News | NewsAPI + Financial Modeling Prep |
| Database | Supabase (PostgreSQL) |
| Frontend | React, Chart.js, Tailwind CSS |
| Email | Gmail SMTP (dev), SendGrid (prod) |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## Project Structure

```
stock-market/
├── dags/                   # Airflow DAG (daily pipeline)
├── src/
│   └── sentiment_analyzer/
│       ├── news/           # fetch_financial_news, fetch_top_tickers
│       ├── sentiment/      # analyze_sentiment (Claude API)
│       ├── database/       # store_sentiment_result (Supabase)
│       ├── email/          # send_email_digest
│       ├── api/            # FastAPI endpoints
│       └── utils/          # logger, config
├── tests/                  # Unit tests (pytest)
├── .github/workflows/      # CI/CD (GitHub Actions)
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/apate476/Stock-Market.git
cd Stock-Market
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Fill in your keys in `.env`:

```
ANTHROPIC_API_KEY=
NEWS_API_KEY=
FMP_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
EMAIL_SENDER=
EMAIL_PASSWORD=
```

### 5. Run tests

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### 6. Start the API

```bash
uvicorn src.sentiment_analyzer.api.main:app --reload
```

---

## Pipeline Flow

```
fetch_financial_news → analyze_sentiment → store_sentiment_result → send_email_digest
```

Each step is an Airflow task. Data passes between tasks via XCom.

---

## Personal Watchlist

Currently tracking: `NVDA`, `SPCX`, `MSFT`, `BRK-B`, `JPM` + top 10 most active stocks fetched daily from Financial Modeling Prep.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
