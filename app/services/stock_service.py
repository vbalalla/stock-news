from typing import List
from ..models import Stock

class StockService:
    def __init__(self):
        # In-memory storage for top NYSE stocks by market cap
        self._stocks = [
            Stock(
                symbol="JPM",
                name="JPMorgan Chase & Co.",
                market_cap=415000000000,
                sector="Financial Services"
            ),
            Stock(
                symbol="V",
                name="Visa Inc.",
                market_cap=405000000000,
                sector="Financial Services"
            ),
            Stock(
                symbol="JNJ",
                name="Johnson & Johnson",
                market_cap=380000000000,
                sector="Healthcare"
            ),
            Stock(
                symbol="WMT",
                name="Walmart Inc.",
                market_cap=375000000000,
                sector="Consumer Defensive"
            ),
            Stock(
                symbol="PG",
                name="Procter & Gamble Co.",
                market_cap=350000000000,
                sector="Consumer Defensive"
            ),
            Stock(
                symbol="XOM",
                name="Exxon Mobil Corporation",
                market_cap=340000000000,
                sector="Energy"
            ),
            Stock(
                symbol="MA",
                name="Mastercard Incorporated",
                market_cap=335000000000,
                sector="Financial Services"
            ),
            Stock(
                symbol="CVX",
                name="Chevron Corporation",
                market_cap=285000000000,
                sector="Energy"
            ),
            Stock(
                symbol="HD",
                name="The Home Depot Inc.",
                market_cap=280000000000,
                sector="Consumer Cyclical"
            ),
            Stock(
                symbol="UNH",
                name="UnitedHealth Group Inc.",
                market_cap=275000000000,
                sector="Healthcare"
            )
        ]

    def get_stocks(self) -> List[Stock]:
        """Get list of top NYSE stocks"""
        return self._stocks

    def get_stock_by_symbol(self, symbol: str) -> Stock:
        """Get stock by symbol"""
        for stock in self._stocks:
            if stock.symbol == symbol:
                return stock
        return None

    def get_stock_symbols(self) -> List[str]:
        """Get list of all stock symbols"""
        return [stock.symbol for stock in self._stocks]
