from pyrogram import filters as Filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from ..youtube import GoogleAuth
from ..config import Config
from ..translations import Messages as tr
from ..utubebot import UtubeBot

auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
url = auth.GetAuthUrl()

@UtubeBot.on_message
    Filters.private
    & Filters.incoming
    & Filters.command("login")
)
async def _login(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    await m.reply_text(
        text=tr.LOGIN_MSG[1],
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Authentication URL", url=url)]]
    )

