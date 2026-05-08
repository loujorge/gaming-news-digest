# Gaming & Cinema News Digest

Daily automated digest of gaming and cinema news, sent directly to your WhatsApp group.

Aggregates news from 50+ sources (IGN, GameSpot, Polygon, Kotaku, Eurogamer, etc.), deduplicates, optionally summarizes with AI, and delivers via WhatsApp.

## Setup

```bash
git clone https://github.com/YOUR_USER/gaming-news-digest.git
cd gaming-news-digest
python -m venv venv
venv\Scripts\activate  # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Usage

```bash
python main.py
```

## Configuration

All config is via environment variables (`.env` file or GitHub Secrets):

| Variable | Required | Description |
|----------|----------|-------------|
| `WHATSAPP_PROVIDER` | Yes | `twilio` or `evolution` |
| `TWILIO_ACCOUNT_SID` | If Twilio | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | If Twilio | Twilio Auth Token |
| `TWILIO_FROM` | If Twilio | `whatsapp:+14155238886` |
| `TWILIO_TO` | If Twilio | `whatsapp:+5511...` |
| `EVOLUTION_API_URL` | If Evolution | Evolution API server URL |
| `EVOLUTION_API_KEY` | If Evolution | Evolution API key |
| `EVOLUTION_INSTANCE` | If Evolution | Instance name |
| `EVOLUTION_TO` | If Evolution | `5511...@s.whatsapp.net` |
| `ANTHROPIC_API_KEY` | No | For AI summarization |
| `SUMMARIZE` | No | `true` to enable AI summary (default: `false`) |
| `DEDUPE_THRESHOLD` | No | 0-100, similarity threshold (default: `85`) |
| `MAX_ARTICLES_PER_SOURCE` | No | Articles per feed (default: `5`) |

## Adding/Removing Sources

Edit `data/sources.json`. Each source needs:

```json
{
  "name": "Site Name",
  "url": "https://site.com/rss/feed",
  "category": "gaming",
  "language": "en",
  "enabled": true
}
```

Set `"enabled": false` to disable a source without removing it.

## WhatsApp Providers

**Twilio (recommended):** Reliable, official API. Requires Twilio account + WhatsApp sandbox or approved number.

**Evolution API (experimental):** Self-hosted, free. Requires server running Evolution API connected to WhatsApp Web.

## GitHub Actions (Scheduled)

The workflow runs daily at 08:00 BRT (11:00 UTC). Configure secrets in your repo:
Settings > Secrets and variables > Actions > New repository secret

You can also trigger manually: Actions > Daily Gaming & Cinema Digest > Run workflow

## Running Tests

```bash
pip install -r requirements.txt
pytest
```
