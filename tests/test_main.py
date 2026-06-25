from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.sentiment_analyzer.api.main import app

client = TestClient(app)


def test_get_all_sentiments_returns_list():
    """Test that /sentiments returns a list of results."""
    mock_supabase = MagicMock()
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"ticker": "AAPL", "sentiment": "bullish", "confidence": 85, "summary": "Apple hits record high."}
    ]

    with patch("src.sentiment_analyzer.api.main.get_supabase", return_value=mock_supabase):
        response = client.get("/sentiments")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["ticker"] == "AAPL"


def test_get_all_sentiments_returns_empty_on_exception():
    """Test that /sentiments returns empty list on error."""
    mock_supabase = MagicMock()
    mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("DB error")

    with patch("src.sentiment_analyzer.api.main.get_supabase", return_value=mock_supabase):
        response = client.get("/sentiments")

    assert response.status_code == 200
    assert response.json() == []


def test_get_sentiment_by_ticker_returns_result():
    """Test that /sentiments/{ticker} returns results for a specific ticker."""
    mock_supabase = MagicMock()
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"ticker": "TSLA", "sentiment": "bearish", "confidence": 72, "summary": "Tesla misses targets."}
    ]

    with patch("src.sentiment_analyzer.api.main.get_supabase", return_value=mock_supabase):
        response = client.get("/sentiments/TSLA")

    assert response.status_code == 200
    assert response.json()[0]["ticker"] == "TSLA"
