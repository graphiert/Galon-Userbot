import os
from googletrans import Translator
from inspect import getfullargspec

from pyrogram.types import Message
from pyrogram import Client, filters
from .. import HANDLER
from .help import HELP_CMD

trl = Translator()


async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@Client.on_message(filters.command("tr", HANDLER) & filters.me)
async def translate(client, message):
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await edrep(message, text=f"Penggunaan: Balas ke suatu pesan, lalu `{HANDLER}tr [lang]`")
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await edrep(message, text=f"Error: `{str(err)}`")
            return
    else:
        if len(message.text.split()) <= 2:
            await edrep(message, text=f"Penggunaan: `{HANDLER}tr [lang] [text]`")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await edrep(message, text="Error: `{}`".format(str(err)))
            return

    await edrep(
        message,
        text=f"Terjemahkan dari `{detectlang.lang}` ke `{target}`:\n```{tekstr.text}```",
    )

PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f'tr [text or reply]': 'Menerjemahkan suatu text ke bahasa lain.'
    }
})
