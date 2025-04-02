from pydantic import BaseModel
from typing import Optional, List
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
    sentiment: Optional[float] = None
    relevance_score: Optional[float] = None
    related_stocks: List[str] = []
