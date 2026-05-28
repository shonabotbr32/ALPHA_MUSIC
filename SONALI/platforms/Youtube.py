# SECURE YOUTUBE API FILE BY HARSH CHAURASIYA 
# Fully patched against command injection
# No shell=True
# No subprocess_shell
# Safe URL validation
# Exploit protection added

import asyncio
import glob
import json
import os
import random
import re
from typing import Union
from urllib.parse import urlparse

import requests
import yt_dlp

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from py_yt import VideosSearch

from SONALI import LOGGER
from SONALI.utils.database import is_on_off
from SONALI.utils.formatters import time_to_seconds

from config import (
    YT_API_KEY,
    YTPROXY_URL as YTPROXY,
)

logger = LOGGER(__name__)


# -------------------- COOKIE -------------------- #


def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"

        txt_files = glob.glob(
            os.path.join(folder_path, "*.txt")
        )

        if not txt_files:
            return None

        selected = random.choice(txt_files)

        return f"cookies/{os.path.basename(selected)}"

    except Exception:
        return None


# -------------------- URL VALIDATION -------------------- #


def validate_youtube_url(url: str) -> bool:
    try:
        parsed = urlparse(url)

        allowed_domains = [
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "music.youtube.com",
        ]

        if parsed.netloc not in allowed_domains:
            return False

        dangerous_patterns = [
            ";",
            "|",
            "&;",
            "&&",
            "||",
            "`",
            "$(",
            "${",
            ">",
            "<",
            "\n",
            "\r",
        ]

        for bad in dangerous_patterns:
            if bad in url:
                return False

        return True

    except Exception:
        return False


# -------------------- FILE SIZE -------------------- #


async def check_file_size(link):

    if not validate_youtube_url(link):
        return None

    try:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies",
            cookie_txt_file() or "",
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            return None

        data = json.loads(stdout.decode())

        total_size = 0

        for fmt in data.get("formats", []):

            if "filesize" in fmt:
                total_size += fmt["filesize"]

        return total_size

    except Exception:
        return None


# -------------------- SESSION -------------------- #


def create_session():

    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=0.1,
    )

    session.mount(
        "http://",
        HTTPAdapter(max_retries=retries),
    )

    session.mount(
        "https://",
        HTTPAdapter(max_retries=retries),
    )

    return session


# -------------------- MAIN CLASS -------------------- #


class YouTubeAPI:

    def __init__(self):

        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

        self.dl_stats = {
            "total_requests": 0,
            "downloads": 0,
            "existing_files": 0,
        }

    # -------------------- EXISTS -------------------- #

    async def exists(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        return bool(re.search(self.regex, link))

    # -------------------- URL -------------------- #

    async def url(
        self,
        message_1: Message,
    ) -> Union[str, None]:

        messages = [message_1]

        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        text = ""
        offset = None
        length = None

        for message in messages:

            if offset:
                break

            if message.entities:

                for entity in message.entities:

                    if entity.type == MessageEntityType.URL:

                        text = message.text or message.caption

                        offset = entity.offset
                        length = entity.length

                        break

            elif message.caption_entities:

                for entity in message.caption_entities:

                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        if offset is None:
            return None

        return text[offset: offset + length]

    # -------------------- DETAILS -------------------- #

    async def details(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            raise ValueError("Unsafe URL blocked")

        results = VideosSearch(
            link,
            limit=1,
        )

        for result in (await results.next())["result"]:

            title = result["title"]

            duration_min = result["duration"]

            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

            vidid = result["id"]

            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(
                    time_to_seconds(duration_min)
                )

        return (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        )

    # -------------------- TITLE -------------------- #

    async def title(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            return None

        results = VideosSearch(
            link,
            limit=1,
        )

        for result in (await results.next())["result"]:
            return result["title"]

    # -------------------- DURATION -------------------- #

    async def duration(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            return None

        results = VideosSearch(
            link,
            limit=1,
        )

        for result in (await results.next())["result"]:
            return result["duration"]

    # -------------------- THUMBNAIL -------------------- #

    async def thumbnail(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            return None

        results = VideosSearch(
            link,
            limit=1,
        )

        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"]

    # -------------------- VIDEO STREAM -------------------- #

    async def video(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            return 0, "Unsafe URL blocked"

        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies",
            cookie_txt_file() or "",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        if stdout:
            return 1, stdout.decode().split("\n")[0]

        return 0, stderr.decode()

    # -------------------- PLAYLIST -------------------- #

    async def playlist(
        self,
        link,
        limit,
        user_id,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.listbase + link

        if not validate_youtube_url(link):
            logger.error("Blocked malicious playlist URL")
            return []

        try:

            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "-i",
                "--get-id",
                "--flat-playlist",
                "--cookies",
                cookie_txt_file() or "",
                "--playlist-end",
                str(limit),
                "--skip-download",
                link,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()

            if stderr:
                err = stderr.decode().lower()

                if "unavailable videos are hidden" not in err:
                    logger.error(err)

            result = stdout.decode().split("\n")

            result = [
                x.strip()
                for x in result
                if x.strip()
            ]

            return result

        except Exception as e:

            logger.error(
                f"Playlist Error: {e}"
            )

            return []

    # -------------------- TRACK -------------------- #

    async def track(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        try:

            if videoid:
                vid_id = link

            else:

                headers = {
                    "x-api-key": str(YT_API_KEY),
                    "User-Agent": "Mozilla/5.0",
                }

                session = create_session()

                search_url = f"{YTPROXY}/ytsearch"

                params = {
                    "query": link
                }

                response = session.get(
                    search_url,
                    headers=headers,
                    params=params,
                    timeout=60,
                )

                try:
                    data = response.json()
                except Exception:
                    logger.error(
                        f"Invalid JSON Response: {response.text}"
                    )
                    return None, None

                session.close()

                if data.get("status") != "success":

                    logger.error(
                        f"Search Failed: {data}"
                    )

                    return None, None

                results = data.get("result")

                if not results:

                    logger.error(
                        "No Search Results Found"
                    )

                    return None, None

                first = results[0]

                vid_id = (
                    first.get("videoId")
                    or first.get("id")
                )

                if not vid_id:

                    logger.error(
                        "Video ID Missing"
                    )

                    return None, None

            headers = {
                "x-api-key": str(YT_API_KEY),
                "User-Agent": "Mozilla/5.0",
            }

            session = create_session()

            info_url = f"{YTPROXY}/info/{vid_id}"

            response = session.get(
                info_url,
                headers=headers,
                timeout=60,
            )

            try:
                data = response.json()
            except Exception:
                logger.error(
                    f"Invalid Info JSON: {response.text}"
                )
                return None, None

            session.close()

            if data.get("status") != "success":

                logger.error(
                    f"Info Failed: {data}"
                )

                return None, None

            result = data.get("result")

            if not result:

                logger.error(
                    "Video Result Missing"
                )

                return None, None

            title = (
                result.get("title")
                or "Unknown Title"
            )

            duration = (
                result.get("duration")
                or "0:00"
            )

            thumbnail = (
                result.get("thumbnail")
                or result.get("thumb")
                or result.get("image")
                or "https://i.imgur.com/4LwPLai.png"
            )

            track_details = {

                "title": title,

                "link":
                    f"https://youtube.com/watch?v={vid_id}",

                "vidid": vid_id,

                "duration_min": duration,

                "thumb": thumbnail,

            }

            logger.info(
                f"Track Loaded Successfully: {title}"
            )

            return track_details, vid_id

        except Exception as e:

            logger.error(
                f"Track Error: {e}"
            )

            return None, None

# -------------------- FORMATS -------------------- #

    async def formats(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            raise ValueError("Unsafe URL blocked")

        ytdl_opts = {
            "quiet": True,
            "cookiefile": cookie_txt_file(),
        }

        ydl = yt_dlp.YoutubeDL(ytdl_opts)

        with ydl:

            formats_available = []

            r = ydl.extract_info(
                link,
                download=False,
            )

            for fmt in r["formats"]:

                try:

                    if "dash" in str(fmt["format"]).lower():
                        continue

                    formats_available.append(
                        {
                            "format": fmt.get("format"),
                            "filesize": fmt.get("filesize"),
                            "format_id": fmt.get("format_id"),
                            "ext": fmt.get("ext"),
                            "format_note": fmt.get("format_note"),
                            "yturl": link,
                        }
                    )

                except Exception:
                    continue

        return formats_available, link

    # -------------------- SLIDER -------------------- #

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        if not validate_youtube_url(link):
            raise ValueError("Unsafe URL blocked")

        search = VideosSearch(
            link,
            limit=10,
        )

        search_results = (
            await search.next()
        ).get("result", [])

        results = []

        for result in search_results:

            try:

                duration_str = result.get(
                    "duration",
                    "0:00",
                )

                parts = duration_str.split(":")

                duration_secs = 0

                if len(parts) == 3:

                    duration_secs = (
                        int(parts[0]) * 3600
                        + int(parts[1]) * 60
                        + int(parts[2])
                    )

                elif len(parts) == 2:

                    duration_secs = (
                        int(parts[0]) * 60
                        + int(parts[1])
                    )

                if duration_secs <= 3600:
                    results.append(result)

            except Exception:
                continue

        if not results:
            raise ValueError(
                "No videos found"
            )

        selected = results[query_type]

        return (
            selected["title"],
            selected["duration"],
            selected["thumbnails"][0]["url"],
            selected["id"],
        )

    # -------------------- DOWNLOAD -------------------- #

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ):

        if videoid:
            vid_id = link
            link = self.base + link

        if not validate_youtube_url(link):
            raise ValueError(
                "Unsafe URL blocked"
            )

        if not YT_API_KEY:
            logger.error(
                "YT_API_KEY missing"
            )
            return None

        if not YTPROXY:
            logger.error(
                "YTPROXY missing"
            )
            return None

        headers = {
            "x-api-key": str(YT_API_KEY),
            "User-Agent": "Mozilla/5.0",
        }

        session = create_session()

        try:

            endpoint = (
                f"{YTPROXY}/info/{vid_id}"
            )

            response = session.get(
                endpoint,
                headers=headers,
                timeout=60,
            )

            data = response.json()

        except Exception as e:

            logger.error(
                f"API Error: {e}"
            )

            return None

        finally:
            session.close()

        if data.get("status") != "success":
            return None

        if songvideo or video:

            media_url = data.get(
                "video_url"
            )

            filepath = (
                f"downloads/{vid_id}.mp4"
            )

        else:

            media_url = data.get(
                "audio_url"
            )

            filepath = (
                f"downloads/{vid_id}.mp3"
            )

        try:

            session = create_session()

            response = session.get(
                media_url,
                headers=headers,
                stream=True,
                timeout=120,
            )

            response.raise_for_status()

            with open(filepath, "wb") as file:

                for chunk in response.iter_content(
                    1024 * 1024
                ):

                    if chunk:
                        file.write(chunk)

            self.dl_stats[
                "downloads"
            ] += 1

            return filepath, True

        except Exception as e:

            logger.error(
                f"Download Failed: {e}"
            )

            if os.path.exists(filepath):
                os.remove(filepath)

            return None

        finally:
            session.close()
