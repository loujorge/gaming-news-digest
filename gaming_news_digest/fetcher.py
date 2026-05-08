from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import feedparser
from tenacity import retry, stop_after_attempt, wait_exponential

from gaming_news_digest.config import SourceItem

logger = logging.getLogger(__name__)


@dataclass
class Article:
    title: str
    url: str
    summary: str
    published: str
    source_name: str
    category: str


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=1, max=10))
def _parse_feed(url: str) -> feedparser.FeedParserDict:
    return feedparser.parse(url)


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _extract_article(entry, source: SourceItem) -> Article | None:
    title = getattr(entry, "title", None)
    link = getattr(entry, "link", None)
    if not title or not link:
        return None

    summary_raw = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
    summary = _strip_html(summary_raw)[:500]

    published = getattr(entry, "published", "") or getattr(entry, "updated", "") or ""

    return Article(
        title=title.strip()[:300],
        url=link.strip(),
        summary=summary,
        published=published,
        source_name=source.name,
        category=source.category,
    )


def fetch_articles_from_source(source: SourceItem, max_articles: int = 5) -> list[Article]:
    try:
        feed = _parse_feed(source.url)
        articles = []
        for entry in feed.entries[:max_articles]:
            article = _extract_article(entry, source)
            if article:
                articles.append(article)
        logger.info("%s: %d articles fetched", source.name, len(articles))
        return articles
    except Exception as e:
        logger.error("Failed to fetch %s: %s", source.name, e)
        return []


def fetch_all_articles(sources: list[SourceItem], max_per_source: int = 5) -> list[Article]:
    all_articles: list[Article] = []
    for source in sources:
        articles = fetch_articles_from_source(source, max_per_source)
        all_articles.extend(articles)

    logger.info("Total articles fetched: %d from %d sources", len(all_articles), len(sources))
    return all_articles
