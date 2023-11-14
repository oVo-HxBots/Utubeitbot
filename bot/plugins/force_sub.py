from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from ..config import Config
from helpers.database import db

async def not_subscribed(c: UtubeBot, m: Message):
    await db.add_user(user.id)
    if not Config.FORCE_SUB:
        return False
    try:             
        user = await client.get_chat_member(Config.FORCE_SUB, m.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True 
        else:
            return False                
    except UserNotParticipant:
        pass
    return True


@UtubeBot.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(c: UtubeBot, m: Message):
    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=f"https://t.me/{Config.FORCE_SUB}") ]]
    text = "**Sᴏʀʀy Dᴜᴅᴇ Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴄᴏɴᴛɪɴᴜᴇ**"
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, m.from_user.id)    
        if user.status == enums.ChatMemberStatus.BANNED:                                   
            return await client.send_message(m.from_user.id, text="Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")  
    except UserNotParticipant:                       
        return await m.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    return await m.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
          
