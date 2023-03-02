import asyncio, math, os
from PIL import Image
from typing import Tuple

from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram import Client, filters
from pyrogram.types import Message

from .. import HANDLER
from .help import HELP_CMD


@Client.on_message(filters.command(["kang", "steal"], HANDLER) & filters.me)
async def kang(client: Client, message):
    get_me = await client.get_me()
    teks = await message.edit_text("**Stiker yang bagus, saya ambil yah...**")
    if not message.reply_to_message:
        await teks.edit("Tolong Balas ke Stiker!")
        return
    xxx = get_text(message)
    name = ""
    pack = 1
    username = message.from_user.username
    if username:
        nam = message.from_user.username
        name = nam[1:]
    else:
        await client.get_me()
    packname = f"{get_me.first_name} Kang Pack {pack}"
    packshortname = f"Galon_{message.from_user.id}_{pack}"
    emoji = "👑"
    try:
        xxx = xxx.strip()
        if not xxx.isalpha():
            if not xxx.isnumeric():
                emoji = xxx
        else:
            emoji = "👑"
    except BaseException:
        emoji = "👑"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not xxx:
            emoji = message.reply_to_message.sticker.emoji or "😁"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            convert = await convert_to_image(message, client)
            if not convert:
                await teks.edit("**Balas ke media yang valid!**")
                return
            file_name = resize_image(convert)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        convert = await convert_to_image(message, client)
        if not convert:
            await teks.edit("**Balas ke media yang valid!**")
            return
        file_name = resize_image(convert)
    try:
        exist = await client.send(
            GetStickerSet(
                stickerset=InputStickerSetShortName(short_name=packshortname), hash=0
            )
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await client.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await teks.edit("**Tolong unblock** @Stickers **terlebih dahulu!**")
            await client.unblock_user("stickers")
        await client.send_message("stickers", packshortname)
        await asyncio.sleep(2)
        limit = "50" if is_anim else "120"
        yyy = (await client.get_history("stickers", 1))[0]
        while limit in yyy.text:
            pack += 1
            prev_pack = int(pack) - 1
            await teks.edit(
                f"Kang Pack Vol __{prev_pack}__ is Full! Switching To Vol __{pack}__ Kang Pack"
            )
            huh = await client.get_me()
            nama = huh.first_name
            packname = f"@{nama} Kang Pack {pack}"
            packshortname = f"Galon_{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await client.send_message("stickers", packshortname)
            await asyncio.sleep(2)
            yyy = (await client.get_history("stickers", 1))[0]
            if yyy.text == "Invalid pack selected.":
                if is_anim:
                    await client.send_message("stickers", "/newanimated")
                else:
                    await client.send_message("stickers", "/newpack")
                await asyncio.sleep(2)
                await client.send_message("stickers", packname)
                await asyncio.sleep(2)
                await client.send_document("stickers", file_name)
                await asyncio.sleep(2)
                await client.send_message("stickers", emoji)
                await asyncio.sleep(2)
                await client.send_message("stickers", "/publish")
                if is_anim:
                    await client.send_message("stickers", f"<{packname}>")
                await client.send_message("stickers", "/skip")
                await asyncio.sleep(2)
                await client.send_message("stickers", packshortname)
                await teks.edit(
                    "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                        emoji, packshortname
                    )
                )
                return
        await client.send_document("stickers", file_name)
        await asyncio.sleep(2)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(2)
        await client.send_message("stickers", "/done")
        await teks.edit(
            "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                emoji, packshortname
            )
        )
    else:
        if is_anim:
            await client.send_message("stickers", "/newanimated")
        else:
            await client.send_message("stickers", "/newpack")
        await client.send_message("stickers", packname)
        await asyncio.sleep(2)
        await client.send_document("stickers", file_name)
        await asyncio.sleep(2)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(2)
        await client.send_message("stickers", "/publish")
        await asyncio.sleep(2)
        if is_anim:
            await client.send_message("stickers", f"<{packname}>")
        await client.send_message("stickers", "/skip")
        await asyncio.sleep(2)
        await client.send_message("stickers", packshortname)
        await teks.edit(
            "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                emoji, packshortname
            )
        )
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
            downname = "./Downloads"
            if os.path.isdir(downname):
                shutil.rmtree(downname)
        except BaseException:
            print("ERROR: Can't remove downloaded sticker files")
            return


@Client.on_message(filters.command(["getsticker",
                  "get_sticker"], HANDLER) & filters.me)
async def getsticker(client, message):
    reply = message.reply_to_message
    if not reply or not reply.sticker:
        return await message.edit("**Harap balas ke stiker**")
    txt = await message.edit("**Mengconvert ke foto...**")
    convert = await convert_to_image(message, client)
    file_name = resize_image(convert)
    await client.send_document(message.chat.id, file_name)
    await txt.delete()


# ------------------------------------------

def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def convert_to_image(message, client) -> [None, str]:
    if not message:
        return None
    if not message.reply_to_message:
        return None
    final_path = None
    if not (
        message.reply_to_message.video
        or message.reply_to_message.photo
        or message.reply_to_message.sticker
        or message.reply_to_message.media
        or message.reply_to_message.animation
        or message.reply_to_message.audio
    ):
        return None
    if message.reply_to_message.photo:
        final_path = await message.reply_to_message.download()
    elif message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await message.reply_to_message.download()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await client.download_media(message.reply_to_message)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await run_cmd(cmd)
    elif message.reply_to_message.audio:
        thumb = message.reply_to_message.audio.thumbs[0].file_id
        final_path = await client.download_media(thumb)
    elif message.reply_to_message.video or message.reply_to_message.animation:
        final_path = "fetched_thumb.png"
        vid_path = await client.download_media(message.reply_to_message)
        await run_cmd(f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path


def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = "Sticker.png"
    im.save(file_name, "PNG")
    if os.path.exists(image):
        os.remove(image)
    return file_name


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"kang": "Memasukkan foto atau stiker ke packmu.",
        f"getsticker": "Mengconvert stiker ke foto."
    }
})
