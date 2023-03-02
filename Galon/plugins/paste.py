import os
import re
import aiofiles

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import HANDLER
from ..utils.paste import paste
from ..utils.basic import eor
from .help import HELP_CMD


pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@Client.on_message(filters.command("paste", HANDLER) & filters.me)
async def paste_func(client, message: Message):
    if not message.reply_to_message:
        return await eor(message, f"Balas ke pesan dengan `{HANDLER}paste`")
    reply = message.reply_to_message
    if not reply.text and not reply.document:
        return await eor(message, "**Hanya teks dan dokumen yang didukung!**")
    msg = await eor(message, "`Pasting...`")
    if reply.text:
        content = str(reply.text)
    elif reply.document:
        if reply.document.file_size > 40000:
            return await msg.edit("**Kamu hanya bisa mempaste dokumen dengan ukuran dibawah 40KB!**")
        if not pattern.search(reply.document.mime_type):
            return await msg.edit("**Hanya file teks yang dapat di paste!**")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as fek:
            content = await fek.read()
        os.remove(doc)
    link = await paste(content)
    try:
        if msg.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"**Paste Link:** [Disini]({link})",
            )
        await msg.delete()
    except Exception:
        await msg.edit(f"[Here]({link}) your paste")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "paste": "Balas ke Pesan Teks atau Dokumen untuk mengunggahnya ke pastebin."
}})
