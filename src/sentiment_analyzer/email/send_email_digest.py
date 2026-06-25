import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.sentiment_analyzer.utils.logger import logger
from src.sentiment_analyzer.utils.config import EMAIL_SENDER, EMAIL_PASSWORD


def send_email_digest(results: list[dict], recipient: str) -> bool:
    """Send a daily sentiment digest email to the recipient."""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Stock Market Sentiment Digest"
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient

        html = "<h2>Daily Stock Sentiment Report</h2><ul>"
        for item in results:
            html += f"<li><b>{item.get('ticker')}</b>: {item.get('sentiment')} (confidence: {item.get('confidence')}%) — {item.get('summary')}</li>"
        html += "</ul>"
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        logger.info(f"Email digest sent to {recipient}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email digest: {e}")
        return False