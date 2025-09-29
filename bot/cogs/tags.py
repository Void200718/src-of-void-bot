from __future__ import annotations

import time
from typing import Optional, List

import discord
from discord import app_commands
from discord.ext import commands

try:
	import aiosqlite  # type: ignore
except Exception:  # pragma: no cover
	aiosqlite = None  # type: ignore

from bot.utils.paginator import EmbedPaginatorView


def db_required():
	async def predicate(interaction: discord.Interaction) -> bool:
		return getattr(interaction.client, "db", None) is not None

	return app_commands.check(predicate)


class Tags(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="tag_create", description="Create or update a tag in this server")
	@db_required()
	@app_commands.describe(name="Tag name", content="Tag content")
	async def tag_create(self, interaction: discord.Interaction, name: str, content: str) -> None:
		name = name.strip().lower()
		if not name:
			await interaction.response.send_message("Tag name cannot be empty.", ephemeral=True)
			return
		db = getattr(self.bot, "db", None)
		assert db is not None
		await db.execute(
			"INSERT INTO tags (guild_id, name, content, author_id, created_at) VALUES (?, ?, ?, ?, ?)\n"
			"ON CONFLICT(guild_id, name) DO UPDATE SET content=excluded.content, author_id=excluded.author_id, created_at=excluded.created_at",
			(interaction.guild_id, name, content, interaction.user.id, int(time.time())),
		)
		await db.commit()
		await interaction.response.send_message(f"Saved tag '{name}'.", ephemeral=True)

	@app_commands.command(name="tag", description="Show a tag by name")
	@db_required()
	@app_commands.describe(name="Tag name")
	async def tag_get(self, interaction: discord.Interaction, name: str) -> None:
		db = getattr(self.bot, "db", None)
		assert db is not None
		async with db.execute("SELECT content FROM tags WHERE guild_id=? AND name=?", (interaction.guild_id, name.lower())) as cur:
			row = await cur.fetchone()
			if row is None:
				await interaction.response.send_message("Tag not found.", ephemeral=True)
				return
			await interaction.response.send_message(row[0])

	@app_commands.command(name="tag_delete", description="Delete a tag")
	@db_required()
	@app_commands.describe(name="Tag name")
	async def tag_delete(self, interaction: discord.Interaction, name: str) -> None:
		db = getattr(self.bot, "db", None)
		assert db is not None
		await db.execute("DELETE FROM tags WHERE guild_id=? AND name=?", (interaction.guild_id, name.lower()))
		await db.commit()
		await interaction.response.send_message(f"Deleted tag '{name}'.", ephemeral=True)

	@app_commands.command(name="tags", description="List tags in this server")
	@db_required()
	async def tags(self, interaction: discord.Interaction) -> None:
		db = getattr(self.bot, "db", None)
		assert db is not None
		async with db.execute("SELECT name, author_id, created_at FROM tags WHERE guild_id=? ORDER BY name ASC", (interaction.guild_id,)) as cur:
			rows = await cur.fetchall()
			if not rows:
				await interaction.response.send_message("No tags yet.", ephemeral=True)
				return
			page_size = 10
			embeds: List[discord.Embed] = []
			for i in range(0, len(rows), page_size):
				chunk = rows[i : i + page_size]
				desc_lines = [
					f"`{name}` — by <@{author_id}> — <t:{created_at}:R>" for (name, author_id, created_at) in chunk
				]
				embed = discord.Embed(title="Tags", description="\n".join(desc_lines), color=discord.Color.blurple())
				embeds.append(embed)
			view = EmbedPaginatorView(embeds=embeds, author_id=interaction.user.id)
			await view.send(interaction)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Tags(bot))

