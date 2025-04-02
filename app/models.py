from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class Stock(BaseModel):
    symbol: str
    name: str
    market_cap: float
    sector: Optional[str] = None

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    published_at: datetime
    source: str
    sentiment_scores: Dict[str, float] = {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0}
    sentiment: str = "neutral"
    relevance_score: Optional[float] = None
    related_stocks: List[str] = []
