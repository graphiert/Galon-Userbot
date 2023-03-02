import os
from io import BytesIO

from pyrogram.types import Message
from pyrogram import Client, filters
from .. import HANDLER, aiosession

from .help import HELP_CMD


@Client.on_message(filters.command("carbon", HANDLER) & filters.me)
async def carbon_func(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    teks = await message.edit("`Preparing Carbon...`")
    carbon = await make_carbon(text)
    await teks.edit("`Uploading...`")
    king = await client.get_me()
    await client.send_photo(
        message.chat.id,
        carbon,
        caption=f"**Carbonised by** [{king.first_name}](tg://user?id={king.id})",
    )
    await teks.delete()
    carbon.close()


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f'carbon': 'Karbonisasi teks.'
    }
})
