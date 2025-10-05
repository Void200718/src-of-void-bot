import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv


@dataclass
class Config:
    discord_token: str
    owner_ids: List[int]
    guild_id: Optional[int]


def _parse_owner_ids(raw_value: Optional[str]) -> List[int]:
    if not raw_value:
        return []
    owner_ids: List[int] = []
    for part in raw_value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            owner_ids.append(int(part))
        except ValueError:
            # Ignore invalid owner IDs silently to avoid startup failures
            continue
    return owner_ids


def get_config() -> Config:
    load_dotenv(override=False)

    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "DISCORD_TOKEN is not set. Create a .env with DISCORD_TOKEN=your_token"
        )

    owner_ids_raw = os.getenv("BOT_OWNER_IDS")
    owner_ids = _parse_owner_ids(owner_ids_raw)

    guild_id_raw = os.getenv("GUILD_ID", "").strip()
    guild_id: Optional[int] = None
    if guild_id_raw:
        try:
            guild_id = int(guild_id_raw)
        except ValueError:
            guild_id = None

    return Config(discord_token=token, owner_ids=owner_ids, guild_id=guild_id)

