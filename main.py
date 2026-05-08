from __future__ import annotations

import logging
import sys

from gaming_news_digest.config import load_config, load_sources
from gaming_news_digest.deduplicator import deduplicate_articles
from gaming_news_digest.fetcher import fetch_all_articles
from gaming_news_digest.history import filter_new_articles, load_history, save_history
from gaming_news_digest.notifiers import get_notifier
from gaming_news_digest.summarizer import format_digest_plaintext, summarize_articles


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run_pipeline() -> None:
    config = load_config()
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)

    logger.info("Starting Gaming & Cinema News Digest pipeline")

    sources = load_sources(config.sources_path)
    logger.info("Fetching articles from %d sources...", len(sources))

    raw_articles = fetch_all_articles(sources, config.max_articles_per_source)
    if not raw_articles:
        logger.warning("No articles fetched from any source. Exiting.")
        return

    articles = deduplicate_articles(raw_articles, config.dedupe_threshold)
    logger.info("After deduplication: %d articles", len(articles))

    sent_urls = load_history()
    articles = filter_new_articles(articles, sent_urls)
    if not articles:
        logger.info("No new articles to send. Exiting.")
        return

    if config.summarize and config.anthropic_api_key:
        logger.info("Generating AI summary with Claude Haiku...")
        digest = summarize_articles(articles, config.anthropic_api_key)
    else:
        logger.info("Generating plaintext digest...")
        digest = format_digest_plaintext(articles)

    logger.info("Digest length: %d characters", len(digest))

    notifier = get_notifier(config)
    success = notifier.send_chunked(digest)

    if success:
        logger.info("Digest sent successfully!")
        new_urls = {a.url for a in articles}
        save_history(sent_urls | new_urls)
    else:
        logger.error("Failed to send digest")
        sys.exit(1)


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logging.getLogger(__name__).critical("Pipeline failed: %s", e, exc_info=True)
        sys.exit(1)
