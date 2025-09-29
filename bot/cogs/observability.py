from __future__ import annotations

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger("bot.observability")

try:
	from prometheus_client import Counter, Histogram
	_METRICS_AVAILABLE = True
except Exception:  # pragma: no cover
	_METRICS_AVAILABLE = False

if _METRICS_AVAILABLE:
	COMMANDS_TOTAL = Counter(
		"discord_commands_total",
		"Total number of slash command invocations",
		["command", "status"],
	)
	COMMAND_LATENCY = Histogram(
		"discord_command_latency_seconds",
		"Latency of slash command execution in seconds",
		["command"],
	)
else:
	COMMANDS_TOTAL = None
	COMMAND_LATENCY = None


class Observability(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@commands.Cog.listener()
	async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command) -> None:
		if _METRICS_AVAILABLE and COMMANDS_TOTAL and COMMAND_LATENCY:
			COMMANDS_TOTAL.labels(command=command.qualified_name, status="success").inc()

	@commands.Cog.listener()
	async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
		# Record metric
		if _METRICS_AVAILABLE and COMMANDS_TOTAL:
			name = getattr(interaction.command, "qualified_name", "<unknown>")
			COMMANDS_TOTAL.labels(command=name, status="error").inc()

		# Provide user-friendly ephemeral reply if not already responded
		try:
			if interaction.response.is_done():
				await interaction.followup.send("Sorry, an error occurred while processing your command.", ephemeral=True)
			else:
				await interaction.response.send_message("Sorry, an error occurred while processing your command.", ephemeral=True)
		except Exception:
			pass

	@app_commands.command(name="health", description="Report bot health and latency")
	async def health(self, interaction: discord.Interaction) -> None:
		latency_ms = round(self.bot.latency * 1000)
		embed = discord.Embed(description=f"OK - {latency_ms} ms", color=discord.Color.green())
		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Observability(bot))