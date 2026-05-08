from __future__ import annotations

import logging

from twilio.rest import Client

from gaming_news_digest.notifiers.base import BaseNotifier

logger = logging.getLogger(__name__)


class TwilioNotifier(BaseNotifier):
    def __init__(self, account_sid: str, auth_token: str, from_number: str, to_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
        self.to_number = to_number
        logger.info("TwilioNotifier initialized")

    def send(self, message: str) -> bool:
        try:
            msg = self.client.messages.create(
                from_=self.from_number,
                to=self.to_number,
                body=message,
            )
            logger.info("Message sent via Twilio (SID: %s)", msg.sid)
            return True
        except Exception as e:
            logger.error("Twilio send failed: %s", e)
            return False
