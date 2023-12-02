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


def map_btns(pos):
    if pos == 1:
        button = [[InlineKeyboardButton(text="-->", callback_data="help+2")]]
    elif pos == len(tr.HELP_MSG) - 1:
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        url = auth.GetAuthUrl()
        button = [
            [InlineKeyboardButton(text="<--", callback_data=f"help+{pos-1}")],
            [InlineKeyboardButton(text="Login URL", url=url)],
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text="<--", callback_data=f"help+{pos-1}"),
                InlineKeyboardButton(text="-->", callback_data=f"help+{pos+1}"),
            ],
        ]
    return button


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("help")
)
async def _help(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    await m.reply_text(
        text=tr.HELP_MSG[1],
        reply_markup=InlineKeyboardMarkup(map_btns(1)),
    )


help_callback_filter = Filters.create(
    lambda _, __, query: query.data.startswith("help+")
)


@UtubeBot.on_callback_query(help_callback_filter)
async def help_answer(c: UtubeBot, q: CallbackQuery):
    pos = int(q.data.split("+")[1])
    await q.answer()
    await q.edit_message_text(
        text=tr.HELP_MSG[pos], reply_markup=InlineKeyboardMarkup(map_btns(pos))
    )


auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
url = auth.GetAuthUrl()

@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("login")
)
async def _login(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    await m.reply_text(
        text=tr.LOGIN_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Authentication URL", url=url)]]
     )
)

@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("plans")
)
async def _upgrade(c: UtubeBot, m: Message):
    await m.reply_chat_action("typing")
    msg=(
        f"👉 Plans For DS [Youtube Upload Bot](https://t.me/Utubeitbot):-\n\n"
        f"💗  Plans 💗\n\n"
        f"Plan 1:-\n"
             f"Plan Name:- BASIC\n"
             f"Video Limit:- 10 Videos Daily\n"
             f"Price:-\n"
                   f"INR:- 139₹\n"
             f"Validity:- 28 days\n\n"
        f"Plan 2:-\n"
             f"Plan Name:- UPGRADE\n"
             f"Video limit:- 20 Videos Daily\n"
             f"Price:-\n"
                   f"INR:- 249₹\n"
             f"Validity:- 28 days\n\n"
        f"Plan 3:-\n"
             f"Plan Name:- PREMIUM\n"
             f"Video limit:- 100 Videos Daily\n"
             f"Price:-\n"
                   f"INR:- 949₹\n"
             f"Validity:- 28 days\n\n"
        f"⚠️ Indian All payment methods accepted\n\n"
        f"⚠️ Payment through Crypto , Paypal , Binance , UPI , Paytm , Phonepe , wallet etc. Accepted.\n\n"
        f"⚠️ Services Are Non refundable.\n\n"
        f"👉 For More Details and for buying the plan , please contact :- [Kirodewal](https://t.me/Kirodewal)"
    )
    await m.reply_text(
        text=msg,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="More Details", url="https://t.me/+97tA4_TrzyowMjk1")]]
     )
)
