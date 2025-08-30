import os
import logging
import asyncio
import datetime as dt
import discord
from discord.ext import commands
from discord import app_commands

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


class AdvancedBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        prefix = os.getenv("BOT_PREFIX", ".")
        super().__init__(command_prefix=prefix, intents=intents, case_insensitive=True)

        self.start_time: dt.datetime = dt.datetime.utcnow()
        self.synced: bool = False

    async def setup_hook(self) -> None:
        await self.load_extension("bot.cogs.utility")
        await self.load_extension("bot.cogs.moderation")

    async def on_ready(self) -> None:
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        activity = discord.Activity(type=discord.ActivityType.watching, name="the server")
        await self.change_presence(status=discord.Status.online, activity=activity)
        logging.getLogger(__name__).info("Logged in as %s (%s)", self.user, self.user and self.user.id)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.send(f"Error: {error}")


async def _run() -> None:
    if load_dotenv is not None:
        load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Missing DISCORD_TOKEN in environment.")

    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    bot = AdvancedBot()

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        logging.getLogger(__name__).exception("App command error: %s", error)
        if interaction.response.is_done():
            await interaction.followup.send(f"Error: {error}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

    await bot.start(token, reconnect=True)


def main() -> None:
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

