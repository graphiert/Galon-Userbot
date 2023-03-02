import time
import os
from asyncio import sleep
from requests import get

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from .. import HANDLER, DEVS
from ..utils.basic import eor
from .help import HELP_CMD


BLACKLIST_GCAST = get(
    "https://raw.githubusercontent.com/SeorangDion/Cool/dion/gcastblacklist.json").json()


@Client.on_message(filters.command(["gcast",
                  "broadcast"], HANDLER) & filters.me)
async def gcast(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    start_time = time.time()
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await eor(message, "**Berikan Sebuah Pesan atau Reply**")
    txt = await eor(message, "`Memulai global broadcast...`")
    list_chat = 0
    error_chats = 0
    async for dialogs in client.iter_dialogs():
        if dialogs.chat.type in ("group", "supergroup"):
            chat = dialogs.chat.id
            if chat not in BLACKLIST_GCAST:
                try:
                    await client.send_message(chat, text)
                    await sleep(0.1)
                    list_chat += 1
                except FloodWait as e:
                    await sleep(e.value)
                    await client.send_message(chat, text)
                    list_chat += 1
                except Exception:
                    error_chats += 1
    end_time = time.time()
    get_time = round(end_time - start_time)
    await txt.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{list_chat}` **Grup**\n**Gagal Mengirim Pesan Ke** `{error_chats}` **Grup**\n\n**Selesai Dalam** `{get_time}` **Detik**"
    )


@Client.on_message(filters.command("gucast", HANDLER) & filters.me)
async def gucast(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    start_time = time.time()
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await eor(message, "**Berikan Sebuah Pesan atau Reply**")
    teks = await eor(message, "`Started global broadcast to users...`")
    chat_list = 0
    error_chats = 0
    async for dialogs in client.iter_dialogs():
        if dialogs.chat.type == "private" and not dialog.chat.is_verified:
            chat = dialogs.chat.id
            if chat not in DEVS:
                try:
                    await client.send_message(chat, text)
                    await sleep(0.1)
                    chat_list += 1
                except FloodWait as e:
                    await sleep(e.value)
                    await client.send_message(chat, text)
                    chat_list += 1
                except Exception:
                    error_chats += 1
    end_time = time.time()
    get_time = round(end_time - start_time)
    await teks.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{chat_list}` **Chat**\n**Gagal Mengirim Pesan Ke** `{error_chats}` **Chat**\n\n**Selesai Dalam** `{get_time}` **Detik**"
    )


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "gcast [text/reply]": "Mengirim pesan ke seluruh grup yang kamu masuki.",
    "gucast [text/reply]": "Mengirim pesan ke seluruh chat / Private Message."
}})
