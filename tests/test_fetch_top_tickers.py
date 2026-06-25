from unittest.mock import patch, MagicMock
from src.sentiment_analyzer.news.fetch_top_tickers import fetch_top_tickers


def test_fetch_top_tickers_returns_list():
    """Test that a list of tickers is returned when FMP responds successfully."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"symbol": "AAPL"}, {"symbol": "TSLA"}, {"symbol": "NVDA"}]
    mock_response.raise_for_status.return_value = None

    with patch("src.sentiment_analyzer.news.fetch_top_tickers.requests.get", return_value=mock_response):
        result = fetch_top_tickers()

    assert "AAPL" in result
    assert len(result) <= 10


def test_fetch_top_tickers_returns_empty_list_on_exception():
    """Test that an empty list is returned when FMP throws an exception."""
    with patch("src.sentiment_analyzer.news.fetch_top_tickers.requests.get", side_effect=Exception("API error")):
        result = fetch_top_tickers()

    assert result == []


def test_fetch_top_tickers_returns_max_10():
    """Test that at most 10 tickers are returned."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"symbol": f"TICK{i}"} for i in range(20)]
    mock_response.raise_for_status.return_value = None

    with patch("src.sentiment_analyzer.news.fetch_top_tickers.requests.get", return_value=mock_response):
        result = fetch_top_tickers()

    assert len(result) <= 10
