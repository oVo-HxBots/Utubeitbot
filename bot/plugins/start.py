from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from ..translations import Messages as tr
from ..config import Config
from ..utubebot import UtubeBot


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("start")
)
async def _start(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    await m.reply_text(
        text=tr.START_MSG.format(m.from_user.first_name),
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
                  [
                      InlineKeyboardButton("How To Use Me🙄", callback_data="/help")
                  ],
                  [
                      InlineKeyboardButton("Project Channel!", url="https://t.me/hxbots"),
                      InlineKeyboardButton("Support Group", url="https://t.me/HxSupport")
                  ],
                  [  
                      InlineKeyboardButton("Upgrade😀", callback_data="/help")
                  ]]
        ),
    )
