from pyrogram import Client, filters

from ..database.welcome import *
from .. import *
from ..utils.pyrohelper import welcome_chat

from .help import HELP_CMD
import os
PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "setwelcome": "Menyetel pesan selamat datang.",
    "clearwelcome": "Menonaktifkan pesan selamat datang dalam obrolan."
}})


@Client.on_message(filters.command("clearwelcome", HANDLER) & filters.me)
def welcome(client, message):
    clear_welcome(str(message.chat.id))
    message.edit("**Pesan selamat datang telah berhasil dihapus.**")


@Client.on_message(filters.create(welcome_chat) &
                  filters.new_chat_members, group=-2)
def new_welcome(client: Client, message):
    msg_id = get_welcome(str(message.chat.id))
    caption = ""
    men = ""
    msg = client.get_messages(BOTLOG_CHATID, msg_id)
    if msg.media:
        if msg.caption:
            caption = msg.caption
            if "{mention}" in caption:
                men = caption.replace("{mention}", "[{}](tg://user?id={})")
        if msg.photo and caption is not None:
            client.send_photo(
                message.chat.id,
                msg.photo.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        if msg.animation and caption is not None:
            client.send_animation(
                message.chat.id,
                msg.animation.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        if msg.sticker:
            client.send_sticker(
                message.chat.id,
                msg.sticker.file_id,
                reply_to_message_id=message.message_id,
            )

    else:
        text = msg.text
        if "{mention}" in text:
            men = text.replace("{mention}", "[{}](tg://user?id={})")
            client.send_message(
                message.chat.id,
                men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.message_id,
            )
        else:
            client.send_message(
                message.chat.id, text, reply_to_message_id=message.message_id
            )


@Client.on_message(filters.command("setwelcome", HANDLER) & filters.me)
def setwelcome(client, message):
    reply = message.reply_to_message
    if not reply:
        message.edit(
            "**Balas pesan atau media untuk mengatur pesan selamat datang.**")
        return
    frwd = client.copy_message(BOTLOG_CHATID, message.chat.id, reply.message_id)
    msg_id = frwd.message_id
    save_welcome(str(message.chat.id), msg_id)
    message.edit("**Pesan selamat datang telah disimpan.**")
