import os
from asyncio import sleep
from pyrogram import Client, filters
from .. import HANDLER
from .help import HELP_CMD


@Client.on_message(filters.command("limit", HANDLER) & filters.me)
async def limit(client, message):
    """ Check limit from t.me/SpamBot"""
    txt = await message.edit("`Processing...`")
    await sleep(1)
    msg = await client.get_history("SpamBot", 1)
    msg_id = msg[0]["message_id"]

    await client.send_message("SpamBot", "/start")
    await txt.delete()
    await client.copy_message(message.chat.id, "@SpamBot", msg_id)


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"limit": "Mengecek batasan akun."
    }
})
