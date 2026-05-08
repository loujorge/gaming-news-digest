import pytest

from gaming_news_digest.config import AppConfig
from gaming_news_digest.notifiers import get_notifier
from gaming_news_digest.notifiers.base import BaseNotifier


class FakeNotifier(BaseNotifier):
    def __init__(self):
        self.sent: list[str] = []

    def send(self, message: str) -> bool:
        self.sent.append(message)
        return True


def test_chunk_message_under_limit():
    notifier = FakeNotifier()
    chunks = notifier._chunk_message("short message", max_chars=4096)
    assert len(chunks) == 1
    assert chunks[0] == "short message"


def test_chunk_message_splits():
    notifier = FakeNotifier()
    long_msg = "\n".join([f"Line {i}: some content here" for i in range(200)])
    chunks = notifier._chunk_message(long_msg, max_chars=500)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 500


def test_send_chunked_success():
    notifier = FakeNotifier()
    result = notifier.send_chunked("hello world", max_chars=4096)
    assert result is True
    assert len(notifier.sent) == 1


def test_send_chunked_multiple():
    notifier = FakeNotifier()
    long_msg = "\n".join([f"Line {i}" for i in range(100)])
    result = notifier.send_chunked(long_msg, max_chars=200)
    assert result is True
    assert len(notifier.sent) > 1


def test_get_notifier_invalid_provider():
    config = AppConfig(notification_provider="discord")
    with pytest.raises(ValueError, match="Unknown provider"):
        get_notifier(config)


def test_get_notifier_telegram_missing_config():
    config = AppConfig(notification_provider="telegram")
    with pytest.raises(ValueError, match="Telegram requires"):
        get_notifier(config)


def test_get_notifier_twilio_missing_config():
    config = AppConfig(notification_provider="twilio")
    with pytest.raises(ValueError, match="Twilio requires"):
        get_notifier(config)
