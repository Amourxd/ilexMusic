from cache.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ilex.config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from cache.filters import other_filters2
from time import time
from datetime import datetime
from cache.decorators import authorized_users_only

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 ** 2 * 24),
    ("hour", 60 ** 2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)

start_keyboard = InlineKeyboardMarkup( [[
      InlineKeyboardButton("🍓 sᴜᴘᴘᴏʀᴛ 🍓", url=f"https://t.me/ilexupdates/85"), 
      ],[
      InlineKeyboardButton("🧁 ɢʀᴏᴜᴘ 🧁", url=f"t.me/{GROUP_SUPPORT}"), 
      InlineKeyboardButton("💌 ᴜᴘᴅᴀᴛᴇs 💌", url=f"t.me/{UPDATES_CHANNEL}"), 
      ],[
      InlineKeyboardButton("✚ 𝗔𝗗𝗗 𝗠𝗘 𝗕𝗔𝗕𝗬 ✚", url=f"t.me/{BOT_USERNAME}?startgroup=True")
      ]]
      ) 


@Client.on_message(filters.command("start") & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        text=f"**𝐇𝐞𝐥𝐥𝐨 {message.from_user.mention()}\n\n🛸𝐓𝐡𝐢𝐬 {BOT_NAME}ɪs 𝐀𝐝𝐯𝐚𝐧𝐜𝐞 🥀𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐌ᴜsɪᴄ 🎶 𝐁𝐨𝐭 \n𝐑𝐮𝐧 𝐎𝐧 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 🥀 ʜᴇʀᴏᴋᴜ 💫sᴇʀᴠᴇʀ ♻️ \nᴛʜɪs ɪs ᴀʀɴᴀᴠ ダ ᴍᴜsɪᴄ​ 🥀
 ᴀ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ᴀɴᴅ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs.

ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ \n⭐𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐝 𝐁𝐲 [ɪʟᴇxᴍᴜsɪᴄ](https://t.me/arnav_ilexsupport)💖..**", 
        disable_web_page_preview=True,
        reply_markup=start_keyboard, 
    ) 
        
