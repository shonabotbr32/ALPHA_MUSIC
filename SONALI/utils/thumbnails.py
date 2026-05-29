# =========================================================
#                MADE BY HARSH CHAURASIYA 🥰
# =========================================================

import os
import re
import aiofiles
import aiohttp

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
)

from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

# =========================================================
# CACHE
# =========================================================

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# =========================================================
# PANEL SETTINGS
# =========================================================

PANEL_W, PANEL_H = 763, 545
PANEL_X = (1280 - PANEL_W) // 2
PANEL_Y = 88

TRANSPARENCY = 170
INNER_OFFSET = 36

THUMB_W, THUMB_H = 542, 273
THUMB_X = PANEL_X + (PANEL_W - THUMB_W) // 2
THUMB_Y = PANEL_Y + INNER_OFFSET

TITLE_X = 377
META_X = 377

TITLE_Y = THUMB_Y + THUMB_H + 10
META_Y = TITLE_Y + 45

BAR_X, BAR_Y = 388, META_Y + 45
BAR_RED_LEN = 280
BAR_TOTAL_LEN = 480

ICONS_W, ICONS_H = 415, 45
ICONS_X = PANEL_X + (PANEL_W - ICONS_W) // 2
ICONS_Y = BAR_Y + 48

MAX_TITLE_WIDTH = 580

# =========================================================
# TEXT TRIM
# =========================================================


def trim_to_width(text, font, max_width):
    ellipsis = "…"

    try:
        if font.getlength(text) <= max_width:
            return text
    except Exception:
        return text

    for i in range(len(text) - 1, 0, -1):
        candidate = text[:i] + ellipsis

        try:
            if font.getlength(candidate) <= max_width:
                return candidate
        except Exception:
            pass

    return ellipsis


# =========================================================
# DOWNLOAD IMAGE
# =========================================================


async def download_image(url, path):
    try:
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:

                if response.status != 200:
                    return False

                content = await response.read()

                async with aiofiles.open(path, "wb") as f:
                    await f.write(content)

        return os.path.exists(path)

    except Exception:
        return False


# =========================================================
# MAIN FUNCTION
# =========================================================


async def get_thumb(videoid: str):

    cache_path = os.path.join(
        CACHE_DIR,
        f"{videoid}_v4.png",
    )

    # =====================================================
    # RETURN CACHE
    # =====================================================

    if os.path.exists(cache_path):
        return cache_path

    # =====================================================
    # DEFAULT VALUES
    # =====================================================

    title = "Unsupported Title"
    thumbnail = YOUTUBE_IMG_URL
    duration = None
    views = "Unknown Views"

    # =====================================================
    # FETCH YOUTUBE DATA
    # =====================================================

    try:
        search = VideosSearch(videoid, limit=1)

        results = await search.next()

        result_items = results.get("result", [])

        if result_items:

            data = result_items[0]

            title = data.get(
                "title",
                "Unsupported Title",
            )

            title = re.sub(
                r"\s+",
                " ",
                title,
            ).strip()

            thumbs = data.get(
                "thumbnails",
                [],
            )

            if thumbs:
                thumbnail = thumbs[0].get(
                    "url",
                    YOUTUBE_IMG_URL,
                )

            duration = data.get("duration")

            views = (
                data.get("viewCount", {}).get("short")
                or "Unknown Views"
            )

    except Exception:
        pass

    # =====================================================
    # LIVE CHECK
    # =====================================================

    is_live = (
        not duration
        or str(duration).strip().lower()
        in [
            "",
            "live",
            "live now",
        ]
    )

    duration_text = (
        "Live"
        if is_live
        else duration
    )

    # =====================================================
    # DOWNLOAD THUMBNAIL
    # =====================================================

    thumb_path = os.path.join(
        CACHE_DIR,
        f"thumb_{videoid}.jpg",
    )

    downloaded = await download_image(
        thumbnail,
        thumb_path,
    )

    # fallback image
    if not downloaded:

        downloaded = await download_image(
            YOUTUBE_IMG_URL,
            thumb_path,
        )

        if not downloaded:
            return None

    # =====================================================
    # OPEN IMAGE
    # =====================================================

    try:
        original_thumb = (
            Image.open(thumb_path)
            .convert("RGBA")
        )

    except Exception:
        return None

    # =====================================================
    # CREATE BACKGROUND
    # =====================================================

    try:
        base = original_thumb.resize(
            (1280, 720)
        )

    except Exception:
        return None

    bg = (
        ImageEnhance.Brightness(
            base.filter(
                ImageFilter.BoxBlur(12)
            )
        ).enhance(0.6)
    )

    # =====================================================
    # GLASS PANEL
    # =====================================================

    panel_area = bg.crop(
        (
            PANEL_X,
            PANEL_Y,
            PANEL_X + PANEL_W,
            PANEL_Y + PANEL_H,
        )
    )

    overlay = Image.new(
        "RGBA",
        (PANEL_W, PANEL_H),
        (
            255,
            255,
            255,
            TRANSPARENCY,
        ),
    )

    frosted = Image.alpha_composite(
        panel_area,
        overlay,
    )

    mask = Image.new(
        "L",
        (PANEL_W, PANEL_H),
        0,
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.rounded_rectangle(
        (
            0,
            0,
            PANEL_W,
            PANEL_H,
        ),
        radius=50,
        fill=255,
    )

    bg.paste(
        frosted,
        (
            PANEL_X,
            PANEL_Y,
        ),
        mask,
    )

    draw = ImageDraw.Draw(bg)

    # =====================================================
    # LOAD FONTS
    # =====================================================

    try:
        title_font = ImageFont.truetype(
            "SONALI/assets/font2.ttf",
            32,
        )

        regular_font = ImageFont.truetype(
            "SONALI/assets/font.ttf",
            18,
        )

    except Exception:
        title_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()

    # =====================================================
    # THUMBNAIL
    # =====================================================

    thumb = original_thumb.resize(
        (
            THUMB_W,
            THUMB_H,
        )
    )

    thumb_mask = Image.new(
        "L",
        (
            THUMB_W,
            THUMB_H,
        ),
        0,
    )

    ImageDraw.Draw(thumb_mask).rounded_rectangle(
        (
            0,
            0,
            THUMB_W,
            THUMB_H,
        ),
        radius=20,
        fill=255,
    )

    bg.paste(
        thumb,
        (
            THUMB_X,
            THUMB_Y,
        ),
        thumb_mask,
    )

    # =====================================================
    # TITLE
    # =====================================================

    title = trim_to_width(
        title,
        title_font,
        MAX_TITLE_WIDTH,
    )

    draw.text(
        (
            TITLE_X,
            TITLE_Y,
        ),
        title,
        fill="black",
        font=title_font,
    )

    # =====================================================
    # META TEXT
    # =====================================================

    meta_text = f"YouTube | {views}"

    draw.text(
        (
            META_X,
            META_Y,
        ),
        meta_text,
        fill="black",
        font=regular_font,
    )

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    draw.line(
        [
            (
                BAR_X,
                BAR_Y,
            ),
            (
                BAR_X + BAR_RED_LEN,
                BAR_Y,
            ),
        ],
        fill="red",
        width=6,
    )

    draw.line(
        [
            (
                BAR_X + BAR_RED_LEN,
                BAR_Y,
            ),
            (
                BAR_X + BAR_TOTAL_LEN,
                BAR_Y,
            ),
        ],
        fill="gray",
        width=5,
    )

    draw.ellipse(
        [
            (
                BAR_X + BAR_RED_LEN - 7,
                BAR_Y - 7,
            ),
            (
                BAR_X + BAR_RED_LEN + 7,
                BAR_Y + 7,
            ),
        ],
        fill="red",
    )

    # =====================================================
    # TIME TEXT
    # =====================================================

    draw.text(
        (
            BAR_X,
            BAR_Y + 15,
        ),
        "00:00",
        fill="black",
        font=regular_font,
    )

    end_text = (
        duration_text
        or "Unknown"
    )

    end_x = (
        BAR_X
        + BAR_TOTAL_LEN
        - (
            90
            if is_live
            else 60
        )
    )

    draw.text(
        (
            end_x,
            BAR_Y + 15,
        ),
        end_text,
        fill=(
            "red"
            if is_live
            else "black"
        ),
        font=regular_font,
    )

    # =====================================================
    # ICONS
    # =====================================================

    icons_path = (
        "SONALI/assets/play_icons.png"
    )

    if os.path.isfile(icons_path):

        try:
            icons = (
                Image.open(icons_path)
                .resize(
                    (
                        ICONS_W,
                        ICONS_H,
                    )
                )
                .convert("RGBA")
            )

            r, g, b, a = icons.split()

            black_icons = Image.merge(
                "RGBA",
                (
                    r.point(lambda _: 0),
                    g.point(lambda _: 0),
                    b.point(lambda _: 0),
                    a,
                ),
            )

            bg.paste(
                black_icons,
                (
                    ICONS_X,
                    ICONS_Y,
                ),
                black_icons,
            )

        except Exception:
            pass

    # =====================================================
    # SAVE IMAGE
    # =====================================================

    try:
        bg.save(cache_path)

    except Exception:
        return None

    # =====================================================
    # CLEANUP
    # =====================================================

    try:
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception:
        pass

    return cache_path
