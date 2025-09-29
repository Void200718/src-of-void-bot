# Advanced Discord Bot (Slash Commands)

Modern, secure Discord bot using discord.py v2 with slash commands, cogs, .env-based configuration, and optional diagnostics. The legacy script with hardcoded tokens has been removed.

## Setup

1. Create and fill your env file:
   - Copy `.env.example` to `.env` and set `DISCORD_TOKEN`.
   - Optionally set `GUILD_ID` for faster command sync during development.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run locally:
   - `python -m main`
4. Verify health/metrics endpoints (optional):
   - Health: `GET http://localhost:8080/healthz` returns `{ "status": "ok" }`.
   - Metrics: `GET http://localhost:8080/metrics` exposes Prometheus metrics (if `prometheus-client` is installed).

## Features
- Slash commands: `/ping`, `/avatar`, `/servericon`, `/uptime`, `/about`, `/badges`, `/addbadge`, `/health`
- Badges system persisted to `badges.json`
- Structured logging (`LOG_LEVEL=INFO` by default)
- Optional [jishaku](https://github.com/Gorialis/jishaku) developer extension
- Observability:
  - FastAPI health endpoint on port 8080
  - Prometheus metrics for command counts and latency
  - Global slash command error handling with friendly ephemeral replies

## Deploy

Heroku or container platforms are supported.

- Set `DISCORD_TOKEN` as a config var/secret.
- `Procfile` runs `python3 -m main` as a worker dyno.
- `runtime.txt` selects Python 3.11.

## Development Tips
- Set `GUILD_ID` to your test server ID for near-instant command sync.
- Use `LOG_LEVEL=DEBUG` to see more details during development.