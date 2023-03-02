import os
from pyrogram import Client, filters

from .. import HANDLER as cmd
from ..utils.basic import eor

from .help import HELP_CMD


@Client.on_message(filters.command("create", cmd) & filters.me)
async def create(client: Client, message):
    if len(message.command) < 3:
        return await eor(
            message, f"""**Penulisanmu salah.
Ketik `{cmd}create channel [nama channel]` atau `{cmd}create group [nama grup]` untuk membuat grup.**"""
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    a = await eor(message, "`Processing...`")
    desc = "Welcome To My " + ("Group" if group_type == "group" else "Channel")
    if group_type == "group":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id["id"])
        await a.edit(
            f"**Berhasil Membuat Group Telegram: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "channel":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id["id"])
        await a.edit(
            f"**Berhasil Membuat Channel Telegram: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({ PLUGIN_NAME: {
    "create channel [nama channel]": "Untuk membuat channel telegram dengan userbot",
    "create group [nama grup]": "Untuk membuat group telegram dengan userbot",
}})
