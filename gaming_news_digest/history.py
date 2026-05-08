from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from gaming_news_digest.fetcher import Article

logger = logging.getLogger(__name__)

HISTORY_FILE = "data/history.json"
MAX_HISTORY_ENTRIES = 5000


def load_history(path: str = HISTORY_FILE) -> set[str]:
    file = Path(path)
    if not file.exists():
        return set()

    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
        urls = set(data.get("sent_urls", []))
        logger.info("Loaded %d URLs from history", len(urls))
        return urls
    except Exception as e:
        logger.warning("Failed to load history, starting fresh: %s", e)
        return set()


def save_history(sent_urls: set[str], path: str = HISTORY_FILE) -> None:
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)

    urls_list = sorted(sent_urls)
    if len(urls_list) > MAX_HISTORY_ENTRIES:
        urls_list = urls_list[-MAX_HISTORY_ENTRIES:]

    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": len(urls_list),
        "sent_urls": urls_list,
    }

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info("Saved %d URLs to history", len(urls_list))


def filter_new_articles(articles: list[Article], sent_urls: set[str]) -> list[Article]:
    new = [a for a in articles if a.url not in sent_urls]
    skipped = len(articles) - len(new)
    if skipped:
        logger.info("Filtered out %d already-sent articles (%d new)", skipped, len(new))
    return new
