import datetime as dt
import discord
from discord import app_commands
from discord.ext import commands

try:
    from googletrans import Translator
except Exception:
    Translator = None  # type: ignore


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Show bot latency in milliseconds")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {latency_ms} ms")

    @app_commands.command(name="uptime", description="Show how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction) -> None:
        started: dt.datetime = getattr(self.bot, "start_time", dt.datetime.utcnow())
        delta: dt.timedelta = dt.datetime.utcnow() - started
        days, remainder = divmod(int(delta.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        await interaction.response.send_message("Uptime: " + " ".join(parts))

    @app_commands.command(name="avatar", description="Show the avatar of a user")
    async def avatar(self, interaction: discord.Interaction, user: discord.User | None = None) -> None:
        target = user or interaction.user
        embed = discord.Embed(title=f"Avatar — {target}")
        if target.display_avatar:
            embed.set_image(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="translate", description="Translate text to a target language code (e.g., en, es)")
    async def translate(self, interaction: discord.Interaction, lang: str, *, text: str) -> None:
        if Translator is None:
            await interaction.response.send_message("Translation service unavailable.", ephemeral=True)
            return
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        await interaction.response.send_message(translated.text)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))

