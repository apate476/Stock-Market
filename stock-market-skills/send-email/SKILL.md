---
name: Send Email Digest
description: Use this skill when building, debugging, or improving the send_email_digest function in the Stock Market Sentiment Analyzer. Triggers when the user mentions sending emails, email digest, morning briefing, email formatting, Gmail SMTP, SendGrid, or HTML email templates.
dependencies:
  - supabase
  - python-dotenv
  - sendgrid
---

# Send Email Digest Skill

## What This Does
Formats and sends the daily morning email digest to the user. This is SKILL 4 in the daily pipeline. Runs after all sentiment results are stored. Queries Supabase for today's results and sends a formatted HTML email at 7:15 AM.

## Project Context
- Project: Stock Market Sentiment Analyzer
- File location: src/pipeline/email_digest.py
- Reads from: Supabase sentiment_results table (populated by SKILL 3)
- Triggered by: Airflow DAG at 7:15 AM daily (15 minutes after news fetch)

## Required Imports
```python
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
```

## Run Tests
```bash
pytest tests/unit/test_email_digest.py -v
```

## Function Signature
```python
def send_email_digest(user_email: str, analysis_results: list[dict], date: str) -> bool:
```

## Email Structure
The email should be clean, scannable, and mobile-friendly HTML with these sections:

1. Header: "Good Morning [Name] — Stock Market Sentiment for [Date]"
2. Top 3 Bullish Stocks (green section)
3. Top 3 Bearish Stocks (red section)
4. User's Watchlist (blue section)
5. Major Sentiment Shifts (yellow section — only if >10% change vs yesterday)
6. Footer: Dashboard link, Manage Preferences link, Unsubscribe link

## Email Delivery Options
- Primary: Gmail SMTP (use for development and personal use)
- Production alternative: SendGrid API (better deliverability at scale)

## Gmail SMTP Setup
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_via_gmail(to_email: str, subject: str, html_body: str) -> bool:
    smtp_server = "smtp.gmail.com"
    port = 587
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")  # Use Gmail App Password, not real password
    # ...
```

## Rules for This Function
- Never hardcode email credentials. Use environment variables.
- Use Gmail App Password (not real Gmail password). Set up at myaccount.google.com/apppasswords
- Retry sending 3 times on failure with exponential backoff
- If all retries fail, send a Slack alert (if webhook configured)
- Log every sent email with timestamp and recipient
- Return True on success, False on failure
- HTML should be inline CSS only (email clients strip external stylesheets)

## Sentiment to Color Mapping (for HTML)
```python
SENTIMENT_COLORS = {
    "bullish": "#22c55e",      # green
    "bearish": "#ef4444",      # red
    "neutral": "#94a3b8"       # gray
}

RECOMMENDATION_COLORS = {
    "BUY": "#22c55e",
    "STRONG BUY": "#16a34a",
    "HOLD": "#f59e0b",
    "WATCH": "#3b82f6",
    "AVOID": "#ef4444"
}
```

## Error Handling
- SMTP connection fails: retry 3 times, send Slack alert, return False
- Invalid email address: log error, return False, do not retry
- Empty analysis_results: send simplified email "No analysis available today", return True

## Testing Requirements
- Unit test: Mock SMTP, verify email is constructed correctly
- Unit test: Verify HTML contains correct stock names and sentiments
- Unit test: Handle empty analysis results
- Unit test: Handle SMTP failure, verify retry logic
- Unit test: Verify returns True on success, False on failure
- All tests in: tests/unit/test_email_digest.py

## Example Test Pattern
```python
from unittest.mock import patch, MagicMock
from src.pipeline.email_digest import send_email_digest

def test_email_sent_successfully():
    mock_results = [
        {"ticker": "AAPL", "sentiment": "bullish", "confidence": 85, "recommendation": "BUY", "summary": "Strong quarter."}
    ]
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_smtp.return_value)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        result = send_email_digest("test@gmail.com", mock_results, "2026-06-25")
        assert result == True
```
