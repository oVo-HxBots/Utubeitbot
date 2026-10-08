import logging
from urllib.parse import parse_qs, urlparse

from pyrogram import filters as Filters
from pyrogram.types import Message

from ..youtube import GoogleAuth
from ..config import Config
from ..translations import Messages as tr
from ..utubebot import UtubeBot


log = logging.getLogger(__name__)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("authorise")
    & Filters.user(Config.AUTH_USERS)
)
async def _auth(c: UtubeBot, m: Message) -> None:
    if len(m.command) == 1:
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        url = auth.GetAuthUrl()
        await m.reply_text(
            f"Open this URL and allow access:\n{url}\n\nAfter Google redirects, copy the full URL from the browser and send it back in this format:\n/authorise <code-or-full-url>",
            True,
            disable_web_page_preview=True,
        )
        return

    code = m.command[1]
    if "http" in code.lower():
        parsed = urlparse(code)
        params = parse_qs(parsed.query)
        code = params.get("code", [None])[0]

    if not code:
        await m.reply_text("❌ No valid authorization code found in the text you sent.", True)
        return

    try:
        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        auth.Auth(code)
        auth.SaveCredentialsFile(Config.CRED_FILE)

        msg = await m.reply_text(tr.AUTH_SUCCESS_MSG, True)

        with open(Config.CRED_FILE, "r", encoding="utf-8") as f:
            cred_data = f.read()

        log.debug(f"Authentication success, auth data saved to {Config.CRED_FILE}")

        msg2 = await msg.reply_text(cred_data, parse_mode=None)
        await msg2.reply_text(
            "This is your authorization data! Save it for later use. Reply /save_auth_data to re-authorize later.",
            True,
        )

    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(tr.AUTH_FAILED_MSG.format(e), True)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("save_auth_data")
    & Filters.reply
    & Filters.user(Config.AUTH_USERS)
)
async def _save_auth_data(c: UtubeBot, m: Message) -> None:
    auth_data = m.reply_to_message.text
    try:
        with open(Config.CRED_FILE, "w", encoding="utf-8") as f:
            f.write(auth_data)

        auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
        auth.LoadCredentialsFile(Config.CRED_FILE)
        auth.authorize()

        await m.reply_text(tr.AUTH_DATA_SAVE_SUCCESS, True)
        log.debug(f"Authentication success, auth data saved to {Config.CRED_FILE}")
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(tr.AUTH_FAILED_MSG.format(e), True)
