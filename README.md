# StockPulse Insights

A SaaS application that provides real-time insights for the top 100 stocks using news data and NLP analysis.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
NEWS_API_KEY=your_api_key_here
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- GET `/stocks` - Get list of top 100 stocks
- GET `/news?stock_symbol={symbol}` - Get news articles, optionally filtered by stock symbol
- GET `/trending` - Get trending news across all stocks

## Running Tests

```bash
pytest tests/
```
