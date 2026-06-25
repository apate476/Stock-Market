from unittest.mock import patch
from src.sentiment_analyzer.news.fetch_financial_news import fetch_financial_news



def test_fetch_financial_news_returns_articles():
    """Test that articles are returned when NewsAPI responds successfully."""
    mock_response = {"articles": [{"title": "Apple hits record high", "url": "http://example.com"}]}
    
    with patch("src.sentiment_analyzer.news.fetch_financial_news.NewsApiClient") as mock_client:
        mock_client.return_value.get_everything.return_value = mock_response
        result = fetch_financial_news("AAPL")
    
    assert len(result) == 1
    assert result[0]["title"] == "Apple hits record high"



def test_fetch_financial_news_returns_empty_list_when_no_articles():
    """Test that an empty list is returned when NewsAPI returns no articles."""
    mock_response = {"articles": []}
    
    with patch("src.sentiment_analyzer.news.fetch_financial_news.NewsApiClient") as mock_client:
        mock_client.return_value.get_everything.return_value = mock_response
        result = fetch_financial_news("AAPL")
    
    assert result == []



def test_fetch_financial_news_returns_empty_list_on_exception():
    """Test that an empty list is returned when NewsAPI throws an exception."""
    with patch("src.sentiment_analyzer.news.fetch_financial_news.NewsApiClient") as mock_client:
        mock_client.return_value.get_everything.side_effect = Exception("API error")
        result = fetch_financial_news("AAPL")
    
    assert result == []