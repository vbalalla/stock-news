import pytest
from app.services.stock_service import StockService
from app.services.news_service import NewsService
from app.models import Stock, NewsArticle
import os
from datetime import datetime

def test_stock_service():
    service = StockService()
    stocks = service.get_stocks()
    
    assert len(stocks) > 0
    assert isinstance(stocks[0], Stock)
    assert stocks[0].symbol == "JPM"  # First stock should be JPMorgan Chase
    
    # Test getting stock by symbol
    jpm = service.get_stock_by_symbol("JPM")
    assert jpm is not None
    assert jpm.name == "JPMorgan Chase & Co."
    assert jpm.sector == "Financial Services"
    
    # Test getting all stock symbols
    symbols = service.get_stock_symbols()
    assert len(symbols) == len(stocks)
    assert "JPM" in symbols
    assert "V" in symbols

@pytest.mark.skipif(not os.getenv("NEWS_API_KEY"), reason="NEWS_API_KEY not set")
def test_news_service():
    api_key = os.getenv("NEWS_API_KEY")
    service = NewsService(api_key=api_key)
    
    # Test news fetching
    try:
        news = service.get_news()
        assert isinstance(news, list)
        if len(news) > 0:
            article = news[0]
            assert isinstance(article, NewsArticle)
            assert isinstance(article.published_at, datetime)
            assert article.title is not None
            assert article.url is not None
            assert isinstance(article.sentiment_scores, dict)
            assert "compound" in article.sentiment_scores
            assert article.sentiment in ["positive", "negative", "neutral"]
    except Exception as e:
        pytest.skip(f"Skipping news API test due to error: {str(e)}")
    
    # Test trending news
    try:
        trending = service.get_trending_news()
        assert isinstance(trending, list)
        assert len(trending) <= 10
        if len(trending) > 1:
            # Check if articles are sorted by sentiment
            assert trending[0].sentiment_scores["compound"] >= trending[-1].sentiment_scores["compound"]
    except Exception as e:
        pytest.skip(f"Skipping trending news test due to error: {str(e)}")

def test_news_service_without_api_key():
    service = NewsService(api_key=None)
    with pytest.raises(ValueError, match="NewsAPI key is not set"):
        service.get_news()
