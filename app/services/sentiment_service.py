from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from typing import Dict, Union, List

class SentimentService:
    def __init__(self):
        """Initialize the sentiment analyzer"""
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a text and return scores
        
        Returns:
            Dict with keys: compound, pos, neg, neu
            compound: normalized score between -1 (negative) and 1 (positive)
        """
        if not text:
            return {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0}
        return self.analyzer.polarity_scores(text)

    def get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to sentiment label"""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score <= -0.05:
            return "negative"
        else:
            return "neutral"

    def analyze_articles(self, articles: List[dict]) -> List[dict]:
        """Analyze sentiment for a list of articles"""
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            scores = self.analyze_text(text)
            article['sentiment_scores'] = scores
            article['sentiment'] = self.get_sentiment_label(scores['compound'])
        return articles
