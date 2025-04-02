import pytest
from datetime import datetime
from app.services.relevance_service import RelevanceService
from app.models import NewsArticle

@pytest.fixture
def relevance_service():
    return RelevanceService()

@pytest.fixture
def sample_article():
    return NewsArticle(
        title="JPMorgan Chase Reports Strong Q4 Earnings",
        description="JPMorgan Chase & Co. announced better than expected earnings for Q4",
        url="http://example.com",
        published_at=datetime.now(),
        source="Test Source",
        sentiment_scores={"compound": 0.5, "pos": 0.6, "neg": 0.0, "neu": 0.4},
        sentiment="positive",
        related_stocks=["JPM"]
    )

def test_keyword_score(relevance_service, sample_article):
    score = relevance_service._calculate_keyword_score(
        f"{sample_article.title} {sample_article.description}",
        "JPM"
    )
    assert score > 0.0
    assert score <= 1.0
    
    # Test with irrelevant text
    score = relevance_service._calculate_keyword_score(
        "Unrelated news about technology",
        "JPM"
    )
    assert score == 0.0

def test_position_score(relevance_service, sample_article):
    score = relevance_service._calculate_position_score(
        f"{sample_article.title} {sample_article.description}",
        "JPM"
    )
    assert score > 0.0
    assert score <= 1.0
    
    # Test with symbol at end
    score = relevance_service._calculate_position_score(
        "Some unrelated text JPM",
        "JPM"
    )
    assert score < relevance_service._calculate_position_score(
        "JPM reports earnings",
        "JPM"
    )

def test_relevance_scoring(relevance_service, sample_article):
    # Test single article scoring
    score = relevance_service.calculate_relevance_score(sample_article, "JPM")
    assert score > 0.0
    assert score <= 1.0
    
    # Test irrelevant article
    irrelevant_article = NewsArticle(
        title="Tech News Today",
        description="News about technology sector",
        url="http://example.com",
        published_at=datetime.now(),
        source="Test Source",
        sentiment_scores={"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0},
        sentiment="neutral",
        related_stocks=[]
    )
    score = relevance_service.calculate_relevance_score(irrelevant_article, "JPM")
    assert score == 0.0

def test_article_sorting(relevance_service):
    articles = [
        NewsArticle(
            title="JPMorgan Chase Headlines",
            description="Major news about JPM",
            url="http://example.com/1",
            published_at=datetime.now(),
            source="Test Source",
            sentiment_scores={"compound": 0.5, "pos": 0.6, "neg": 0.0, "neu": 0.4},
            sentiment="positive",
            related_stocks=["JPM"]
        ),
        NewsArticle(
            title="Brief mention of JPM",
            description="Mostly about other topics",
            url="http://example.com/2",
            published_at=datetime.now(),
            source="Test Source",
            sentiment_scores={"compound": 0.3, "pos": 0.4, "neg": 0.0, "neu": 0.6},
            sentiment="positive",
            related_stocks=["JPM"]
        )
    ]
    
    scored_articles = relevance_service.score_articles(articles, "JPM")
    assert len(scored_articles) == 2
    assert scored_articles[0].relevance_score >= scored_articles[1].relevance_score
