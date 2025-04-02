from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import NewsArticle, Stock
from .services.news_service import NewsService
from .services.stock_service import StockService
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("NEWS_API_KEY")
logger.info(f"Loaded NEWS_API_KEY: {'Present' if api_key else 'Missing'}")

app = FastAPI(title="StockPulse Insights")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
news_service = NewsService(api_key=api_key)
stock_service = StockService()

@app.get("/stocks")
async def get_stocks():
    """Get list of top 100 stocks"""
    return stock_service.get_stocks()

@app.get("/news")
async def get_news(stock_symbol: str = None):
    """Get news articles, optionally filtered by stock symbol"""
    try:
        return news_service.get_news(stock_symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending")
async def get_trending_news():
    """Get trending news across all stocks"""
    try:
        return news_service.get_trending_news()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
