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
      InlineKeyboardButton("šš¼šŗšŗš®š»š±š šø", url=f"https://t.me/ilexupdates"), 
      ],[
      InlineKeyboardButton("šššæš¼šš½", url=f"t.me/{GROUP_SUPPORT}"), 
      InlineKeyboardButton("šØš½š±š®šš²š š®š³", url=f"t.me/{UPDATES_CHANNEL}"), 
      ],[
      InlineKeyboardButton("ā ššš š š šššš¬ ā", url=f"t.me/{BOT_USERNAME}?startgroup=True")
      ]]
      ) 


@Client.on_message(filters.command("start") & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        text=f"**ššš„š„šØ {message.from_user.mention()}\n\nš„šš”š¢š¬ {BOT_NAME}šš¬ šššÆšš§šš š„ššš„šš š«šš¦ šš®š¬š¢š š¶ ššØš­ \nšš®š§ šš§ šš«š¢šÆšš­š š„ šš©š¬ šššš«šÆšš« š \nšššš„ ā¤ļø šš¢š š” šš®šš„š¢š­š² šš®š¬š¢š š§ šš§ šš šš¤ \nā­šššÆšš„šØš©šš šš² [šš„šš±ššØš«š](https://t.me/link_copied)š..**", 
        disable_web_page_preview=True,
        reply_markup=start_keyboard, 
    ) 
        
