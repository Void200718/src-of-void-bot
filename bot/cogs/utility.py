from __future__ import annotations

import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class Utility(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="ping", description="Show the bot latency in milliseconds")
	async def ping(self, interaction: discord.Interaction) -> None:
		latency_ms = round(self.bot.latency * 1000)
		embed = discord.Embed(description=f"Latency: {latency_ms} ms", color=discord.Color.blurple())
		await interaction.response.send_message(embed=embed, ephemeral=True)

	@app_commands.command(name="uptime", description="Show how long the bot has been running")
	async def uptime(self, interaction: discord.Interaction) -> None:
		start_time = getattr(self.bot, "start_time", None)
		if start_time is None:
			await interaction.response.send_message("Uptime tracking not available yet.", ephemeral=True)
			return
		delta: datetime.timedelta = datetime.datetime.utcnow() - start_time
		hours, remainder = divmod(int(delta.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		embed = discord.Embed(
			title="Uptime",
			description=f"{hours}h {minutes}m {seconds}s",
			color=discord.Color.green(),
		)
		await interaction.response.send_message(embed=embed, ephemeral=True)

	@app_commands.command(name="avatar", description="Show a user's avatar")
	@app_commands.describe(user="The user to view")
	async def avatar(self, interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
		user = user or interaction.user
		embed = discord.Embed(title=f"Avatar for {user}", color=discord.Color.blurple())
		embed.set_image(url=user.display_avatar.url)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="say", description="Make the bot say a message")
	@app_commands.describe(message="What should I say?", ephemeral="Only you can see the response")
	async def say(self, interaction: discord.Interaction, message: str, ephemeral: bool = False) -> None:
		await interaction.response.send_message(message, ephemeral=ephemeral)

	@app_commands.command(name="sync", description="Sync application commands (owner only)")
	async def sync(self, interaction: discord.Interaction) -> None:
		owner_ids = getattr(getattr(self.bot, "settings", None), "owner_ids", [])
		if interaction.user.id not in owner_ids and owner_ids:
			await interaction.response.send_message("You are not authorized to run this.", ephemeral=True)
			return

		await interaction.response.defer(ephemeral=True)
		try:
			guild_ids = getattr(getattr(self.bot, "settings", None), "command_guild_ids", [])
			if guild_ids:
				for gid in guild_ids:
					await self.bot.tree.sync(guild=discord.Object(id=gid))
				await interaction.followup.send(f"Synced commands to guilds: {', '.join(map(str, guild_ids))}")
			else:
				await self.bot.tree.sync()
				await interaction.followup.send("Globally synced commands.")
		except Exception as exc:
			await interaction.followup.send(f"Sync failed: {exc}")


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Utility(bot))