import os, asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import HANDLER
from .help import HELP_CMD
from ..utils.basic import eor


@Client.on_message(filters.command("q", HANDLER) & filters.me)
async def _quotly(client: Client, message: Message):
    if not message.reply_to_message:
        return await eor(message, "**Balas ke sebuah pesan!**")
    msg = await eor(message, "`Making a Quote...`")
    await message.reply_to_message.forward("QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            await asyncio.sleep(4.2)
            sticker = await client.get_history("@QuotLyBot", 1)
            is_sticker = True
        except Exception as err:
            await msg.edit(f"**ERROR**:\n`{err}`")
    if msg_id := sticker[0]["message_id"]:
        await asyncio.gather(
            msg.delete(),
            client.copy_message(message.chat.id, "@QuotLyBot", msg_id)
        )


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"q": "Membuat kutipan stiker dari pesan [membalas pesan]"
    }
})
