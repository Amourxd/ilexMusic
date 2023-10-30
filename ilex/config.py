import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME")
ALIVE_NAME = getenv("ALIVE_NAME")
ASSISTANT_USERNAME = getenv("ASSISTANT_USERNAME")
BOT_USERNAME = getenv("BOT_USERNAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "link_copied")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "ilexupdates")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5157056683").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://te.legra.ph/file/a0004a5905754096ebbd2.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/singhji143/AmoxYMusicxd")
IMG = getenv("IMG", "https://te.legra.ph/file/a0004a5905754096ebbd2.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://te.legra.ph/file/a0004a5905754096ebbd2.jpg")
