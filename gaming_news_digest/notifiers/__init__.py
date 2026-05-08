from __future__ import annotations

from gaming_news_digest.config import AppConfig
from gaming_news_digest.notifiers.base import BaseNotifier
from gaming_news_digest.notifiers.evolution_notifier import EvolutionNotifier
from gaming_news_digest.notifiers.telegram_notifier import TelegramNotifier
from gaming_news_digest.notifiers.twilio_notifier import TwilioNotifier


def get_notifier(config: AppConfig) -> BaseNotifier:
    provider = config.notification_provider

    if provider == "telegram":
        if not all([config.telegram_bot_token, config.telegram_chat_id]):
            raise ValueError("Telegram requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        return TelegramNotifier(
            bot_token=config.telegram_bot_token,  # type: ignore
            chat_id=config.telegram_chat_id,  # type: ignore
        )

    if provider == "twilio":
        if not all([config.twilio_account_sid, config.twilio_auth_token, config.twilio_from, config.twilio_to]):
            raise ValueError("Twilio requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO")
        return TwilioNotifier(
            account_sid=config.twilio_account_sid,  # type: ignore
            auth_token=config.twilio_auth_token,  # type: ignore
            from_number=config.twilio_from,  # type: ignore
            to_number=config.twilio_to,  # type: ignore
        )

    if provider == "evolution":
        if not all([config.evolution_api_url, config.evolution_api_key, config.evolution_instance, config.evolution_to]):
            raise ValueError("Evolution API requires EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE, EVOLUTION_TO")
        return EvolutionNotifier(
            api_url=config.evolution_api_url,  # type: ignore
            api_key=config.evolution_api_key,  # type: ignore
            instance=config.evolution_instance,  # type: ignore
            to=config.evolution_to,  # type: ignore
        )

    raise ValueError(f"Unknown provider: '{provider}'. Use 'telegram', 'twilio', or 'evolution'.")
