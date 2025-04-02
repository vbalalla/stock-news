from typing import List
from ..models import Stock

class StockService:
    def __init__(self):
        # In-memory storage for top 100 stocks
        self._stocks = [
            Stock(
                symbol="AAPL",
                name="Apple Inc.",
                market_cap=2800000000000,
                sector="Technology"
            ),
            Stock(
                symbol="MSFT",
                name="Microsoft Corporation",
                market_cap=2700000000000,
                sector="Technology"
            ),
            # Add more stocks as needed
        ]

    def get_stocks(self) -> List[Stock]:
        """Get list of top 100 stocks"""
        return self._stocks

    def get_stock_by_symbol(self, symbol: str) -> Stock:
        """Get stock by symbol"""
        for stock in self._stocks:
            if stock.symbol == symbol:
                return stock
        return None
