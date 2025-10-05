import platform
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._started_at = time.monotonic()

    @app_commands.command(name="ping", description="Show bot latency in milliseconds")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(description=f"Pong! {latency_ms} ms", color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Get a user's avatar")
    async def avatar(self, interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
        target = user or interaction.user
        embed = discord.Embed(title=f"Avatar for {target}", color=discord.Color.blurple())
        embed.set_image(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="servericon", description="Get this server's icon")
    @app_commands.guild_only()
    async def servericon(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if not guild or not guild.icon:
            await interaction.response.send_message("No server icon.", ephemeral=True)
            return
        embed = discord.Embed(title=guild.name, color=discord.Color.blurple())
        embed.set_image(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uptime", description="Show how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction) -> None:
        delta = time.monotonic() - self._started_at
        hours, rem = divmod(int(delta), 3600)
        minutes, seconds = divmod(rem, 60)
        await interaction.response.send_message(f"Uptime: {hours}h {minutes}m {seconds}s")

    @app_commands.command(name="about", description="Show information about the bot")
    async def about(self, interaction: discord.Interaction) -> None:
        py = platform.python_version()
        embed = discord.Embed(title="Advanced Bot", color=discord.Color.blurple())
        embed.add_field(name="Python", value=py)
        embed.add_field(name="Library", value=f"discord.py {discord.__version__}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))

