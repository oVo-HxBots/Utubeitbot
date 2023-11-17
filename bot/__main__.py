import logging
import os
from .utubebot import UtubeBot
from .config import Config


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)
    logging.getLogger("pyrogram").setLevel(
        logging.INFO if Config.DEBUG else logging.WARNING
    )
    if not os.path.isdir(Config.DOWNLOAD_DIRECTORY):
        os.makedirs(Config.DOWNLOAD_DIRECTORY)

    UtubeBot().run()
