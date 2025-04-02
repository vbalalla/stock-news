import json
from typing import List, Optional
import os
from polygon import RESTClient
from models import Stock
from dotenv import load_dotenv
import time

class StockService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.client = RESTClient(api_key=self.api_key)
        self._stocks_cache = None
        self._cache_symbols = None
        self._dev_mode = True  # Set to False in production

    def _get_test_stocks(self) -> List[Stock]:
        """Get test stock data for development"""
        return [
            Stock(
                symbol="AAPL",
                name="Apple Inc.",
                market_cap=3000000000000,
                sector="Technology"
            ),
            Stock(
                symbol="MSFT",
                name="Microsoft Corporation",
                market_cap=2800000000000,
                sector="Technology"
            ),
            Stock(
                symbol="GOOGL",
                name="Alphabet Inc.",
                market_cap=1800000000000,
                sector="Technology"
            ),
            Stock(
                symbol="AMZN",
                name="Amazon.com Inc.",
                market_cap=1600000000000,
                sector="Consumer Cyclical"
            ),
            Stock(
                symbol="NVDA",
                name="NVIDIA Corporation",
                market_cap=1400000000000,
                sector="Technology"
            )
        ]

    def get_stocks(self) -> List[Stock]:
        """Get a list of top stocks by market cap"""
        if self._dev_mode:
            return self._get_test_stocks()

        if self._stocks_cache is not None:
            return self._stocks_cache

        try:
            # Get top tickers
            tickers = self.client.list_tickers(market="stocks", active=True, limit=100)
            stocks = []
            
            for ticker in tickers:
                try:
                    # Sleep to avoid rate limits
                    time.sleep(0.2)
                    
                    # Get company details
                    details = self.client.get_ticker_details(ticker.ticker)
                    
                    stock = Stock(
                        symbol=ticker.ticker,
                        name=details.name if details else ticker.ticker,
                        market_cap=ticker.market_cap if hasattr(ticker, 'market_cap') else None,
                        sector=details.sic_description if details else None
                    )
                    stocks.append(stock)
                except Exception as e:
                    print(f"Error fetching details for {ticker.ticker}: {e}")
                    continue

            # Sort by market cap
            stocks.sort(key=lambda x: x.market_cap or 0, reverse=True)
            self._stocks_cache = stocks
            self._cache_symbols = {s.symbol for s in stocks}
            return stocks
        except Exception as e:
            print(f"Error fetching stocks: {e}")
            return self._get_test_stocks()  # Fallback to test data

    def get_stock_by_symbol(self, symbol: str) -> Optional[Stock]:
        """Get a specific stock by its symbol"""
        if self._dev_mode:
            test_stocks = self._get_test_stocks()
            return next((s for s in test_stocks if s.symbol == symbol), None)

        try:
            # Try to find in cache first
            if self._stocks_cache:
                stock = next((s for s in self._stocks_cache if s.symbol == symbol), None)
                if stock:
                    return stock

            # If not in cache, fetch directly
            ticker = self.client.get_ticker_details(symbol)
            if not ticker:
                return None

            # Get latest price to estimate market cap
            aggs = self.client.get_aggs(symbol, 1, "day", "2023-01-01", "2025-12-31", limit=1)
            market_cap = None
            if aggs and len(aggs) > 0 and hasattr(ticker, 'share_class_shares_outstanding'):
                market_cap = aggs[0].close * ticker.share_class_shares_outstanding

            return Stock(
                symbol=symbol,
                name=ticker.name,
                market_cap=market_cap,
                sector=ticker.sic_description
            )
        except Exception as e:
            print(f"Error fetching stock {symbol}: {e}")
            # Try test data as fallback
            test_stocks = self._get_test_stocks()
            return next((s for s in test_stocks if s.symbol == symbol), None)

    def get_stock_symbols(self) -> List[str]:
        """Get a list of all stock symbols"""
        if self._dev_mode:
            return [s.symbol for s in self._get_test_stocks()]

        if self._cache_symbols is not None:
            return list(self._cache_symbols)
        
        stocks = self.get_stocks()
        return [stock.symbol for stock in stocks]
