import logging

from .config import Config
from .utubebot import UtubeBot


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG if Config.DEBUG else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger("pyrogram").setLevel(
        logging.DEBUG if Config.DEBUG else logging.WARNING
    )

    app = UtubeBot()
    app.run()
