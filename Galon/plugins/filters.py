import re, os

from pyrogram import Client, filters
from .. import *
from ..utils.pyrohelper import get_arg
from ..database.filters import (
    add_filters,
    all_filters,
    del_filters,
    filters_del,
    filters_info,
)

from .help import HELP_CMD
PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "filters": "Daftar semua filter aktif dalam obrolan saat ini.",
    "filter [keyword]": "Menyimpan filter.",
    "stop [keyword]": "Menghentikan filter tertentu.",
    "stopall": "Menghapus semua filter."
}})


@Client.on_message(filters.command("stop", HANDLER) & filters.me)
def del_filterz(client, message):
    note_ = message.edit("`Processing..`")
    note_name = get_arg(message)
    if not note_name:
        note_.edit(f"**Nama filter {note_name} tidak diperbolehkan.**")
        return
    note_name = note_name.lower()
    if not filters_info(note_name, int(message.chat.id)):
        note_.edit(f"**Filter** `{note_name}` **tidak ada.**")
        return
    del_filters(note_name, int(message.chat.id))
    note_.edit(f"**Filter** `{note_name}` **berhasil di hapus.**")


@Client.on_message(filters.command("filters", HANDLER) & filters.me)
def show_filters(client, message):
    a = message.edit("`Processing..`")
    b = all_filters(int(message.chat.id))
    if b is False:
        a.edit("**Tidak ada filter di chat ini.**")
        return
    kk = ""
    for c in b:
        kk += f"\n ◍ `{c.get('keyword')}`"
    X = client.get_chat(int(message.chat.id))
    grp_nme = X.title
    mag = f"**Daftar filter di {grp_nme}:** \n{kk}"
    a.edit(mag)


@Client.on_message(filters.command("filter", HANDLER) & filters.me)
def s_filters(client, message):
    note_ = message.edit("`Processing..`")
    note_name = get_arg(message)
    if not note_name:
        note_.edit(f"**Nama filter** `{note_name}` **tidak diperbolehkan.**")
        return
    if not message.reply_to_message:
        note_.edit("**Harap balas ke pesan untuk dijadikan filter.**")
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = msg.copy(int(BOTLOG_CHATID))
    add_filters(note_name, int(message.chat.id), copied_msg.message_id)
    note_.edit(f"**Filter** `{note_name}` **berhasil ditambahkan!**")


@Client.on_message(filters.incoming &
                  filters.group & ~filters.private & ~filters.me, group=3, )
def filter_s(client, message):
    owo = message.text
    al_fill = []
    is_m = False
    if not owo:
        return
    al_fil = all_filters(int(message.chat.id))
    if not al_fil:
        return
    for all_fil in al_fil:
        al_fill.append(all_fil.get("keyword"))
    owo.lower()
    for filter_s in al_fill:
        pattern = r"( |^|[^\w])" + re.escape(filter_s) + r"( |$|[^\w])"
        if re.search(pattern, owo, flags=re.IGNORECASE):
            f_info = filters_info(filter_s, int(message.chat.id))
            m_s = client.get_messages(int(BOTLOG_CHATID), f_info["msg_id"])
            if is_media(m_s):
                text_ = m_s.caption or ""
                is_m = True
            else:
                text_ = m_s.text or ""
            if text_ != "":
                mention = message.from_user.mention
                user_id = message.from_user.id
                user_name = message.from_user.username or "No Username"
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name or "No Last Name"
                text_ = text_.format(
                    mention=mention,
                    user_id=user_id,
                    user_name=user_name,
                    first_name=first_name,
                    last_name=last_name,
                )
            if not is_m:
                client.send_message(
                    message.chat.id,
                    text_,
                    reply_to_message_id=message.message_id)
            else:
                m_s.copy(
                    chat_id=int(message.chat.id),
                    caption=text_,
                    reply_to_message_id=message.message_id,
                )


def is_media(message):
    if not (
        message.photo
        or message.video
        or message.document
        or message.audio
        or message.sticker
        or message.animation
        or message.voice
        or message.video_note
    ):
        return False
    return True


@Client.on_message(filters.command("stopall", HANDLER) & filters.me)
def del_all_filters(client, message):
    a = message.edit("`Processing..`")
    poppy = all_filters(int(message.chat.id))
    if poppy is False:
        a.edit("**Filter tidak pernah diset di grup ini.**")
        return
    filters_del(int(message.chat.id))
    a.edit("**Semua filter berhasil dihapus!**")
