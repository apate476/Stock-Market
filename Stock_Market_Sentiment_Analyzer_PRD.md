# Stock Market Sentiment Analyzer
## Product Requirements Document (PRD)
**Version:** 1.0
**Author:** Arya Patel
**Date:** June 2026
**Status:** Active

---

## 1. Project Overview

**Project Name:** Stock Market Sentiment Analyzer

**One-Line Description:**
An automated AI-powered system that fetches financial news daily, analyzes sentiment using Claude, and delivers personalized investment insights via email and a real-time dashboard.

**Why This Project Exists:**
Daily active investors need to process large volumes of financial news quickly to make informed decisions. Reading every article manually takes hours. This system automates that process, surfaces the most important signals, and delivers them before the market opens.

---

## 2. Problem Statement

Daily investors face three core challenges:

1. **Information overload** — Hundreds of news articles published daily across thousands of stocks. No time to read everything.
2. **Delayed reactions** — By the time investors read the news, the market has already priced it in.
3. **No historical context** — Hard to know if today's sentiment is unusual without comparing it to past trends.

**Result:** Investors make decisions without complete information or miss opportunities entirely.

---

## 3. Solution

An automated pipeline that:
- Fetches financial news every morning at 7 AM via NewsAPI
- Uses Claude AI to analyze each article for sentiment (bullish, bearish, neutral)
- Stores results in Supabase for historical trend analysis
- Sends a personalized email digest at 7:15 AM with investment recommendations
- Displays a real-time dashboard showing 30-day sentiment trends
- Sends real-time alerts when sentiment shifts more than 10% for any stock

---

## 4. Target User

**Primary User:** Daily active retail investors who:
- Trade stocks regularly (daily or weekly)
- Make decisions based on news sentiment
- Want market insights delivered before they start their day
- Have a personal watchlist of 5-10 stocks they follow closely

---

## 5. Core Features

### Feature 1: Daily News Ingestion (Automated)
- Runs every morning at 7:00 AM via Airflow scheduler
- Fetches latest financial news from NewsAPI
- Covers top 10 most-traded stocks by default
- Includes user's custom watchlist (up to 5 additional stocks)
- Deduplicates articles to avoid analyzing the same story twice

### Feature 2: Claude-Powered Sentiment Analysis
- Each article analyzed by Claude for sentiment: bullish, bearish, or neutral
- Confidence score returned (0-100%)
- Key factors extracted (earnings, competition, regulation, leadership changes)
- Short 1-2 sentence summary generated per article
- Sentiment aggregated per stock across all articles for that day

### Feature 3: Daily Email Digest
- Sent at 7:15 AM (15 minutes after ingestion completes)
- Subject: "Stock Market Sentiment - [Date]"
- Shows top 3 bullish stocks, top 3 bearish stocks
- Shows user's personal watchlist sentiment
- Compares today's sentiment to yesterday (trend direction)
- Includes buy, hold, or watch recommendation per stock
- Clean HTML format, mobile-friendly

### Feature 4: Real-Time Dashboard
- React frontend showing sentiment trends over time
- Charts: 30-day sentiment score per stock (Chart.js)
- Filters: By stock, by date range, by sentiment type
- WebSocket for real-time updates when new analysis runs
- Authentication: Users see only their own watchlist data
- Mobile-responsive design

### Feature 5: Sentiment Shift Alerts
- Triggered when a stock's sentiment changes by more than 10% vs. previous day
- Delivered via email immediately (not waiting for morning digest)
- User can customize sensitivity threshold (5%, 10%, 20%)
- Alert includes: stock name, previous sentiment, new sentiment, key article that caused the shift

### Feature 6: User Authentication and Watchlist Management
- Supabase Auth (email/password login)
- User profile stores: email, custom watchlist (up to 5 stocks), alert preferences, email frequency
- Users can add/remove stocks from their watchlist at any time
- Settings page to manage preferences

---

## 6. Stock Selection Strategy

### Default Top 10 (analyzed daily for all users):
AAPL, MSFT, GOOGL, NVDA, TSLA, AMZN, META, NFLX, MAGN, SPY

### User Custom Watchlist:
- Up to 5 additional stocks per user
- Any valid NYSE or NASDAQ ticker
- Stored in Supabase user profile
- Included in daily email and dashboard

### Daily Email Coverage:
Top 10 default stocks + user's custom watchlist = 10-15 stocks per email

---

## 7. Custom Skills (Functions Claude Can Call)

These are the 4 core skills Claude uses to execute the daily pipeline:

### SKILL 1: `fetch_financial_news`
```
Purpose: Fetch latest financial news articles for a list of stock tickers
Input: tickers (list of strings), num_articles (int, default 10)
Output: Dictionary of {ticker: [list of articles with title, description, url, published_at]}
Error handling: Returns empty list if NewsAPI fails, logs error
```

### SKILL 2: `analyze_sentiment`
```
Purpose: Claude analyzes a news article and returns structured sentiment data
Input: ticker (str), title (str), description (str)
Output: {
  sentiment: "bullish" | "bearish" | "neutral",
  confidence: int (0-100),
  factors: list of strings (key reasons),
  summary: str (1-2 sentence explanation)
}
Error handling: Returns neutral sentiment with 0 confidence if analysis fails
```

### SKILL 3: `store_sentiment_result`
```
Purpose: Save sentiment analysis result to Supabase database
Input: ticker (str), sentiment (dict from analyze_sentiment), date (str)
Output: Boolean (True = success, False = failure)
Error handling: Retries 3 times on failure, logs final error
```

### SKILL 4: `send_email_digest`
```
Purpose: Format and send daily sentiment email to user
Input: user_email (str), analysis_results (list of dicts), date (str)
Output: Boolean (True = delivered, False = failed)
Error handling: Retries 3 times, sends Slack alert if all retries fail
```

### OPTIONAL SKILL 5: `send_slack_alert`
```
Purpose: Send real-time sentiment shift alert to Slack
Input: webhook_url (str), message (str), stock (str), old_sentiment (str), new_sentiment (str)
Output: Boolean (True = sent, False = failed)
Error handling: Logs failure, does not retry (non-critical)
```

---

## 8. Email Digest Template

**Subject:** Stock Market Sentiment - June 25, 2026

```
Good Morning, Arya

Here is your daily market sentiment analysis for June 25, 2026.

---

TOP BULLISH STOCKS

1. TSLA (Tesla)
   Sentiment: Very Bullish | Confidence: 87%
   Key Factors: Record deliveries, positive analyst upgrade
   Headline: "Tesla Reports Best Quarter in Company History"
   Recommendation: STRONG BUY

2. NVDA (NVIDIA)
   Sentiment: Bullish | Confidence: 74%
   Key Factors: AI chip demand, new partnership announced
   Headline: "NVIDIA Secures Major Cloud Partnership"
   Recommendation: BUY

3. AAPL (Apple)
   Sentiment: Slightly Bullish | Confidence: 61%
   Key Factors: iPhone sales steady, services revenue up
   Headline: "Apple Services Revenue Hits All-Time High"
   Recommendation: WATCH

---

TOP BEARISH STOCKS

1. META (Meta Platforms)
   Sentiment: Bearish | Confidence: 78%
   Key Factors: Regulatory pressure, ad revenue concerns
   Headline: "EU Fines Meta $1B for Privacy Violations"
   Recommendation: HOLD or REDUCE

2. BA (Boeing)
   Sentiment: Very Bearish | Confidence: 82%
   Key Factors: Safety concerns, production delays
   Headline: "Boeing Halts Production After New Defects Found"
   Recommendation: AVOID

---

YOUR WATCHLIST

- MSFT: Neutral (no change from yesterday)
- AMZN: Slightly Bullish (+8% vs yesterday)
- GOOGL: Neutral (-3% vs yesterday)

---

MAJOR SHIFTS TODAY

- TSLA: +22% swing (was Neutral, now Very Bullish)
- META: -18% swing (was Slightly Bullish, now Bearish)

---

View your full dashboard: [Dashboard Link]
Manage your preferences: [Settings Link]
Unsubscribe: [Unsubscribe Link]
```

---

## 9. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend API | Python + FastAPI | Industry standard, fast, you know it |
| Pipeline Orchestration | Apache Airflow | Schedules daily 7 AM run, industry standard |
| AI/Sentiment | Anthropic Claude API | Core intelligence of the system |
| News Source | NewsAPI | Free tier, easy to use, financial news coverage |
| Database | Supabase (PostgreSQL) | Managed, free tier, built-in auth, real-time |
| Authentication | Supabase Auth | Email/password, no extra code needed |
| Frontend | React + Chart.js | You know React, Chart.js for sentiment graphs |
| Real-Time Updates | WebSocket | Live dashboard updates |
| Styling | Tailwind CSS | Fast to build, clean UI |
| Containerization | Docker | Production-ready, portfolio-worthy |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Hosting | AWS EC2 or DigitalOcean | Deployment experience for resume |
| Email Delivery | Gmail SMTP or SendGrid | Reliable email delivery |

---

## 10. Project Structure

```
stock-market-sentiment/
|
|- src/
|   |- api/
|   |   |- main.py              # FastAPI app, endpoints, WebSocket
|   |   |- auth.py              # Supabase auth integration
|   |   |- routes/
|   |       |- stocks.py        # Stock data endpoints
|   |       |- sentiment.py     # Sentiment query endpoints
|   |       |- users.py         # User watchlist endpoints
|   |
|   |- pipeline/
|   |   |- dag.py               # Airflow DAG (daily 7 AM run)
|   |   |- fetch_news.py        # SKILL 1: fetch_financial_news
|   |   |- analyze.py           # SKILL 2: analyze_sentiment
|   |   |- store.py             # SKILL 3: store_sentiment_result
|   |   |- email_digest.py      # SKILL 4: send_email_digest
|   |   |- alerts.py            # SKILL 5: send_slack_alert
|   |
|   |- models/
|   |   |- sentiment.py         # Pydantic models for sentiment data
|   |   |- user.py              # Pydantic models for user data
|   |
|   |- utils/
|       |- logger.py            # Logging setup
|       |- config.py            # Environment variables
|
|- frontend/
|   |- src/
|       |- App.jsx
|       |- components/
|           |- Dashboard.jsx    # Main dashboard with charts
|           |- WatchList.jsx    # User's custom stocks
|           |- SentimentCard.jsx
|           |- AlertBanner.jsx
|
|- tests/
|   |- unit/
|   |   |- test_fetch_news.py
|   |   |- test_analyze.py
|   |   |- test_store.py
|   |   |- test_email.py
|   |- integration/
|       |- test_pipeline.py     # Full pipeline test
|       |- test_api.py          # API endpoint tests
|
|- .github/
|   |- workflows/
|       |- ci.yml               # Run tests on every push
|       |- deploy.yml           # Deploy on merge to main
|
|- docker-compose.yml
|- Dockerfile
|- .env.example
|- requirements.txt
|- README.md
```

---

## 11. Database Schema (Supabase)

### Table: users
```
id            uuid PRIMARY KEY
email         text UNIQUE NOT NULL
created_at    timestamp
watchlist     text[] (array of stock tickers, max 5)
alert_threshold float DEFAULT 0.10
email_frequency text DEFAULT 'daily'
```

### Table: sentiment_results
```
id            uuid PRIMARY KEY
ticker        text NOT NULL
date          date NOT NULL
sentiment     text NOT NULL (bullish/bearish/neutral)
confidence    int NOT NULL (0-100)
factors       text[] (array of key factors)
summary       text
article_url   text
created_at    timestamp
```

### Table: daily_digests
```
id            uuid PRIMARY KEY
user_id       uuid REFERENCES users(id)
date          date NOT NULL
email_sent    boolean DEFAULT false
sent_at       timestamp
error_message text
```

---

## 12. Testing Strategy

### Unit Tests (test each skill in isolation)
- test_fetch_news.py: Mock NewsAPI, test article parsing, test empty response handling
- test_analyze.py: Mock Claude API, test sentiment parsing, test edge cases (no news, all neutral)
- test_store.py: Mock Supabase, test successful write, test retry logic on failure
- test_email.py: Test email HTML formatting, test send success and failure paths

### Integration Tests (test full pipeline)
- test_pipeline.py: Run full pipeline with mocked external APIs, verify data stored correctly
- test_api.py: Test all FastAPI endpoints with test client

### Coverage Target: 80%+

### Test Command:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 13. CI/CD Pipeline

### GitHub Actions Workflow (ci.yml)
```
Trigger: Every push to any branch

Steps:
1. Checkout code
2. Set up Python 3.10
3. Install dependencies (pip install -r requirements.txt)
4. Run linter (pylint src/)
5. Run type checker (mypy src/)
6. Run all tests (pytest tests/ --cov=src)
7. Build Docker image
8. Report coverage

Pass criteria: All steps must pass before merging to main
```

### Deploy Workflow (deploy.yml)
```
Trigger: Merge to main branch

Steps:
1. Run full CI pipeline
2. Build and push Docker image to registry
3. SSH into production server
4. Pull latest Docker image
5. Restart containers
6. Health check (ping /health endpoint)
7. Notify Slack on success or failure
```

---

## 14. Deployment & Monitoring

### Infrastructure
- AWS EC2 (t2.micro free tier) or DigitalOcean Droplet ($6/month)
- Docker Compose running: FastAPI + Airflow + Redis (Airflow broker)
- Supabase handles database (no self-hosted DB needed)
- Nginx reverse proxy for HTTPS

### Monitoring
- Log every pipeline run (start time, articles fetched, sentiments analyzed, email sent)
- Track Claude API usage and costs daily
- Track NewsAPI request count vs. daily limit (100 free)
- Health check endpoint: GET /health returns pipeline status

### Failure Handling
| Failure | Response |
|---|---|
| NewsAPI fails | Use cached articles from yesterday, log warning |
| Claude API fails | Mark analysis as failed, skip email for that stock |
| Email fails to send | Retry 3 times with exponential backoff, send Slack alert |
| Supabase connection fails | Retry 3 times, log error, continue pipeline |
| Full pipeline crash | Alert via Slack, send fallback email: "Analysis unavailable today" |

---

## 15. Success Metrics

| Metric | Target |
|---|---|
| Pipeline uptime | 99% (runs successfully every day) |
| Email delivery time | Within 5 minutes of 7:15 AM scheduled time |
| Sentiment accuracy | 80%+ validated against manual review |
| Dashboard load time | Under 2 seconds |
| Test coverage | 80%+ |
| Claude API cost | Under $10/month during development |

---

## 16. Build Timeline

### Week 1: Foundation
- Set up project structure (src/, tests/, docker/)
- Configure Supabase (tables, auth)
- Build FastAPI skeleton with health check endpoint
- Implement SKILL 1: fetch_financial_news
- Implement SKILL 2: analyze_sentiment (Claude API integration)
- Write unit tests for both skills
- Set up GitHub Actions CI

### Week 2: Data Pipeline
- Implement SKILL 3: store_sentiment_result
- Build Airflow DAG (daily 7 AM schedule)
- Implement SKILL 4: send_email_digest
- Write integration tests for full pipeline
- Docker Compose setup
- Test full pipeline end-to-end locally

### Week 3: Frontend + Dashboard
- Build React frontend (Dashboard, WatchList, SentimentCard)
- Integrate Chart.js for sentiment trend charts
- Connect WebSocket for real-time updates
- Add authentication (Supabase Auth login/signup)
- User watchlist management (add/remove stocks)

### Week 4: Production + Polish
- Deploy to AWS or DigitalOcean
- Set up HTTPS with Nginx
- Add monitoring and logging
- Implement alert system (SKILL 5)
- Write README
- Final testing and bug fixes
- Push to GitHub with clean commit history

---

## 17. Environment Variables

```
# .env.example (never commit actual values)

# Anthropic
ANTHROPIC_API_KEY=your_key_here

# NewsAPI
NEWS_API_KEY=your_key_here

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# Email
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SENDGRID_API_KEY=optional_sendgrid_key

# Slack (optional alerts)
SLACK_WEBHOOK_URL=your_webhook_url

# App
APP_ENV=development
APP_PORT=8000
SECRET_KEY=your_secret_key
```

---

## 18. Future Features (Post-MVP)

| Feature | Description | Priority |
|---|---|---|
| Portfolio tracker | Track user's actual holdings and P&L | High |
| Price alerts | Notify when stock hits target price | High |
| Competitor comparison | Compare sentiment of competing companies | Medium |
| Sector analysis | Analyze entire sectors (tech, energy, healthcare) | Medium |
| Historical backtesting | "What if you bought when sentiment was 80%+ bullish?" | Medium |
| ML model training | Train custom model on historical sentiment data | Low |
| Multi-user teams | Share watchlists and insights with team members | Low |
| Mobile app | React Native version of the dashboard | Low |

---

## 19. How to Use This PRD

Upload this document to your Claude Project as context. When starting each phase of development, reference the relevant section:

- **Starting Week 1?** Reference: Tech Stack, Project Structure, SKILL 1 and 2 definitions
- **Building the pipeline?** Reference: SKILL 3 and 4, Airflow DAG, Database Schema
- **Building the frontend?** Reference: Dashboard features, Email Template, WebSocket
- **Deploying?** Reference: CI/CD Pipeline, Deployment section, Environment Variables

Tell Claude: "I am building the Stock Market Sentiment Analyzer. Here is my PRD. I am currently on Week [X]. Help me build [specific feature]. Do not write the entire code for me. Guide me through it."

---

*End of PRD*
