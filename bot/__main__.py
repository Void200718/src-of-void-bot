import logging
import os

from dotenv import load_dotenv

# Load environment variables from a local .env file if present
load_dotenv()

from .bot import AdvancedBot
from .config import BotSettings


def configure_logging() -> None:
	level_name = os.getenv("LOG_LEVEL", "INFO").upper()
	level = getattr(logging, level_name, logging.INFO)

	logging.getLogger("discord").setLevel(logging.WARNING)
	logging.getLogger("discord.voice").setLevel(logging.WARNING)

	handler = logging.StreamHandler()
	try:
		import colorlog  # type: ignore

		formatter = colorlog.ColoredFormatter(
			"%(log_color)s%(levelname)-8s%(reset)s %(white)s%(name)s%(reset)s | %(message)s"
		)
		handler.setFormatter(formatter)
	except Exception:
		formatter = logging.Formatter("%(levelname)-8s %(name)s | %(message)s")
		handler.setFormatter(formatter)

	root = logging.getLogger()
	root.setLevel(level)
	root.handlers.clear()
	root.addHandler(handler)


def main() -> None:
	configure_logging()
	settings = BotSettings.from_env()
	bot = AdvancedBot(settings)
	bot.run(settings.token, reconnect=True)


if __name__ == "__main__":
	main()