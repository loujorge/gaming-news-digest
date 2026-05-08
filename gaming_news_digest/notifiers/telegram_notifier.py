from __future__ import annotations

import logging

import requests

from gaming_news_digest.notifiers.base import BaseNotifier

logger = logging.getLogger(__name__)


class TelegramNotifier(BaseNotifier):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        logger.info("TelegramNotifier initialized (chat_id: %s)", chat_id)

    def send(self, message: str) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "disable_web_page_preview": True,
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            logger.info("Message sent via Telegram (chat_id: %s)", self.chat_id)
            return True
        except requests.RequestException as e:
            logger.error("Telegram send failed: %s", e)
            return False
