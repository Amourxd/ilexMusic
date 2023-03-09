from pyrogram import Client
from ilex.config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME
from pytgcalls import PyTgCalls, idle

bot = Client(
    "ilex",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="ilex.handler"),
    )

ilex = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    session_name=SESSION_NAME,
    
    )

user = PyTgCalls(ilex,
    cache_duration=100,
    overload_quiet_mode=True,)

call_py = PyTgCalls(ilex, overload_quiet_mode=True)

with Client("ilex", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
    me_bot = app.get_me()
with ilex as app:
    me_ilex = app.get_me()
