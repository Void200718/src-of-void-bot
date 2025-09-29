import asyncio
import logging
import sys
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from .config import get_config
from .logging_config import setup_logging
from .health import start_health_app


log = logging.getLogger("bot")


class AdvancedBot(commands.Bot):
    def __init__(self, *, guild_id: Optional[int] = None) -> None:
        intents = discord.Intents.default()
        # No privileged intents required for these commands. Enable as needed.
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=None,
        )
        self.target_guild_id = guild_id

    async def setup_hook(self) -> None:
        await self._load_cogs()
        await self._sync_commands()

    async def _load_cogs(self) -> None:
        try:
            await self.load_extension("bot.cogs.general")
            await self.load_extension("bot.cogs.badges")
            try:
                await self.load_extension("jishaku")
            except Exception:
                # Jishaku is optional; ignore if not installed
                pass
            log.info("Cogs loaded successfully")
        except Exception as exc:
            log.exception("Failed to load cogs: %s", exc)
            raise

    async def _sync_commands(self) -> None:
        # Sync either to a specific guild for fast iteration or globally
        if self.target_guild_id:
            guild = discord.Object(id=self.target_guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info("Synced %d commands to guild %s", len(synced), self.target_guild_id)
        else:
            synced = await self.tree.sync()
            log.info("Globally synced %d commands", len(synced))

    async def on_ready(self) -> None:
        log.info("Logged in as %s (ID: %s)", self.user, getattr(self.user, "id", "?"))
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )


def main() -> None:
    setup_logging()
    # Start lightweight health server (useful for containers/Heroku)
    start_health_app()
    try:
        cfg = get_config()
    except Exception as exc:
        # Ensure a clean error on missing token
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(2)

    bot = AdvancedBot(guild_id=cfg.guild_id)
    try:
        bot.run(cfg.discord_token, log_handler=None)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

