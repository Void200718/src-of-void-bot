from __future__ import annotations

from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.paginator import EmbedPaginatorView


class Help(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="help", description="Show a paginated list of commands")
	async def help(self, interaction: discord.Interaction) -> None:
		commands_list = self.bot.tree.get_commands()
		commands_list.sort(key=lambda c: c.name)
		page_size = 8
		embeds: List[discord.Embed] = []
		for i in range(0, len(commands_list), page_size):
			chunk = commands_list[i : i + page_size]
			desc_lines = [f"`/{cmd.name}` — {cmd.description or 'No description'}" for cmd in chunk]
			embed = discord.Embed(title="Commands", description="\n".join(desc_lines), color=discord.Color.blurple())
			embeds.append(embed)
		if not embeds:
			embeds = [discord.Embed(title="Commands", description="No commands registered.")]
		view = EmbedPaginatorView(embeds=embeds, author_id=interaction.user.id)
		await view.send(interaction)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Help(bot))

