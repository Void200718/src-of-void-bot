from __future__ import annotations

import datetime
import logging
import os
import pkgutil
import importlib
from typing import List, Optional

import discord
from discord import app_commands
from discord.ext import commands

try:
    import aiosqlite  # type: ignore
except Exception:  # pragma: no cover - optional at import time, ensured by requirements
    aiosqlite = None  # type: ignore

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
		self.db: Optional["aiosqlite.Connection"] = None

	async def setup_hook(self) -> None:
		# Ensure database is ready (and folder exists)
		await self._ensure_database()

		# Load core/optional extensions dynamically
		await self._auto_load_extensions()

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

	async def _auto_load_extensions(self) -> None:
		"""Auto-discover and load all cogs in bot.cogs package."""
		try:
			import bot.cogs as cogs_pkg  # local import to ensure package is available
		except Exception:
			self.log.exception("Failed to import cogs package")
			return

		loaded: List[str] = []
		for module_info in pkgutil.iter_modules(cogs_pkg.__path__, prefix="bot.cogs."):
			name = module_info.name
			leaf = name.rsplit(".", 1)[-1]
			if leaf.startswith("_"):
				continue
			try:
				await self.load_extension(name)
				loaded.append(name)
			except Exception:
				self.log.exception("Failed to load extension %s", name)

		# Try to load jishaku if installed for diagnostics
		try:
			await self.load_extension("jishaku")
			loaded.append("jishaku")
		except Exception:
			pass

		if loaded:
			self.log.info("Loaded extensions: %s", ", ".join(loaded))

	async def _ensure_database(self) -> None:
		"""Create the database file and required tables if needed."""
		if aiosqlite is None:
			self.log.warning("aiosqlite not available; database features disabled")
			return

		db_path = self.settings.database_path
		db_dir = os.path.dirname(db_path)
		if db_dir and not os.path.exists(db_dir):
			os.makedirs(db_dir, exist_ok=True)

		self.db = await aiosqlite.connect(db_path)
		self.db.row_factory = aiosqlite.Row  # type: ignore[attr-defined]
		await self.db.execute("PRAGMA journal_mode=WAL;")
		await self.db.execute(
			"""
			CREATE TABLE IF NOT EXISTS tags (
				guild_id    INTEGER NOT NULL,
				name        TEXT    NOT NULL,
				content     TEXT    NOT NULL,
				author_id   INTEGER NOT NULL,
				created_at  INTEGER NOT NULL,
				PRIMARY KEY (guild_id, name)
			);
			"""
		)
		await self.db.commit()

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

	async def close(self) -> None:  # type: ignore[override]
		try:
			if self.db is not None:
				await self.db.close()
		except Exception:
			self.log.exception("Error while closing database")
		await super().close()