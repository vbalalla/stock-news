import requests
from typing import List, Optional
from datetime import datetime
from models import NewsArticle
from .sentiment_service import SentimentService
from .relevance_service import RelevanceService

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self._news_cache = []  # In-memory storage for news articles
        self.sentiment_service = SentimentService()
        self.relevance_service = RelevanceService()

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
            "q": query if query else "(NYSE OR 'New York Stock Exchange') AND (stock OR market OR trading)"
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            
            processed_articles = []
            for article in articles:
                # Create article object
                news_article = NewsArticle(
                    title=article["title"],
                    description=article.get("description", ""),
                    url=article["url"],
                    published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")),
                    source=article["source"]["name"],
                    related_stocks=self._extract_stock_mentions(article["title"] + " " + (article.get("description") or ""))
                )
                
                # Analyze sentiment
                text = f"{news_article.title} {news_article.description}"
                sentiment_scores = self.sentiment_service.analyze_text(text)
                news_article.sentiment_scores = sentiment_scores
                news_article.sentiment = self.sentiment_service.get_sentiment_label(sentiment_scores["compound"])
                
                processed_articles.append(news_article)
            
            # Score articles for relevance
            processed_articles = self.relevance_service.score_articles(processed_articles)
            return processed_articles
        except requests.exceptions.RequestException as e:
            raise Exception(f"NewsAPI error: {str(e)}")

    def _extract_stock_mentions(self, text: str) -> List[str]:
        """Extract stock symbols from text"""
        from services.stock_service import StockService
        stock_service = StockService()
        stock_symbols = stock_service.get_stock_symbols()
        
        # Simple extraction: check if stock symbol is mentioned in text
        mentioned_stocks = []
        for symbol in stock_symbols:
            if symbol in text.upper().split():
                mentioned_stocks.append(symbol)
        return mentioned_stocks

    def get_news(self, stock_symbol: Optional[str] = None) -> List[NewsArticle]:
        """Get news articles, optionally filtered by stock symbol"""
        if not self._news_cache:
            self._news_cache = self.fetch_news()

        articles = [
            article for article in self._news_cache
            if not stock_symbol or stock_symbol in article.related_stocks
        ]
        
        # Score articles specifically for the requested stock
        if stock_symbol:
            articles = self.relevance_service.score_articles(articles, stock_symbol)
        return articles

    def get_trending_news(self) -> List[NewsArticle]:
        """Get trending news across all stocks, prioritizing positive sentiment and relevance"""
        if not self._news_cache:
            self._news_cache = self.fetch_news()
        
        # Sort by a combination of sentiment and relevance
        return sorted(
            self._news_cache,
            key=lambda x: (x.sentiment_scores["compound"] + (x.relevance_score or 0)) / 2,
            reverse=True
        )[:10]
