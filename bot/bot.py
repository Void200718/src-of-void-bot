from __future__ import annotations

import datetime
import logging
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from .config import BotSettings


class AdvancedBot(commands.Bot):
	def __init__(self, settings: BotSettings) -> None:
		intents = discord.Intents.default()
		intents.message_content = True
		intents.members = True

		super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents)

		self.settings = settings
		self.start_time: datetime.datetime = datetime.datetime.utcnow()
		self.log = logging.getLogger("bot")

	async def setup_hook(self) -> None:
		# Load cogs/extensions
		await self.load_extension("bot.cogs.utility")

		# Optionally sync commands on startup
		if self.settings.sync_on_startup:
			await self._sync_app_commands()

	async def _sync_app_commands(self) -> None:
		guild_ids: List[int] = self.settings.command_guild_ids
		try:
			if guild_ids:
				for gid in guild_ids:
					await self.tree.sync(guild=discord.Object(id=gid))
				self.log.info("Synced %d app commands to guilds: %s", len(self.tree.get_commands()), guild_ids)
			else:
				await self.tree.sync()
				self.log.info("Globally synced %d app commands", len(self.tree.get_commands()))
		except Exception:
			self.log.exception("Failed to sync app commands")

	async def on_ready(self) -> None:
		activity = discord.Activity(type=discord.ActivityType.watching, name=self.settings.activity_text)
		await self.change_presence(status=discord.Status.online, activity=activity)
		self.log.info("Logged in as %s (%s)", self.user, getattr(self.user, "id", "?"))

	async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		self.log.exception("App command error: %s", error)
		try:
			if interaction.response.is_done():
				await interaction.followup.send("Something went wrong executing that command.", ephemeral=True)
			else:
				await interaction.response.send_message("Something went wrong executing that command.", ephemeral=True)
		except Exception:
			pass