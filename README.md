# Advanced Discord Bot (Slash Commands)

Modern, secure Discord bot using discord.py v2 with slash commands, cogs, .env-based configuration, and optional diagnostics. The legacy script with hardcoded tokens has been removed.

## Setup

1. Create and fill your env file:
   - Copy `.env.example` to `.env` and set `DISCORD_TOKEN`.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run locally:
   - `python -m main`

## Features
- Slash commands: `/ping`, `/avatar`, `/servericon`, `/uptime`, `/about`
- Badges system: `/badges`, `/addbadge`
- Structured logging and optional jishaku extension

## Deploy

Heroku via `Procfile` is supported. Ensure `DISCORD_TOKEN` is set as a config var.