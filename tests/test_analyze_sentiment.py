from unittest.mock import patch, MagicMock
from src.sentiment_analyzer.sentiment.analyze_sentiment import analyze_sentiment



def test_analyze_sentiment_returns_result():
    """Test that sentiment result is returned when Claude responds successfully."""
    mock_message = MagicMock()
    mock_message.content[0].text = '{"sentiment": "bullish", "confidence": 85, "summary": "Apple reports record profits.", "recommendation": "buy"}'
    
    with patch("src.sentiment_analyzer.sentiment.analyze_sentiment.anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_message
        result = analyze_sentiment({"title": "Apple hits record high", "content": "Apple reported record profits."})
    
    assert result["sentiment"] == "bullish"
    assert result["confidence"] == 85



def test_analyze_sentiment_returns_default_on_invalid_json():
    """Test that default neutral result is returned when Claude returns invalid JSON."""
    mock_message = MagicMock()
    mock_message.content[0].text = "This is not valid JSON"
    
    with patch("src.sentiment_analyzer.sentiment.analyze_sentiment.anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_message
        result = analyze_sentiment({"title": "Test", "content": "Test content"})
    
    assert result["sentiment"] == "neutral"
    assert result["confidence"] == 0



def test_analyze_sentiment_returns_default_on_exception():
    """Test that default neutral result is returned when Claude API throws an exception."""
    with patch("src.sentiment_analyzer.sentiment.analyze_sentiment.anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.side_effect = Exception("API error")
        result = analyze_sentiment({"title": "Test", "content": "Test content"})
    
    assert result["sentiment"] == "neutral"
    assert result["confidence"] == 0           