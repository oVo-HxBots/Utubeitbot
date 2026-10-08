import asyncio
import datetime
import logging
import os
import random
import string
import time
from typing import Tuple, Union

from pyrogram import StopTransmission
from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..config import Config
from ..helpers.downloader import Downloader
from ..helpers.uploader import Uploader
from ..translations import Messages as tr
from ..utubebot import UtubeBot

log = logging.getLogger(__name__)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("upload")
    & Filters.user(Config.AUTH_USERS)
)
async def _upload(c: UtubeBot, m: Message):
    user_id = m.from_user.id
    cred_file = Config.credential_file(user_id)

    if not cred_file.is_file():
        await m.reply_text(
            "❌ YouTube is not authenticated for this Telegram account. "
            "Use /login first.",
            True,
        )
        return

    if not m.reply_to_message:
        await m.reply_text(tr.NOT_A_REPLY_MSG, True)
        return

    message = m.reply_to_message

    if not message.media:
        await m.reply_text(tr.NOT_A_MEDIA_MSG, True)
        return

    if not valid_media(message):
        await m.reply_text(tr.NOT_A_VALID_MEDIA_MSG, True)
        return

    if c.counter >= 6:
        await m.reply_text(tr.DAILY_QOUTA_REACHED, True)
        return

    snt = await m.reply_text(tr.PROCESSING, True)
    c.counter += 1

    download_id = get_download_id(c.download_controller)
    c.download_controller[download_id] = True

    download = Downloader(m)

    try:
        status, file = await download.start(
            progress,
            snt,
            c,
            download_id,
        )
        log.debug("%s %s", status, file)

        c.download_controller.pop(download_id, None)

        if not status:
            c.counter = max(0, c.counter - 1)
            await snt.edit_text(text=file, parse_mode="markdown")
            return

        try:
            await snt.edit_text(
                "Downloaded to local, Now starting to upload to youtube..."
            )
        except Exception as exc:
            log.warning(exc, exc_info=True)

        title = " ".join(m.command[1:]) if len(m.command) > 1 else ""
        upload = Uploader(file, title, user_id)
        status, link = await upload.start(progress, snt)
        log.debug("%s %s", status, link)

        if not status:
            c.counter = max(0, c.counter - 1)

        await snt.edit_text(text=link, parse_mode="markdown")
    finally:
        c.download_controller.pop(download_id, None)
        if "file" in locals() and file and os.path.isfile(file):
            try:
                os.remove(file)
            except OSError:
                log.warning("Could not remove temporary file %s", file)


def get_download_id(storage: dict) -> str:
    while True:
        download_id = "".join(
            random.choice(string.ascii_letters) for _ in range(3)
        )
        if download_id not in storage:
            return download_id


def valid_media(media: Message) -> bool:
    if media.video:
        return True
    if media.video_note:
        return True
    if media.animation:
        return True
    if media.document and media.document.mime_type:
        return media.document.mime_type.startswith("video/")
    return False


def human_bytes(
    num: Union[int, float],
    split: bool = False,
) -> Union[str, Tuple[float, str]]:
    base = 1024.0
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    for unit in suffixes:
        if abs(num) < base:
            if split:
                return round(num, 2), unit
            return f"{round(num, 2)} {unit}"
        num /= base

    if split:
        return round(num, 2), suffixes[-1]
    return f"{round(num, 2)} {suffixes[-1]}"


async def progress(
    cur: Union[int, float],
    tot: Union[int, float],
    start_time: float,
    status: str,
    snt: Message,
    c: UtubeBot,
    download_id: str,
):
    if not c.download_controller.get(download_id):
        raise StopTransmission

    try:
        elapsed_seconds = max(1, int(time.time() - start_time))

        if int(time.time()) % 5 == 0 or cur >= tot:
            await asyncio.sleep(1)

            speed_bps = cur / elapsed_seconds
            speed, unit = human_bytes(speed_bps, True)
            curr = human_bytes(cur)
            total = human_bytes(tot)

            remaining = max(0, tot - cur)
            eta_seconds = int(remaining / max(speed_bps, 1))
            eta = datetime.timedelta(seconds=eta_seconds)
            elapsed = datetime.timedelta(seconds=elapsed_seconds)

            percent = round((cur * 100) / tot, 2) if tot else 0

            text = (
                f"{status}\n\n"
                f"{percent}% done.\n"
                f"{curr} of {total}\n"
                f"Speed: {speed} {unit}/s\n"
                f"ETA: {eta}\n"
                f"Elapsed: {elapsed}"
            )

            await snt.edit_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "Cancel!🚫",
                            callback_data=f"cncl+{download_id}",
                        )
                    ]]
                ),
            )
    except StopTransmission:
        raise
    except Exception as exc:
        log.info(exc)
