import pytest
from app.services.sentiment_service import SentimentService

def test_sentiment_analysis():
    service = SentimentService()
    
    # Test positive sentiment
    text = "The company reported excellent earnings, beating all expectations"
    scores = service.analyze_text(text)
    assert scores["compound"] > 0
    assert service.get_sentiment_label(scores["compound"]) == "positive"
    
    # Test negative sentiment
    text = "The stock crashed after disappointing quarterly results"
    scores = service.analyze_text(text)
    assert scores["compound"] < 0
    assert service.get_sentiment_label(scores["compound"]) == "negative"
    
    # Test neutral sentiment
    text = "The company released its quarterly report today"
    scores = service.analyze_text(text)
    assert service.get_sentiment_label(scores["compound"]) == "neutral"
    
    # Test empty text
    scores = service.analyze_text("")
    assert scores["compound"] == 0.0
    assert service.get_sentiment_label(scores["compound"]) == "neutral"

def test_sentiment_labels():
    service = SentimentService()
    
    assert service.get_sentiment_label(0.5) == "positive"
    assert service.get_sentiment_label(-0.5) == "negative"
    assert service.get_sentiment_label(0.0) == "neutral"
    assert service.get_sentiment_label(0.04) == "neutral"  # Test threshold
