import os
from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from .. import HANDLER, group_call, DEVS
from ..utils.basic import eor
from .help import HELP_CMD


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"**No group call Found** {err_msg}")
    return False


@Client.on_message(filters.group & filters.command("startvc",
                                                  ["?"]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["startvc"], HANDLER) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    a = await eor(message, "`Processing...`")
    if flags == "channel":
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    try:
        await client.send(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await a.edit(f"**Berhasil memulai obrolan suara di** `{message.chat.title}`")
    except Exception as e:
        await a.edit(f"**INFO:** `{e}`")


@Client.on_message(filters.group & filters.command("stopvc",
                                                  ["?"]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["stopvc"], HANDLER) & filters.me)
async def end_vc_(client: Client, message: Message):
    chat_id = message.chat.title
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await eor(message, f"**Berhasil mengakhiri obrolan suara di** `{chat_id}`")


@Client.on_message(filters.group & filters.command("joinvc",
                                                  ["?"]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["joinvc",
                                   "join_vc"], HANDLER) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(
        message.command) > 1 else message.chat.id
    a = await eor(message, "`Processing....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await group_call.start(chat_id)
    except Exception as e:
        return await a.edit(f"**ERROR:** `{e}`")
    await a.edit(f"**Berhasil Join Ke Obrolan Suara di** `{message.chat.title}`")
    await sleep(5)
    await group_call.set_is_mute(True)


@Client.on_message(filters.group & filters.command("leavevc",
                                                  ["?"]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["leavevc",
                  "leave_vc"], HANDLER) & filters.me)
async def leavevc(client: Client, message: Message):
    chat_title = message.chat.title
    try:
        await group_call.stop()
    except Exception as e:
        return await eor(message, f"**ERROR:** `{e}`")
    await eor(
        message, f"**Berhasil Turun dari Obrolan Suara di** `{chat_title}`"
    )
PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    'startvc': 'Untuk Memulai voice chat group.',
    'stopvc': 'Untuk Memberhentikan voice chat group.',
    'joinvc': 'Untuk Bergabung ke voice chat group di grup tersebut.',
    'joinvc [group id/group username]': 'Untuk Bergabung ke voice chat group di grup yang ditentukan.',
    'leavevc': 'Untuk turun/keluar dari voice chat group.'
}})
