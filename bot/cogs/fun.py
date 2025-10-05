from __future__ import annotations

import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="roll", description="Roll an NdM dice, e.g., 2d6")
	@app_commands.describe(spec="Format NdM, e.g., 1d20", ephemeral="Only you can see the result")
	async def roll(self, interaction: discord.Interaction, spec: str = "1d20", ephemeral: bool = False) -> None:
		try:
			n_str, m_str = spec.lower().split("d", 1)
			n = max(1, min(100, int(n_str)))
			m = max(2, min(1000, int(m_str)))
		except Exception:
			await interaction.response.send_message("Invalid format. Use NdM like 2d6.", ephemeral=True)
			return
		rolls = [random.randint(1, m) for _ in range(n)]
		total = sum(rolls)
		await interaction.response.send_message(f"Rolled {n}d{m}: {rolls} = {total}", ephemeral=ephemeral)

	@app_commands.command(name="choose", description="Choose one option from a list")
	@app_commands.describe(options="Comma-separated options", ephemeral="Only you can see the result")
	async def choose(self, interaction: discord.Interaction, options: str, ephemeral: bool = False) -> None:
		choices = [opt.strip() for opt in options.split(",") if opt.strip()]
		if not choices:
			await interaction.response.send_message("Provide at least one option.", ephemeral=True)
			return
		pick = random.choice(choices)
		await interaction.response.send_message(f"I choose: {pick}", ephemeral=ephemeral)

	@app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
	@app_commands.describe(question="Your question", ephemeral="Only you can see the result")
	async def eightball(self, interaction: discord.Interaction, question: str, ephemeral: bool = False) -> None:
		responses = [
			"It is certain.",
			"Without a doubt.",
			"You may rely on it.",
			"Yes, definitely.",
			"It is decidedly so.",
			"As I see it, yes.",
			"Most likely.",
			"Outlook good.",
			"Yes.",
			"Signs point to yes.",
			"Reply hazy, try again.",
			"Ask again later.",
			"Better not tell you now.",
			"Cannot predict now.",
			"Concentrate and ask again.",
			"Don't count on it.",
			"My reply is no.",
			"My sources say no.",
			"Outlook not so good.",
			"Very doubtful.",
		]
		await interaction.response.send_message(random.choice(responses), ephemeral=ephemeral)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Fun(bot))

