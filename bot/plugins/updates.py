from ..config import Config
from pyrogram import Client, filters
from ..translations import Messages as tr

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from ..utubebot import UtubeBot

def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '-->', callback_data = "update+2")]
        ]
    elif(pos==len(tr.UPDATE_MSG)-1):

        button = [
        [
            InlineKeyboardButton(text = 'Support Chat', url = Config.SUPPORT_CHAT_LINK),
            InlineKeyboardButton(text = 'Feature Request', url = "https://github.com/oVo-HxBots/Utubeitbot/issues/new")
            ],
            [InlineKeyboardButton(text = '<--', callback_data = f"update+{pos-1}")]
          
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '<--', callback_data = f"update+{pos-1}"),
                InlineKeyboardButton(text = '-->', callback_data = f"update+{pos+1}")
            ],
        ]
    return button

@UtubeBot.on_message(filters.private & filters.incoming & filters.command(['update', 'up']), group=2)
async def _update(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    await m.reply_text(
        text = tr.UPDATE_MSG[1],
        disable_web_page_preview=True,
        reply_markup = InlineKeyboardMarkup(map(1))
    )


update_callback_filter = filters.create(lambda _, __, query: query.data.startswith('update+'))

@UtubeBot.on_callback_query(update_callback_filter)
async def update_answer(c: UtubeBot, q: CallbackQuery):
    pos = int(q.data.split("+")[1])
    await q.answer()
    await q.edit_message_text(
        text = tr.UPDATE_MSG[pos],    reply_markup = InlineKeyboardMarkup(map(pos))
    )