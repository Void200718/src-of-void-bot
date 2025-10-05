from __future__ import annotations

from typing import List, Optional

import discord


class EmbedPaginatorView(discord.ui.View):
	def __init__(self, *, embeds: List[discord.Embed], author_id: Optional[int] = None, timeout: Optional[float] = 180.0) -> None:
		super().__init__(timeout=timeout)
		self.embeds = embeds
		self.author_id = author_id
		self.current_index = 0

	@property
	def total_pages(self) -> int:
		return max(1, len(self.embeds))

	def _update_buttons(self) -> None:
		self.prev_button.disabled = self.current_index <= 0  # type: ignore[attr-defined]
		self.next_button.disabled = self.current_index >= (self.total_pages - 1)  # type: ignore[attr-defined]

	async def send(self, interaction: discord.Interaction) -> None:
		self._update_buttons()
		await interaction.response.send_message(embed=self._with_footer(self.embeds[self.current_index]), view=self)

	def _with_footer(self, embed: discord.Embed) -> discord.Embed:
		try:
			copy = embed.copy()
		except Exception:
			copy = embed
		page_text = f"Page {self.current_index + 1}/{self.total_pages}"
		if copy.footer and copy.footer.text:
			copy.set_footer(text=f"{copy.footer.text} • {page_text}")
		else:
			copy.set_footer(text=page_text)
		return copy

	@discord.ui.button(label="Prev", style=discord.ButtonStyle.secondary)
	async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:  # type: ignore[override]
		if not self._is_allowed(interaction):
			await interaction.response.send_message("You're not allowed to control this paginator.", ephemeral=True)
			return
		self.current_index = max(0, self.current_index - 1)
		self._update_buttons()
		await interaction.response.edit_message(embed=self._with_footer(self.embeds[self.current_index]), view=self)

	@discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
	async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:  # type: ignore[override]
		if not self._is_allowed(interaction):
			await interaction.response.send_message("You're not allowed to control this paginator.", ephemeral=True)
			return
		self.current_index = min(self.total_pages - 1, self.current_index + 1)
		self._update_buttons()
		await interaction.response.edit_message(embed=self._with_footer(self.embeds[self.current_index]), view=self)

	@discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
	async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:  # type: ignore[override]
		if not self._is_allowed(interaction):
			await interaction.response.send_message("You're not allowed to control this paginator.", ephemeral=True)
			return
		for child in self.children:
			if isinstance(child, discord.ui.Button):
				child.disabled = True
		await interaction.response.edit_message(view=self)
		self.stop()

	def _is_allowed(self, interaction: discord.Interaction) -> bool:
		return self.author_id is None or interaction.user.id == self.author_id

