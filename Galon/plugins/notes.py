from pyrogram import Client, filters

from ..database.notes import *
from .. import *
from ..utils.pyrohelper import get_arg

import os
from .help import HELP_CMD
PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    'save': 'Simpan catatan baru.',
    'get': 'Mendapatkan catatan yang ditentukan.',
    'clear': 'Menghapus catatan, ditentukan oleh nama catatan.',
    'clearall': 'Menghapus semua catatan yang disimpan.',
    'notes': 'Daftar catatan yang disimpan.'
}})


@Client.on_message(filters.command("save", HANDLER) & filters.me)
def save(client: Client, message):
    arg = get_arg(message)
    if not arg:
        message.edit("**Anda harus memberi nama untuk sebuah catatan.**")
        return
    note_name = arg
    note = get_note(note_name)
    if note:
        message.edit(f"**`{note_name}` sudah ada. Gunakan nama lain.**")
        return
    reply = message.reply_to_message
    if not reply:
        message.edit("**Balas pesan untuk menyimpan catatan.**")
        return
    copy = client.copy_message(BOTLOG_CHATID, message.chat.id, reply.message_id)
    save_note(note_name, copy.message_id)
    message.edit("**Catatan berhasil di simpan!**")


@Client.on_message(filters.command("get", HANDLER) & filters.me)
def get(client: Client, message):
    arg = get_arg(message)
    if not arg:
        message.edit("**Masukkan nama note yang tepat.**")
        return
    note_name = arg
    note = get_note(note_name)
    if not note:
        message.edit(
            f"**Note {note_name} tidak ada. Pastikan penulisanmu benar, lalu coba lagi!**")
        return
    if message.reply_to_message:
        client.copy_message(
            message.chat.id,
            BOTLOG_CHATID,
            note,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        client.copy_message(message.chat.id, BOTLOG_CHATID, note)
    message.delete()


@Client.on_message(filters.command("clear", HANDLER) & filters.me)
def clear(client, message):
    arg = get_arg(message)
    if not arg:
        message.edit("**Masukkan nama note yang ingin dihapus.**")
        return
    note_name = arg
    note = get_note(note_name)
    if not note:
        message.edit(f"**Gagal menghapus catatan `{note_name}`...**")
        return
    rm_note(note_name)
    message.edit(f"**Berhasil menghapus catatan `{note_name}`!**")


@Client.on_message(filters.command("notes", HANDLER) & filters.me)
def notes(client, message):
    global get_all_notes
    msg = "**Catatan Tersimpan:**\n\n"
    all_notes = get_all_notes()
    if not all_notes:
        message.edit("**Tidak ada catatan yang disimpan.**")
        return
    for notes in all_notes:
        msg += f"◍ `{notes}`\n"
    message.edit(msg)


@Client.on_message(filters.command("clearall", HANDLER) & filters.me)
def clearall(client, message):
    rm_all()
    message.edit("**Semua catatan berhasil dihapus!**")
