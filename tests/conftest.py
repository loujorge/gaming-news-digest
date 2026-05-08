import pytest

from gaming_news_digest.fetcher import Article


@pytest.fixture
def sample_articles() -> list[Article]:
    return [
        Article(
            title="Elden Ring DLC Release Date Announced",
            url="https://example.com/elden-ring",
            summary="FromSoftware reveals the release date.",
            published="2024-01-15",
            source_name="IGN",
            category="gaming",
        ),
        Article(
            title="GTA 6 Trailer Breaks Records",
            url="https://example.com/gta6",
            summary="Rockstar's new trailer reaches 100M views.",
            published="2024-01-15",
            source_name="GameSpot",
            category="gaming",
        ),
        Article(
            title="New Marvel Movie Announced for 2025",
            url="https://example.com/marvel",
            summary="MCU expands with a new title.",
            published="2024-01-15",
            source_name="Screen Rant",
            category="cinema",
        ),
    ]


@pytest.fixture
def duplicate_articles() -> list[Article]:
    return [
        Article(
            title="Elden Ring DLC Release Date Announced",
            url="https://example.com/elden-ring-1",
            summary="FromSoftware reveals the date.",
            published="2024-01-15",
            source_name="IGN",
            category="gaming",
        ),
        Article(
            title="Elden Ring DLC: Release Date Has Been Announced",
            url="https://example.com/elden-ring-2",
            summary="The date is finally here.",
            published="2024-01-15",
            source_name="GameSpot",
            category="gaming",
        ),
    ]
