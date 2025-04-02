import requests
from datetime import datetime
from typing import List, Optional
from ..models import NewsArticle
import json

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self._news_cache = []  # In-memory storage for news articles

    def fetch_news(self, query: str = None) -> List[NewsArticle]:
        """Fetch news from NewsAPI"""
        if not self.api_key:
            raise ValueError("NewsAPI key is not set")

        endpoint = f"{self.base_url}/everything"
        params = {
            "apiKey": self.api_key,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "q": query if query else "stock market OR finance OR investing"  # Default query
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses
            articles = response.json().get("articles", [])
            
            return [
                NewsArticle(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")),
                    source=article["source"]["name"],
                    sentiment=0.0,  # Placeholder for sentiment analysis
                    relevance_score=1.0,  # Placeholder for relevance scoring
                    related_stocks=[]
                )
                for article in articles
            ]
        except requests.exceptions.RequestException as e:
            raise Exception(f"NewsAPI error: {str(e)}")

    def get_news(self, stock_symbol: Optional[str] = None) -> List[NewsArticle]:
        """Get news articles, optionally filtered by stock symbol"""
        if not self._news_cache:
            self._news_cache = self.fetch_news()

        if stock_symbol:
            return [
                article for article in self._news_cache
                if stock_symbol in article.related_stocks
            ]
        return self._news_cache

    def get_trending_news(self) -> List[NewsArticle]:
        """Get trending news across all stocks"""
        if not self._news_cache:
            self._news_cache = self.fetch_news()
        
        # Sort by relevance score and return top 10
        return sorted(
            self._news_cache,
            key=lambda x: x.relevance_score or 0,
            reverse=True
        )[:10]
