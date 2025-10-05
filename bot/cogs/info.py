from __future__ import annotations

import datetime
import platform
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import psutil


class Info(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="serverinfo", description="Show information about this server")
	async def serverinfo(self, interaction: discord.Interaction) -> None:
		guild = interaction.guild
		if guild is None:
			await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
			return
		embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blurple())
		embed.add_field(name="ID", value=str(guild.id))
		embed.add_field(name="Members", value=str(guild.member_count))
		embed.add_field(name="Owner", value=str(guild.owner) if guild.owner else "?")
		created = discord.utils.format_dt(guild.created_at, style="R")
		embed.add_field(name="Created", value=created)
		if guild.icon:
			embed.set_thumbnail(url=guild.icon.url)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="userinfo", description="Show information about a user")
	@app_commands.describe(user="The user to view")
	async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.Member] = None) -> None:
		member = user or interaction.user
		embed = discord.Embed(title=f"User Info: {member}", color=discord.Color.green())
		embed.add_field(name="ID", value=str(member.id))
		created = discord.utils.format_dt(member.created_at, style="R")
		embed.add_field(name="Created", value=created)
		if isinstance(member, discord.Member):
			joined = discord.utils.format_dt(member.joined_at, style="R") if member.joined_at else "?"
			embed.add_field(name="Joined", value=joined)
			roles = ", ".join(r.mention for r in member.roles[1:]) or "None"
			embed.add_field(name="Roles", value=roles, inline=False)
		if member.display_avatar:
			embed.set_thumbnail(url=member.display_avatar.url)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="botstats", description="Show bot and system statistics")
	async def botstats(self, interaction: discord.Interaction) -> None:
		process = psutil.Process()
		with process.oneshot():
			uptime_seconds = max(0, int(time.time() - process.create_time()))
			mem_info = process.memory_full_info()
			rss_mb = mem_info.rss / (1024 * 1024)
			cpu_percent = process.cpu_percent(interval=0.1)
			num_threads = process.num_threads()

		py_ver = platform.python_version()
		dpy_ver = discord.__version__
		guilds = len(self.bot.guilds)
		users = sum(g.member_count or 0 for g in self.bot.guilds)

		hours, remainder = divmod(uptime_seconds, 3600)
		minutes, seconds = divmod(remainder, 60)

		embed = discord.Embed(title="Bot Statistics", color=discord.Color.gold())
		embed.add_field(name="Guilds", value=str(guilds))
		embed.add_field(name="Users", value=str(users))
		embed.add_field(name="Python", value=py_ver)
		embed.add_field(name="discord.py", value=dpy_ver)
		embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s")
		embed.add_field(name="CPU %", value=f"{cpu_percent:.1f}%")
		embed.add_field(name="Memory", value=f"{rss_mb:.1f} MiB")
		embed.add_field(name="Threads", value=str(num_threads))
		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Info(bot))

