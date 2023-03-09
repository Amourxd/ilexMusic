import re
import asyncio

from ilex.config import ASSISTANT_NAME, BOT_USERNAME
from ilex.inline import stream_markup, audio_markup
from Process.design.chatname import CHAT_TITLE
from cache.filters import command, other_filters
from cache.queues import QUEUE, add_to_queue
from cache.main import call_py, ilex as user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch
from Process.design.thumbnail import play_thumb, queue_thumb

IMAGE_THUMBNAIL = "https://te.legra.ph/file/a0004a5905754096ebbd2.jpg"

def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀʀɴᴀᴠxᴅ__ ᴀᴅᴍɪɴ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪssɪᴏɴs**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n» ❌ __ɪɴᴠɪᴛᴇ ᴜsᴇʀs__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʏᴘᴇ /ʀᴇʟᴏᴀᴅ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:**"
        + "\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **ᴜsᴇʀʙᴏᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀsᴏɴ**: `{e}`"
            )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __ᴏɴʟʏ 𝟽𝟸𝟶, 𝟺𝟾𝟶, 𝟹𝟼𝟶 ᴀʟʟᴏᴡᴇᴅ__ \n💡 **ɴᴏᴡ sᴛʀᴇᴀᴍɪɴɢ ᴠɪᴅᴇᴏ ɪɴ 𝟽𝟸𝟶ᴘ**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = audio_markup(user_id)
                await m.reply_photo(
                    photo=thumbnail,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗠𝘂𝘀𝗶𝗰 𝗫𝗗 ❱ 𝗦𝗼𝗻𝗴 ❤️ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 💫🤟**\n🧸 **𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗯𝘆:** {requester}",
                )
            else:
                if Q == 720:
                    ilex = HighQualityVideo()
                elif Q == 480:
                    ilex = MediumQualityVideo()
                elif Q == 360:
                    ilex = LowQualityVideo()
                await loser.edit("🙊")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        ilex,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = audio_markup(user_id)
                await m.reply_photo(
                    photo=thumbnail,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗠𝘂𝘀𝗶𝗰 𝗫𝗗 ❱ 𝗡𝗼𝘄 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟**\n🧸 **Request by:** {requester}",
                )
        else:
            if len(m.command) < 2:
                await m.reply_text(
                    text="💬**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**", 
             ) 
            else:
                loser = await c.send_message(chat_id, f"**💥 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 ...**"
                      )
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 360
                ilex = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **🥀𝗦𝗼𝗻𝗴 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱 🦜 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗣𝗿𝗼𝗯𝗹𝗲𝗺**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    videoid = search[4]
                    playimg = await play_thumb(videoid)
                    queueimg = await queue_thumb(videoid)
                    dlurl = f"https://www.youtubepp.com/watch?v={videoid}"
                    shub, ytlink = await ytdl(url)
                    if shub == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id, videoid)
                            await m.reply_photo(
                                photo=queueimg,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"**❰ 𝗔𝗿𝗻𝗮𝘃 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗡𝗼𝘄 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟\n**𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗯𝘆:** {requester}",
                            )
                        else:
                            try:
                                await loser.edit(
                            f"**🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...**"
                        )
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        ilex,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id, dlurl)
                                await m.reply_photo(
                                    photo=playimg,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"**❰ 𝗔𝗿𝗻𝗮𝘃 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ Now 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟**\n**𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗯𝘆:** {requester}",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply_text(
                     text="💫**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**", 
         ) 
        else:
            loser = await c.send_message(chat_id, f"**💥 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            ilex = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **🥀𝗦𝗼𝗻𝗴 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱 🦜 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗣𝗿𝗼𝗯𝗹𝗲𝗺.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                videoid = search[4]
                playimg = await play_thumb(videoid)
                queueimg = await queue_thumb(videoid)
                dlurl = f"https://www.youtubepp.com/watch?v={videoid}"               
                shub, ytlink = await ytdl(url)
                if shub == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id, dlurl)
                        await m.reply_photo(
                            photo=queueimg,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"**❰ 𝗔𝗿𝗻𝗮𝘃 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗦𝗼𝗻𝗴 ❤️ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 💫🤟**\n🧸 **Request by:** {requester}",
                        )
                    else:
                        try:
                            await loser.edit(
                            f"**🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    ilex,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id, dlurl)
                            await m.reply_photo(
                                photo=playimg,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"**❰ 𝗔𝗿𝗻𝗮𝘃 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ Now 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟**\n🧸 **Request by:** {requester}",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
