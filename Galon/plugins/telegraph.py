import os

from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, upload_file

from .. import HANDLER
from ..utils.basic import eor
from .help import HELP_CMD


telegraph = Telegraph()
name = telegraph.create_account(short_name="Galon-Userbot")
auth_url = name["auth_url"]


@Client.on_message(filters.command(["tg", "telegraph"], HANDLER) & filters.me)
async def tg(client: Client, message: Message):
    reply = message.reply_to_message
    filesize = 5242880
    msg = await eor(message, "`Processing...`")
    if not reply:
        await msg.edit(
            "**Mohon Balas Ke Pesan, Untuk Mendapatkan Link dari Telegraph.**"
        )
    elif reply.text:
        if len(reply.text) <= 4096:
            own = await client.get_me()
            link = telegraph.create_page(
                own.first_name,
                html_content=(reply.text.html).replace("\n", "<br>"),
            )
            await msg.edit(
                f"**Berhasil diupload ke [Telegraph](https://telegra.ph/{link.get('path')})**",
                disable_web_page_preview=True
            )
        else:
            await msg.edit("**Panjang teks melebihi 4096 karakter.**")
    elif reply.media:
        if (
            reply.photo
            and reply.photo.file_size <= filesize
            or reply.video
            and reply.video.file_size <= filesize
            or reply.animation
            and reply.animation.file_size <= filesize
            or reply.sticker
            and reply.sticker.file_size <= filesize
            or reply.document
            and reply.document.file_size <= filesize
        ):
            if reply.animation or reply.sticker:
                media = await client.download_media(reply, file_name=f"telegraph.png")
            else:
                media = await client.download_media(reply)
            try:
                file = upload_file(media)
            except Exception as err:
                return await msg.edit(f"**ERROR:** `{err}`")
            await msg.edit(
                f"**Berhasil diupload ke [Telegraph](https://telegra.ph{file[0]})**",
                disable_web_page_preview=True
            )
            if os.path.exists(media):
                os.remove(media)
        else:
            await msg.edit(
                "**Silahkan cek format berkas atau ukuran berkas, ukuran berkas harus kurang dari 5 MB!**"
            )
    else:
        await msg.edit("**Maaf, format file tidak didukung.**")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "tg": "Beri Teks atau Balas ke Pesan Teks atau Media untuk mengunggahnya ke telegraph."
}})
