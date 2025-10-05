from __future__ import annotations

import importlib
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


def is_owner_or_allowed():
	async def predicate(interaction: discord.Interaction) -> bool:
		bot = interaction.client
		owner_ids = getattr(getattr(bot, "settings", None), "owner_ids", [])
		return (not owner_ids) or (interaction.user.id in owner_ids)

	return app_commands.check(predicate)


class Admin(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="sync", description="Sync application commands (owner only)")
	@is_owner_or_allowed()
	async def sync(self, interaction: discord.Interaction) -> None:
		await interaction.response.defer(ephemeral=True)
		guild_ids = getattr(getattr(self.bot, "settings", None), "command_guild_ids", [])
		if guild_ids:
			for gid in guild_ids:
				await self.bot.tree.sync(guild=discord.Object(id=gid))
			await interaction.followup.send(f"Synced commands to guilds: {', '.join(map(str, guild_ids))}")
		else:
			await self.bot.tree.sync()
			await interaction.followup.send("Globally synced commands.")

	@app_commands.command(name="setactivity", description="Set the bot's presence text (owner only)")
	@is_owner_or_allowed()
	@app_commands.describe(text="The activity text to set")
	async def setactivity(self, interaction: discord.Interaction, text: str) -> None:
		activity = discord.Activity(type=discord.ActivityType.watching, name=text)
		await self.bot.change_presence(status=discord.Status.online, activity=activity)
		await interaction.response.send_message(f"Activity set to: {text}", ephemeral=True)

	@app_commands.command(name="load", description="Load an extension (owner only)")
	@is_owner_or_allowed()
	@app_commands.describe(extension="Dotted path, e.g., bot.cogs.utility")
	async def load(self, interaction: discord.Interaction, extension: str) -> None:
		await interaction.response.defer(ephemeral=True)
		try:
			await self.bot.load_extension(extension)
			await interaction.followup.send(f"Loaded: {extension}")
		except Exception as exc:
			await interaction.followup.send(f"Load failed: {exc}")

	@app_commands.command(name="unload", description="Unload an extension (owner only)")
	@is_owner_or_allowed()
	@app_commands.describe(extension="Dotted path, e.g., bot.cogs.utility")
	async def unload(self, interaction: discord.Interaction, extension: str) -> None:
		await interaction.response.defer(ephemeral=True)
		try:
			await self.bot.unload_extension(extension)
			await interaction.followup.send(f"Unloaded: {extension}")
		except Exception as exc:
			await interaction.followup.send(f"Unload failed: {exc}")

	@app_commands.command(name="reload", description="Reload an extension (owner only)")
	@is_owner_or_allowed()
	@app_commands.describe(extension="Dotted path, e.g., bot.cogs.utility")
	async def reload(self, interaction: discord.Interaction, extension: str) -> None:
		await interaction.response.defer(ephemeral=True)
		try:
			await self.bot.reload_extension(extension)
			await interaction.followup.send(f"Reloaded: {extension}")
		except Exception as exc:
			await interaction.followup.send(f"Reload failed: {exc}")


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Admin(bot))

