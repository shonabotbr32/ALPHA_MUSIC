import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")


# Vars For API End Pont.
YTPROXY_URL = getenv("YTPROXY_URL", 'https://tgapi.xbitcode.com') ## xBit Music Endpoint.
YT_API_KEY = getenv("YT_API_KEY" , 'xbit_-G9GXbjRf8mA9_mz6-jnQcUoFpcEMsrM') ## Your API key like: xbit_10000000xx0233 Get from  https://t.me/tgmusic_apibot

MONGO_DB_URI = getenv("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 10000))

LOGGER_ID = int(getenv("LOGGER_ID", None))
OWNER_ID = int(getenv("OWNER_ID", 7403621976))

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/shonabotbr32/ALPHA_MUSIC")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/shona_bots")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/SHONA_support")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://silabotov.ru/img/8f2262f1-34dc-42bb-b1df-91f751cbf990.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg")
PLAYLIST_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
STATS_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
TELEGRAM_AUDIO_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
TELEGRAM_VIDEO_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
STREAM_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
SOUNCLOUD_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
YOUTUBE_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://silabotov.ru/img/df1773b9-5142-4381-9396-f4dcb84c1a38.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://silabotov.ru/img/8f2262f1-34dc-42bb-b1df-91f751cbf990.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://")

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://")
