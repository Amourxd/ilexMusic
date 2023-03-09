import asyncio
from pytgcalls import idle
from cache.main import call_py, bot

async def start_bot():
    print("[INFO]: sᴛᴀʀᴛɪɴɢ ɪʟᴇx ʙᴏᴛ ᴄʟɪᴇɴᴛ")
    await bot.start()
    print("[INFO]: sᴛᴀʀᴛɪɴɢ ɪʟᴇx ᴄʟɪᴇɴᴛ")
    await call_py.start()
    await idle()
    print("[INFO]: sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ & ᴜsᴇʀʙᴏᴛ")
    await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
