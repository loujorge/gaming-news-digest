from unittest.mock import MagicMock

from gaming_news_digest.config import SourceItem
from gaming_news_digest.fetcher import _extract_article, fetch_articles_from_source


def _mock_entry(title=None, link=None, summary="", published="2024-01-01"):
    entry = MagicMock()
    entry.title = title
    entry.link = link
    entry.summary = summary
    entry.description = summary
    entry.published = published
    entry.updated = published
    return entry


def test_extract_article_valid():
    source = SourceItem(name="IGN", url="https://ign.com/rss", category="gaming")
    entry = _mock_entry(title="Test Title", link="https://example.com/article")
    article = _extract_article(entry, source)
    assert article is not None
    assert article.title == "Test Title"
    assert article.source_name == "IGN"


def test_extract_article_missing_title():
    source = SourceItem(name="IGN", url="https://ign.com/rss", category="gaming")
    entry = _mock_entry(title=None, link="https://example.com/article")
    assert _extract_article(entry, source) is None


def test_extract_article_missing_link():
    source = SourceItem(name="IGN", url="https://ign.com/rss", category="gaming")
    entry = _mock_entry(title="Title", link=None)
    assert _extract_article(entry, source) is None


def test_extract_article_strips_html():
    source = SourceItem(name="IGN", url="https://ign.com/rss", category="gaming")
    entry = _mock_entry(
        title="Test",
        link="https://example.com",
        summary="<p>Hello <b>world</b></p>",
    )
    article = _extract_article(entry, source)
    assert article is not None
    assert "<" not in article.summary
    assert "Hello world" in article.summary


def test_fetch_from_source_handles_error(monkeypatch):
    source = SourceItem(name="Broken", url="https://broken.invalid/rss", category="gaming")
    monkeypatch.setattr(
        "gaming_news_digest.fetcher._parse_feed",
        lambda url: (_ for _ in ()).throw(Exception("Network error")),
    )
    result = fetch_articles_from_source(source)
    assert result == []
