import io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re
import youtube_dl
import youtube_dl
import aiofiles
import aiohttp
from ilex.converter import convert
import ffmpeg
import requests
from cache.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from ilex.config import ASSISTANT_NAME, BOT_USERNAME
from cache.filters import command, other_filters
from cache.queues import QUEUE, add_to_queue
from cache.main import call_py, ilex as user
from cache.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
from Process.design.thumbnail import play_thumb, queue_thumb 
from ilex.inline import stream_markup, audio_markup

def ytsearch(query):
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


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []

    
@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    buttons = audio_markup(user_id)
    if m.sender_chat:
        return await m.reply_text("𝗕𝗮𝗯𝘆 𝗲𝗸 𝘁𝗵𝗼𝗿𝗶 𝘀𝗮 𝗸𝗲𝘀𝗶 𝗱𝗲 𝗱𝗼 𝗻𝗮 𝗽𝗹𝗲𝘀𝗲 😝.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"Error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"**💡 ᴛᴏ ᴜsᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ   ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪssɪᴏɴs**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴅᴀᴛᴀ ɪs **ᴜᴘᴅᴀᴛᴇᴅ** ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀғᴛᴇʀ ʏᴏᴜ **ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "**ᴍɪssɪɴɢ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ:" + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "**ᴍɪssɪɴɢ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ:" + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__**"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("**ᴍɪssɪɴɢ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ:" + "\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__**")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **ɪs ʙᴀɴɴᴇᴅ ɪɴ ɢʀᴏᴜᴘ** {m.chat.title}\n\n» **ᴜɴʙᴀɴ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ғɪʀsᴛ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **ᴜsᴇʀʙᴏᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀsᴏɴ**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
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
        if replied.audio or replied.voice:
            suhu = await replied.reply("💘")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else: 
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
                    caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗦𝗼𝗻𝗴 ❤️ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 💫🤟\n\n**𝗥𝗲𝗾𝘂𝘀𝘁𝗲𝗱 𝗯𝘆:{m.from_user.mention()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"https://te.legra.ph/file/4d71c4bd3802a77b9c597.jpg",
                    caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗡𝗼𝘄 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟\n\n👤𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:{requester}**",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_text(
                    text="**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**"),
        
        else:
            suhu = await m.reply_text(
        f"**Downloading**\n\n100% ▓▓▓▓▓▓▓▓▓▓▓▓ 00%"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("**🥀𝗦𝗼𝗻𝗴 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱 ✌ 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗣𝗿𝗼𝗯𝗹𝗲𝗺**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                videoid = search[4]
                dlurl = f"https://www.youtubepp.com/watch?v={videoid}"
                info = f"https://t.me/ArnavXMusicBot?start=info_{videoid}"
                keyboard = stream_markup(user_id, dlurl)
                playimg = await play_thumb(videoid)
                queueimg = await queue_thumb(videoid)
                await suhu.edit(
                            f"**Downloader**\n\n**Title**: {title[:22]}\n\n100% ▓▓▓▓▓▓▓▓▓▓▓▓0%\n\n**Time Taken**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=queueimg,
                            caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗦𝗼𝗻𝗴 ❤️ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 💫🤟**:{requester}",
                            reply_markup=InlineKeyboardMarkup(keyboard),
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"**Downloader**\n\n**Title**: {title[:22]}\n\n0% ████████████100%\n\n**Time Taken**: 00:00 Seconds\n\n**Converting Audio[FFmpeg Process]**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=playimg,
                                caption=f"**❰ 𝗜𝗹𝗲𝘅 𝗣𝗹𝗮𝘆𝗲𝗿 ❱ 𝗡𝗼𝘄 😄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 📀 𝗔𝘁 🤟\n\n👤𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗕𝘆:{requester}**",
                                reply_markup=InlineKeyboardMarkup(keyboard),
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 error: `{ep}`")
