from gaming_news_digest.deduplicator import deduplicate_articles
from gaming_news_digest.fetcher import Article


def test_removes_exact_duplicates(duplicate_articles):
    result = deduplicate_articles(duplicate_articles, threshold=85)
    assert len(result) == 1


def test_keeps_distinct_articles(sample_articles):
    result = deduplicate_articles(sample_articles, threshold=85)
    assert len(result) == len(sample_articles)


def test_empty_input():
    result = deduplicate_articles([], threshold=85)
    assert result == []


def test_strict_threshold_keeps_similar():
    articles = [
        Article("Elden Ring DLC Released", "https://a.com", "", "", "IGN", "gaming"),
        Article("Elden Ring DLC: Now Released", "https://b.com", "", "", "GameSpot", "gaming"),
    ]
    result = deduplicate_articles(articles, threshold=100)
    assert len(result) == 2


def test_loose_threshold_removes_more():
    articles = [
        Article("Elden Ring DLC Released", "https://a.com", "", "", "IGN", "gaming"),
        Article("Elden Ring DLC: Now Released", "https://b.com", "", "", "GameSpot", "gaming"),
    ]
    result = deduplicate_articles(articles, threshold=50)
    assert len(result) == 1
