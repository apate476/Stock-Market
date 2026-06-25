import pytest
from unittest.mock import patch, MagicMock
from src.sentiment_analyzer.database.store_sentiment_result import store_sentiment_result


def test_store_sentiment_result_returns_true_on_success():
    """Test that True is returned when Supabase insert succeeds."""
    with patch("src.sentiment_analyzer.database.store_sentiment_result.create_client") as mock_client:
        mock_client.return_value.table.return_value.insert.return_value.execute.return_value = MagicMock()
        result = store_sentiment_result("AAPL", {"sentiment": "bullish", "confidence": 85, "summary": "Apple hits record high."})
    
    assert result == True



def test_store_sentiment_result_returns_false_on_exception():
    """Test that False is returned when Supabase throws an exception."""
    with patch("src.sentiment_analyzer.database.store_sentiment_result.create_client") as mock_client:
        mock_client.return_value.table.return_value.insert.return_value.execute.side_effect = Exception("DB error")
        result = store_sentiment_result("AAPL", {"sentiment": "bullish", "confidence": 85, "summary": "Apple hits record high."})
    
    assert result == False



def test_store_sentiment_result_sends_correct_data():
    """Test that the correct data shape is sent to Supabase."""
    with patch("src.sentiment_analyzer.database.store_sentiment_result.create_client") as mock_client:
        mock_insert = mock_client.return_value.table.return_value.insert
        mock_insert.return_value.execute.return_value = MagicMock()
        
        store_sentiment_result("TSLA", {"sentiment": "bearish", "confidence": 72, "summary": "Tesla misses targets."})
        
        mock_insert.assert_called_once_with({
            "ticker": "TSLA",
            "sentiment": "bearish",
            "confidence": 72,
            "summary": "Tesla misses targets."
        })

