import os
import sys
import time
import asyncio 
import logging 
import datetime
from ..config import Config
from ..helpers.database import db
from pyrogram.types import Message
from pyrogram import Client
from pyrogram import filters as Filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from ..utubebot import UtubeBot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("users")
    & Filters.user(Config.BOT_OWNER)
)
async def get_stats(c: UtubeBot, m: Message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    start_t = time.time()
    st = await m.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")

@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("broadcast")
    & Filters.user(Config.BOT_OWNER)
    & Filters.reply
)
async def broadcast_handler(c: UtubeBot, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("broadcast started !") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Broadcast in progress:\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Broadcast Completed:\nCompleted in `{completed_in}`.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : blocked the bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : user id invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
 