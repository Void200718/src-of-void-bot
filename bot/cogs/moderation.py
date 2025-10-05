from __future__ import annotations

from typing import Optional
import datetime

import discord
from discord import app_commands
from discord.ext import commands


def guild_only():
	async def predicate(interaction: discord.Interaction) -> bool:
		return interaction.guild is not None

	return app_commands.check(predicate)


class Moderation(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="purge", description="Delete a number of recent messages")
	@guild_only()
	@app_commands.checks.has_permissions(manage_messages=True)
	@app_commands.describe(amount="How many messages to delete (max 100)")
	async def purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]) -> None:
		channel = interaction.channel
		if not isinstance(channel, (discord.TextChannel, discord.Thread)):
			await interaction.response.send_message("Unsupported channel type.", ephemeral=True)
			return
		await interaction.response.defer(ephemeral=True)
		deleted = await channel.purge(limit=amount, check=lambda m: True)
		await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)

	@app_commands.command(name="kick", description="Kick a member")
	@guild_only()
	@app_commands.checks.has_permissions(kick_members=True)
	@app_commands.describe(member="Member to kick", reason="Reason for kick")
	async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None) -> None:
		await interaction.guild.kick(member, reason=reason)
		await interaction.response.send_message(f"Kicked {member}.", ephemeral=True)

	@app_commands.command(name="ban", description="Ban a member")
	@guild_only()
	@app_commands.checks.has_permissions(ban_members=True)
	@app_commands.describe(member="Member to ban", reason="Reason for ban", delete_messages_days="Delete message history (0-7 days)")
	async def ban(
		self,
		interaction: discord.Interaction,
		member: discord.Member,
		reason: Optional[str] = None,
		delete_messages_days: app_commands.Range[int, 0, 7] = 0,
	) -> None:
		await interaction.guild.ban(member, reason=reason, delete_message_days=delete_messages_days)
		await interaction.response.send_message(f"Banned {member}.", ephemeral=True)

	@app_commands.command(name="timeout", description="Timeout a member for minutes")
	@guild_only()
	@app_commands.checks.has_permissions(moderate_members=True)
	@app_commands.describe(member="Member to timeout", minutes="Duration in minutes", reason="Reason")
	async def timeout(
		self,
		interaction: discord.Interaction,
		member: discord.Member,
		minutes: app_commands.Range[int, 1, 40320],  # up to 28 days
		reason: Optional[str] = None,
	) -> None:
		duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
		await member.timeout(until=duration, reason=reason)
		await interaction.response.send_message(f"Timed out {member} for {minutes} minutes.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Moderation(bot))

