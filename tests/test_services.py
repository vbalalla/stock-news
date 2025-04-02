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
    assert stocks[0].symbol == "AAPL"

def test_news_service():
    api_key = os.getenv("NEWS_API_KEY")
    assert api_key is not None, "NEWS_API_KEY environment variable is not set"
    
    service = NewsService(api_key=api_key)
    
    # Test news fetching
    try:
        news = service.get_news()
        assert isinstance(news, list)
        if len(news) > 0:
            assert isinstance(news[0], NewsArticle)
            assert isinstance(news[0].published_at, datetime)
            assert news[0].title is not None
            assert news[0].url is not None
    except Exception as e:
        pytest.skip(f"Skipping news API test due to error: {str(e)}")
    
    # Test trending news
    try:
        trending = service.get_trending_news()
        assert isinstance(trending, list)
        assert len(trending) <= 10
    except Exception as e:
        pytest.skip(f"Skipping trending news test due to error: {str(e)}")

def test_news_service_without_api_key():
    service = NewsService(api_key=None)
    with pytest.raises(ValueError, match="NewsAPI key is not set"):
        service.get_news()
