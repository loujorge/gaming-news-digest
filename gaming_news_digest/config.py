from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl

logger = logging.getLogger(__name__)


class SourceItem(BaseModel):
    name: str
    url: str
    category: str
    language: str = "en"
    enabled: bool = True


@dataclass
class AppConfig:
    anthropic_api_key: str | None = None
    summarize: bool = False
    notification_provider: str = "telegram"
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_from: str | None = None
    twilio_to: str | None = None
    evolution_api_url: str | None = None
    evolution_api_key: str | None = None
    evolution_instance: str | None = None
    evolution_to: str | None = None
    dedupe_threshold: int = 85
    max_articles_per_source: int = 5
    log_level: str = "INFO"
    sources_path: str = "data/sources.json"

    def __repr__(self) -> str:
        return (
            f"AppConfig(provider={self.notification_provider}, "
            f"summarize={self.summarize}, "
            f"dedupe_threshold={self.dedupe_threshold}, "
            f"sources_path={self.sources_path})"
        )


def _mask_key(value: str | None) -> str:
    if not value or len(value) <= 4:
        return "***"
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def load_config() -> AppConfig:
    load_dotenv()

    config = AppConfig(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        summarize=os.getenv("SUMMARIZE", "false").lower() == "true",
        notification_provider=os.getenv("NOTIFICATION_PROVIDER", "telegram").lower(),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        twilio_from=os.getenv("TWILIO_FROM"),
        twilio_to=os.getenv("TWILIO_TO"),
        evolution_api_url=os.getenv("EVOLUTION_API_URL"),
        evolution_api_key=os.getenv("EVOLUTION_API_KEY"),
        evolution_instance=os.getenv("EVOLUTION_INSTANCE"),
        evolution_to=os.getenv("EVOLUTION_TO"),
        dedupe_threshold=int(os.getenv("DEDUPE_THRESHOLD") or "85"),
        max_articles_per_source=int(os.getenv("MAX_ARTICLES_PER_SOURCE") or "5"),
        log_level=os.getenv("LOG_LEVEL") or "INFO",
        sources_path=os.getenv("SOURCES_PATH") or "data/sources.json",
    )

    logger.info("Config loaded: %s", config)
    return config


def load_sources(sources_path: str) -> list[SourceItem]:
    path = Path(sources_path)
    if not path.exists():
        raise FileNotFoundError(f"Sources file not found: {sources_path}")

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    sources: list[SourceItem] = []
    for i, entry in enumerate(raw):
        try:
            item = SourceItem(**entry)
            if item.enabled:
                sources.append(item)
        except Exception as e:
            logger.warning("Skipping invalid source at index %d: %s", i, e)

    if not sources:
        raise ValueError("No valid enabled sources found in sources.json")

    logger.info("Loaded %d sources from %s", len(sources), sources_path)
    return sources
