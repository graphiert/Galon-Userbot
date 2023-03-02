import os
import asyncio
import time

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import HANDLER as cmd
from ..utils.basic import eor
from .help import HELP_CMD

PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
 "del": "Menghapus pesan, balas ke pesan.",
 "purge": "Menghapus pesan, balas ke pesan.",
 "purgeme [angka]": "Menghapus jumlah pesan anda, yang mau anda hapus."
}})


@Client.on_message(filters.command("del", cmd) & filters.me)
async def del_msg(_, message: Message):
    await message.reply_to_message.delete()
    await message.delete()


@Client.on_message(filters.command("purge", cmd) & filters.me)
async def purge(client: Client, message: Message):
    start_time = time.time()
    message_ids = []
    purge_len = 0
    event = await eor(message, "`Starting To Purge Messages!`")
    me_m = await client.get_me()
    if message.chat.type in ["supergroup", "channel"]:
        me_ = await message.chat.get_member(int(me_m.id))
        if not me_.can_delete_messages:
            await event.edit("`I Need Delete Permission To Do This!`")
            return
    if not message.reply_to_message:
        await event.edit("`Reply To Message To Purge!`")
        return
    async for msg in client.iter_history(
        chat_id=message.chat.id,
        offset_id=message.reply_to_message.message_id,
        reverse=True,
    ):
        if msg.message_id != message.message_id:
            purge_len += 1
            message_ids.append(msg.message_id)
            if len(message_ids) >= 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                message_ids.clear()
    if message_ids:
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=message_ids, revoke=True
        )
    end_time = time.time()
    u_time = round(end_time - start_time)
    await event.edit(
        f"**» Fast Purge Done!** \n**» Total Message Purged :** `{purge_len}` \n**» Time Taken :** `{u_time}`",
    )
    await asyncio.sleep(3)
    await event.delete()


@Client.on_message(filters.command("purgeme", cmd) & filters.me)
async def purgeme(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.delete()
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await eor(message, "Harap masukan angka")
    n = int(n)
    if n < 1:
        return await eor(message, "Masukan jumlah pesan yang ingin dihapus!")
    chat_id = message.chat.id
    message_ids = [
        m.message_id
        async for m in client.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await eor(message, "Tidak dapat menemukan pesan.")
    to_delete = [message_ids[i : i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
