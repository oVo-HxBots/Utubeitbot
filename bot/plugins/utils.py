import os
import shutil
from os import execl
from time import sleep
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from ..config import Config
from ..utubebot import UtubeBot
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(Config.BOT_OWNER), group=2)
async def _restart(c: UtubeBot, m: Message):
  shutil.rmtree(Config.DOWNLOAD_DIRECTORY)
  LOGGER.info('Deleted Config.DOWNLOAD_DIRECTORY successfully.')
  await m.reply_text(
      text='**♻️Bot Restarted Successfully !**',
      quote=True
  )
  LOGGER.info(f'{m.from_user.id}: Restarting...')
  execl(executable, executable, "-m", "bot")
