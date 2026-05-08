from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timezone

from gaming_news_digest.fetcher import Article

logger = logging.getLogger(__name__)


def format_digest_plaintext(articles: list[Article]) -> str:
    today = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    grouped: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        grouped[a.category.upper()].append(a)

    lines = [f"*Gaming & Cinema Digest - {today}*", ""]

    for category in sorted(grouped.keys()):
        lines.append(f"*=== {category} ===*")
        for a in grouped[category][:15]:
            lines.append(f"- {a.title} ({a.source_name})")
            lines.append(f"  {a.url}")
        lines.append("")

    lines.append(f"_Total: {len(articles)} noticias de {len(set(a.source_name for a in articles))} fontes_")
    return "\n".join(lines)


def _build_prompt(articles: list[Article]) -> str:
    lines = []
    for i, a in enumerate(articles[:30], 1):
        lines.append(f"[{i}] [{a.category.upper()}] {a.title} ({a.source_name})")
        if a.summary:
            lines.append(f"    {a.summary[:200]}")

    articles_text = "\n".join(lines)

    return (
        "Es um assistente de noticias de gaming e cinema. "
        "Abaixo estao as noticias mais recentes. "
        "Cria um digest conciso em portugues, agrupado por categoria (Gaming / Cinema). "
        "Para cada categoria, lista as 5-10 noticias mais importantes com 1 frase cada. "
        "Formata para WhatsApp: usa *negrito* para titulos e categorias. "
        "Maximo 3500 caracteres no total.\n\n"
        f"NOTICIAS:\n{articles_text}"
    )


def summarize_articles(articles: list[Article], api_key: str) -> str:
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = _build_prompt(articles)

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        result = response.content[0].text
        logger.info(
            "Summarization complete: %d input tokens, %d output tokens",
            response.usage.input_tokens,
            response.usage.output_tokens,
        )
        return result

    except Exception as e:
        logger.error("Summarization failed, falling back to plaintext: %s", e)
        return format_digest_plaintext(articles)
