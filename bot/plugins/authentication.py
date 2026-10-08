import logging

from pyrogram import filters as Filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..config import Config
from ..utubebot import UtubeBot
from ..youtube import GoogleAuth

log = logging.getLogger(__name__)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("login")
    & Filters.user(Config.AUTH_USERS)
)
async def _login(c: UtubeBot, m: Message) -> None:
    await m.reply_chat_action(ChatAction.TYPING)

    try:
        auth = GoogleAuth(
            Config.CLIENT_ID,
            Config.CLIENT_SECRET,
            Config.OAUTH_REDIRECT_URI,
        )
        url = auth.GetAuthUrl(m.from_user.id)

        await m.reply_text(
            "🔐 <b>Connect your YouTube channel</b>\n\n"
            "Open the button below and sign in to the Google account that owns "
            "your YouTube channel.\n\n"
            "After Google finishes authorization, it will redirect back "
            "automatically and the bot will confirm the connection.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 Authorize YouTube", url=url)]]
            ),
        )
    except Exception as exc:
        log.error("Unable to start Google OAuth", exc_info=True)
        await m.reply_text(f"❌ Error starting YouTube authorization: {exc}", True)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("authorise")
    & Filters.user(Config.AUTH_USERS)
)
async def _auth(c: UtubeBot, m: Message) -> None:
    await m.reply_text(
        "ℹ️ Authorization codes are no longer copied through Telegram. "
        "Use /login and complete the Google authorization in your browser.",
        True,
    )


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("save_auth_data")
    & Filters.user(Config.AUTH_USERS)
)
async def _save_auth_data(c: UtubeBot, m: Message) -> None:
    await m.reply_text(
        "For security, OAuth refresh tokens are no longer sent through Telegram. "
        "Use /login to connect or reconnect your YouTube account.",
        True,
    )


async def handle_oauth_callback(bot: UtubeBot, code: str, state: str) -> None:
    user_id, credentials = GoogleAuth.complete_callback(code, state)

    auth = GoogleAuth(
        Config.CLIENT_ID,
        Config.CLIENT_SECRET,
        Config.OAUTH_REDIRECT_URI,
    )
    auth.credentials = credentials

    cred_file = Config.credential_file(user_id)
    auth.SaveCredentialsFile(str(cred_file))

    try:
        await bot.send_message(
            user_id,
            "✅ <b>YouTube authorization successful!</b>\n\n"
            "Your YouTube account is now connected. You can now reply to a "
            "Telegram video and use /upload.",
        )
    except Exception:
        log.warning(
            "Could not notify Telegram user %s",
            user_id,
            exc_info=True,
        )

    log.info(
        "YouTube OAuth authorization completed for Telegram user %s",
        user_id,
    )
