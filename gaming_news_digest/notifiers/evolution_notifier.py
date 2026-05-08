from __future__ import annotations

import logging

import requests

from gaming_news_digest.notifiers.base import BaseNotifier

logger = logging.getLogger(__name__)


class EvolutionNotifier(BaseNotifier):
    def __init__(self, api_url: str, api_key: str, instance: str, to: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.instance = instance
        self.to = to
        self.headers = {"apikey": api_key, "Content-Type": "application/json"}
        logger.info("EvolutionNotifier initialized (instance: %s)", instance)

    def send(self, message: str) -> bool:
        url = f"{self.api_url}/message/sendText/{self.instance}"
        payload = {"number": self.to, "textMessage": {"text": message}}

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            logger.info("Message sent via Evolution API (status: %d)", response.status_code)
            return True
        except requests.RequestException as e:
            logger.error("Evolution API send failed: %s", e)
            return False
