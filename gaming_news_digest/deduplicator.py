from __future__ import annotations

import logging
import re

from rapidfuzz import fuzz

from gaming_news_digest.fetcher import Article

logger = logging.getLogger(__name__)


def _normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    return re.sub(r"\s+", " ", title).strip()


def deduplicate_articles(articles: list[Article], threshold: int = 85) -> list[Article]:
    unique: list[Article] = []
    seen_titles: list[str] = []

    for article in articles:
        norm = _normalize_title(article.title)
        is_dup = False
        for seen in seen_titles:
            if fuzz.token_sort_ratio(norm, seen) >= threshold:
                is_dup = True
                break
        if not is_dup:
            unique.append(article)
            seen_titles.append(norm)

    removed = len(articles) - len(unique)
    if removed:
        logger.info("Deduplication removed %d articles (%d remaining)", removed, len(unique))
    return unique
