import pytest
from unittest.mock import patch, MagicMock
from src.sentiment_analyzer.email.send_email_digest import send_email_digest
import base64



def test_send_email_digest_returns_true_on_success():
    """Test that True is returned when email is sent successfully."""
    results = [{"ticker": "AAPL", "sentiment": "bullish", "confidence": 85, "summary": "Apple hits record high."}]
    
    with patch("src.sentiment_analyzer.email.send_email_digest.smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.return_value.__enter__.return_value = MagicMock()
        result = send_email_digest(results, "test@example.com")
    
    assert result == True



def test_send_email_digest_returns_false_on_exception():
    """Test that False is returned when SMTP throws an exception."""
    results = [{"ticker": "AAPL", "sentiment": "bullish", "confidence": 85, "summary": "Apple hits record high."}]
    
    with patch("src.sentiment_analyzer.email.send_email_digest.smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.side_effect = Exception("SMTP error")
        result = send_email_digest(results, "test@example.com")
    
    assert result == False



def test_send_email_digest_includes_ticker_in_email():
    """Test that the email body contains the ticker data."""
    results = [{"ticker": "TSLA", "sentiment": "bearish", "confidence": 72, "summary": "Tesla misses targets."}]
    
    with patch("src.sentiment_analyzer.email.send_email_digest.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        send_email_digest(results, "test@example.com")
        
        sent_email = mock_server.sendmail.call_args[0][2]
        decoded_email = base64.b64decode(sent_email.split("base64\n\n")[1].split("\n\n--")[0]).decode("utf-8")
        assert "TSLA" in decoded_email
        assert "bearish" in decoded_email