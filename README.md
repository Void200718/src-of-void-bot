# Advanced Discord Bot

A modern, secure Discord bot using discord.py v2 with slash commands, environment-based configuration, and clean structure.

## Features
- Slash commands (`/ping`, `/uptime`, `/avatar`, `/say`, `/sync`)
- Env-based configuration with `.env`
- Optional per-guild command sync or global sync
- Structured logging with colorized output
- Minimal dependencies and Python 3.11 runtime
- Dynamic cog auto-loader (`bot.cogs.*`), optional `jishaku` diagnostics
- SQLite via `aiosqlite` with WAL and a `tags` table ready
- Reusable paginator view for multi-page embeds

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
- `DATABASE_PATH` (default: `data/bot.db`): Path to SQLite DB

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
    admin.py
    moderation.py
    info.py
    fun.py
    tags.py
    help.py
  utils/
    __init__.py
    paginator.py
```

## Security Notes
- Secrets must not be committed. Use `.env` locally and environment variables in production.
- The previous legacy script with a hard-coded token was removed.

## New Slash Commands

- Admin: `/sync`, `/setactivity`, `/load`, `/unload`, `/reload`
- Moderation: `/purge`, `/kick`, `/ban`, `/timeout`
- Info: `/serverinfo`, `/userinfo`, `/botstats`
- Fun: `/roll`, `/choose`, `/8ball`
- Tags: `/tag_create`, `/tag`, `/tag_delete`, `/tags`

Tip: Add your user ID to `BOT_OWNERS` to use Admin commands.