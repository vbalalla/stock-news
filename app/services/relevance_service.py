from transformers import pipeline
from typing import List, Dict, Optional
import re
from collections import Counter
from models import NewsArticle
from services.stock_service import StockService

class RelevanceService:
    def __init__(self):
        """Initialize the relevance service with stock data"""
        self.stock_service = StockService()
        self.stocks = self.stock_service.get_stocks()
        self.stock_keywords = self._build_stock_keywords()
        
    def _build_stock_keywords(self) -> Dict[str, List[str]]:
        """Build a dictionary of stock symbols and related keywords"""
        keywords = {}
        for stock in self.stocks:
            # Add symbol and company name variations
            company_words = stock.name.lower().split()
            keywords[stock.symbol] = [
                stock.symbol.lower(),
                *company_words,
                ''.join(company_words),  # joined version
                stock.name.lower().replace(' ', '')  # no spaces
            ]
            if stock.sector:
                keywords[stock.symbol].append(stock.sector.lower())
        return keywords
    
    def _calculate_keyword_score(self, text: str, stock_symbol: str) -> float:
        """Calculate relevance score based on keyword frequency"""
        if not text or not stock_symbol:
            return 0.0
            
        text = text.lower()
        keywords = self.stock_keywords.get(stock_symbol, [])
        if not keywords:
            return 0.0
            
        # Count keyword occurrences
        score = 0.0
        for keyword in keywords:
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
            # Higher weight for symbol matches
            if keyword == stock_symbol.lower():
                score += count * 2.0
            else:
                score += count * 1.0
                
        # Normalize score (0 to 1)
        return min(1.0, score / 5.0)  # Cap at 1.0, assume 5 mentions is max relevance
        
    def _calculate_position_score(self, text: str, stock_symbol: str) -> float:
        """Calculate relevance based on keyword positions in text"""
        if not text or not stock_symbol:
            return 0.0
            
        text = text.lower()
        text_length = len(text)
        if text_length == 0:
            return 0.0
            
        # Find positions of stock symbol and company name
        symbol_pos = text.find(stock_symbol.lower())
        company_name = next((stock.name.lower() for stock in self.stocks 
                           if stock.symbol == stock_symbol), '')
        company_pos = text.find(company_name)
        
        # Calculate position scores (earlier mentions are more relevant)
        score = 0.0
        if symbol_pos != -1:
            score += 1.0 * (1 - (symbol_pos / text_length))
        if company_pos != -1:
            score += 0.8 * (1 - (company_pos / text_length))
            
        return min(1.0, score)
        
    def calculate_relevance_score(self, article: NewsArticle, stock_symbol: Optional[str] = None) -> float:
        """Calculate overall relevance score for an article"""
        if stock_symbol is None:
            # If no stock specified, use the first mentioned stock
            if article.related_stocks:
                stock_symbol = article.related_stocks[0]
            else:
                return 0.0
                
        # Combine title and description for analysis
        text = f"{article.title} {article.description or ''}"
        
        # Calculate individual scores
        keyword_score = self._calculate_keyword_score(text, stock_symbol)
        position_score = self._calculate_position_score(text, stock_symbol)
        
        # Sentiment impact (boost score for strong sentiment)
        sentiment_impact = abs(article.sentiment_scores.get('compound', 0))
        
        # Combine scores with weights
        final_score = (
            keyword_score * 0.5 +  # 50% weight for keyword frequency
            position_score * 0.3 +  # 30% weight for position
            sentiment_impact * 0.2  # 20% weight for sentiment impact
        )
        
        return round(final_score, 3)  # Round to 3 decimal places
        
    def score_articles(self, articles: List[NewsArticle], stock_symbol: Optional[str] = None) -> List[NewsArticle]:
        """Score a list of articles and update their relevance scores"""
        for article in articles:
            article.relevance_score = self.calculate_relevance_score(article, stock_symbol)
        return sorted(articles, key=lambda x: x.relevance_score or 0, reverse=True)
