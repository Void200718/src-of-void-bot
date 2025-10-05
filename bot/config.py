from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


def _parse_int_list(env_name: str) -> List[int]:
	raw = os.getenv(env_name, "").strip()
	if not raw:
		return []
	values: List[int] = []
	for chunk in raw.replace(" ", "").split(","):
		if not chunk:
			continue
		try:
			values.append(int(chunk))
		except ValueError:
			# Ignore invalid values quietly; keep moving
			continue
	return values


@dataclass
class BotSettings:
	token: str
	command_guild_ids: List[int]
	owner_ids: List[int]
	activity_text: str
	sync_on_startup: bool
	database_path: str

	@staticmethod
	def from_env() -> "BotSettings":
		token = os.getenv("DISCORD_TOKEN", "").strip()
		if not token:
			raise RuntimeError("Missing DISCORD_TOKEN in environment")

		command_guild_ids = _parse_int_list("COMMAND_GUILD_IDS")
		owner_ids = _parse_int_list("BOT_OWNERS")
		activity_text = os.getenv("BOT_ACTIVITY", "Managing your server")
		sync_on_startup = os.getenv("SYNC_ON_STARTUP", "true").lower() in {"1", "true", "yes", "y"}
		database_path = os.getenv("DATABASE_PATH", "data/bot.db").strip() or "data/bot.db"

		return BotSettings(
			token=token,
			command_guild_ids=command_guild_ids,
			owner_ids=owner_ids,
			activity_text=activity_text,
			sync_on_startup=sync_on_startup,
			database_path=database_path,
		)