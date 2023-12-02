import asyncio
import io
import math
import os
import shutil
import sys
import time
import traceback
import logging
import datetime
import psutil

from ..config import Config
from ..utubebot import UtubeBot
from ..translations import Messages as tr
from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from ..helpers.database import db

log = logging.getLogger(__name__)


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("status")
    & Filters.user(Config.BOT_OWNER)
)
async def stats_message_fn(c: UtubeBot, m: Message):
    restart_time = Config.BOT_START_DATETIME
    hr, mi, se = map(time_format, up_time(time.time() - Config.BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(psutil.net_io_counters().bytes_sent)
    recv = humanbytes(psutil.net_io_counters().bytes_recv)
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    start_t = time.time()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    
    msg = (
        f"<b>Bot Current Status</b>\n\n"
        f"<b>Restarted on {restart_time}</b>\n"
        f"<b>Bot Uptime</b>: {hr}:{mi}:{se}\n\n"
        f"<b>Total disk space:</b> {total}\n"
        f"<b>Used :</b> {used}\n"
        f"<b>Free :</b> {free}\n\n"
        f"<b>RAM Usage:</b> {ram}%\n"
        f"<b>CPU Usage:</b> {cpu}%\n\n"
        f"<b>Downloaded Data:</b> {recv} 🔻\n"
        f"<b>Uploaded Data:</b> {sent} 🔺\n\n"
    )
    await m.reply_text(
        text=msg,
        quote=True
    )

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"

def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


def time_format(val):
    val = str(val)
    if len(val) == 1:
        val = f"0{val}"
    else:
        pass
    return val