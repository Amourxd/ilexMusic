from pyrogram import Client, errors
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from youtubesearchpython import VideosSearch


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

@Client.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answerss = (
      [
        InlineQueryResultArticle(
            title="Pause Stream",
            description=f"Pause the current playout on group call.",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/pause"),
        ),
        InlineQueryResultArticle(
            title="Resume Stream",
            description=f"Resume the ongoing playout on group call.",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/resume"),
        ),
        InlineQueryResultArticle(
            title="Mute Stream",
            description=f"Mute the ongoing playout on group call.",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/mute"),
        ),
        InlineQueryResultArticle(
            title="Unmute Stream",
            description=f"Unmute the ongoing playout on group call.",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/unmute"),
        ),
        InlineQueryResultArticle(
            title="Skip Stream",
            description=f"Skip to next track. | For Specific track number: /skip [number] ",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/skip"),
        ),
        InlineQueryResultArticle(
            title="End Stream",
            description="Stop the ongoing playout on group call.",
            thumb_url="https://te.legra.ph/file/a0004a5905754096ebbd2.jpg",
            input_message_content=InputTextMessageContent("/stop"),
        ),
      ]
    )
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answerss,
            switch_pm_text="Type The Name Of The Song/Video YouTube...",
            switch_pm_parameter="help",
            cache_time=0,
        )
