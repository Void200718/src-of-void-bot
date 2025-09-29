import json
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


BADGES_PATH = Path("badges.json")


def _load_badges() -> dict:
    if not BADGES_PATH.exists():
        return {}
    try:
        with BADGES_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_badges(data: dict) -> None:
    with BADGES_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class Badges(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="badges", description="List a user's badges")
    async def badges(self, interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
        target = user or interaction.user
        data = _load_badges()
        entries = data.get(str(target.id), [])
        if not entries:
            await interaction.response.send_message(f"{target.mention} has no badges.", ephemeral=True)
            return
        embed = discord.Embed(title=f"Badges for {target}", description="\n".join(entries), color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addbadge", description="Add a badge to a user")
    @app_commands.checks.has_permissions(administrator=True)
    async def addbadge(self, interaction: discord.Interaction, user: discord.User, badge: str) -> None:
        data = _load_badges()
        data.setdefault(str(user.id), []).append(badge)
        _save_badges(data)
        await interaction.response.send_message(f"Added badge '{badge}' to {user.mention}.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Badges(bot))

