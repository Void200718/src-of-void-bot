# Advanced Discord Bot

A modern, secure Discord bot using discord.py v2 with slash commands, environment-based configuration, and clean structure.

## Features
- Slash commands (`/ping`, `/uptime`, `/avatar`, `/say`, `/sync`)
- Env-based configuration with `.env`
- Optional per-guild command sync or global sync
- Structured logging with colorized output
- Minimal dependencies and Python 3.11 runtime

## Getting Started

### 1) Requirements
- Python 3.11+
- A Discord Bot token

### 2) Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your own values
```

### 3) Run locally
```bash
python -m bot
```

### Environment variables
- `DISCORD_TOKEN` (required): Your bot token
- `COMMAND_GUILD_IDS` (optional): Comma-separated guild IDs for faster per-guild command sync
- `BOT_OWNERS` (optional): Comma-separated user IDs allowed to run `/sync`
- `BOT_ACTIVITY` (optional): Presence text
- `SYNC_ON_STARTUP` (default: `true`): Whether to sync app commands at startup
- `LOG_LEVEL` (default: `INFO`): Logging level

### Deploy
Procfile is configured to run the worker:
```
worker: python -m bot
```

## Project Structure
```
bot/
  __init__.py
  __main__.py
  bot.py
  config.py
  cogs/
    __init__.py
    utility.py
```

## Security Notes
- Secrets must not be committed. Use `.env` locally and environment variables in production.
- The previous legacy script with a hard-coded token was removed.