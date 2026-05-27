from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import (
    ChatAdminRequired,
    UserNotParticipant,
    ChatWriteForbidden,
)
from SONALI import app

MUST_JOIN = "theshonabots"  # without @

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):

    if not MUST_JOIN:
        return

    if not msg.from_user:
        return

    try:
        await app.get_chat_member(MUST_JOIN, msg.from_user.id)

    except UserNotParticipant:

        # username link
        if str(MUST_JOIN).startswith("@"):
            link = f"https://t.me/{MUST_JOIN[1:]}"
        else:
            try:
                chat = await app.get_chat(MUST_JOIN)
                link = chat.invite_link

                if not link:
                    link = f"https://t.me/{MUST_JOIN}"

            except Exception:
                link = f"https://t.me/{MUST_JOIN}"

        try:
            await msg.reply_photo(
                photo="https://files.catbox.moe/naban1.jpg",
                caption=(
                    f"๏ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ "
                    f"[๏ sᴜᴘᴘᴏʀᴛ ๏]({link}) "
                    f"ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄʜᴇᴄᴋ ᴍʏ ғᴇᴀᴛᴜʀᴇs.\n\n"
                    f"ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɴᴅ ᴛʏᴘᴇ /start"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "• ᴊᴏɪɴ •",
                                url=link
                            )
                        ]
                    ]
                )
            )

            await msg.stop_propagation()

        except ChatWriteForbidden:
            pass

    except ChatAdminRequired:
        print(
            f"Promote bot as admin in MUST_JOIN chat: {MUST_JOIN}"
                  )
