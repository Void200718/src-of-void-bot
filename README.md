## Advanced Discord Bot (slash commands)

### Setup
- Create a `.env` file with:
```
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=.
```

### Run locally
```bash
pip install -r requirements.txt
python -m bot.main
```

### Deploy
- The Procfile runs: `worker: python -m bot.main`
- Runtime uses Python 3.11

### Features
- Slash commands: ping, uptime, avatar, translate
- Moderation: slowmode, purge, lock, unlock
- Structured logging and error handling