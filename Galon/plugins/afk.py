import os
import time
import asyncio
from .. import *
from ..database.afk import *
from ..utils.time import *
from pyrogram import Client, filters

from .help import HELP_CMD


@Client.on_message(filters.command("afk", HANDLER) & filters.me)
async def afk(client: Client, message):
    me = await client.get_me()
    name = me.first_name
    reason = message.text.split(" ", 1)
    cekrep = message.reply_to_message
    if cekrep:
        if cekrep.sticker or cekrep.photo and len(reason) > 1:
            if cekrep.sticker:
                a = await message.reply_sticker(cekrep.sticker.file_id)
                b = await message.reply(f"{name} telah AFK!\nKarena: {reason[1]}")
                c = await client.send_sticker(BOTLOG_CHATID, cekrep.sticker.file_id)
                await c.reply(f"{name} telah AFK!\nKarena: {reason[1]}")
            elif cekrep.photo:
                capt = f"{name} telah AFK!\nKarena: {reason[1]}"
                a = await message.reply_photo(cekrep.photo.file_id, caption=capt)
                await client.send_photo(BOTLOG_CHATID, cekrep.photo.file_id, caption=capt)
            reason = data_reason(reason[1], cekrep.sticker.file_id if cekrep.sticker else cekrep.photo.file_id)
            add_afk(reason)
        elif cekrep.sticker or cekrep.photo and len(reason) == 1:
            if cekrep.sticker:
                a = await message.reply_sticker(cekrep.sticker.file_id)
                b = await message.reply(f"{name} telah AFK!")
                c = await client.send_sticker(BOTLOG_CHATID, cekrep.sticker.file_id)
                await c.reply(f"{name} telah AFK!")
            elif cekrep.photo:
                capt = f"{name} telah AFK!"
                a = await message.reply_photo(cekrep.photo.file_id, caption=capt)
                await client.send_photo(BOTLOG_CHATID, cekrep.photo.file_id, caption=capt)
            reason = data_reason(media=cekrep.sticker.file_id if cekrep.sticker else cekrep.photo.file_id)
            add_afk(reason)
        else:
            a = await message.edit("**AFK hanya bisa menggunakan media gambar atau stiker!**")
        try:
            await asyncio.sleep(3.5)
            await a.delete()
            await message.delete()
            await b.delete()
        except Exception:
            pass
    else:
        if len(reason) > 1:
            a = await message.edit_text(f"{name} telah AFK!\nKarena: {reason[1]}")
            await client.send_message(BOTLOG_CHATID, f"{name} telah AFK!\nKarena: {reason[1]}")
            add_afk(data_reason(text=reason[1]))
        else:
            a = await message.edit_text(f"{name} telah AFK!")
            await client.send_message(BOTLOG_CHATID, f"{name} telah AFK!")
            add_afk(data_reason())
        await asyncio.sleep(3.5)
        await a.delete()
    await message.stop_propagation()


@Client.on_message(filters.me & ~filters.private & filters.group, group=12)
async def delafk(client: Client, message):
    user = await client.get_me()
    name = user.first_name
    cek = is_afk()
    if cek:
        waktu = get_readable_time(int(time.time()) - int(cek.get("time")))
        remove_afk()
        txt = await message.reply(f"{name} telah kembali setelah AFK selama {waktu}!")
        await asyncio.sleep(3.5)
        await txt.delete()
        mentioners = search_remove_mention()
        tagger = f"Selamat datang kembali, {message.from_user.first_name}."
        if len(mentioners) >= 1:
            tagger += f" Ada sekitar {len(mentioners)} yang telah memention kamu saat kamu AFK. Cek dibawah ini!"
        else:
            tagger += " Tidak ada yang memention kamu saat kamu AFK."
        await client.send_message(BOTLOG_CHATID, tagger)
        i = 1
        for mentioner in mentioners:
            waktu = get_readable_time(int(time.time()) - int(mentioner.get("time")))
            data = mentioner["data"]
            await client.send_message(
                BOTLOG_CHATID,
                f"{i}. Dari: [{data['nameuser']}](tg://user?id={data['userid']}) @ {data['group']}\n"
                f"Link ke chat: {data['link']}\n"
                f"Kamu ditag {waktu} yang lalu setelah kamu AFK.",
                disable_web_page_preview=True
            )
            i += 1
    else:
        return


@Client.on_message(filters.mentioned & ~filters.bot, group=11)
async def termention(client: Client, message):
    getme = await client.get_me()
    name = getme.first_name
    cek = is_afk()
    if cek:
        waktu = get_readable_time(int(time.time()) - cek.get("time"))
        if cek.get("data").get("text") and cek.get("data").get("file"):
            try:
                await message.reply_sticker(cek.get("data").get("file"))
                await message.reply(f"**{name} sedang tidak ada disini!**\nKarena: {cek.get('data').get('text')}, selama {waktu}.")
            except Exception:
                capt = f"**{name} sedang tidak ada disini!**\nKarena: {cek.get('data').get('text')}, selama {waktu}."
                await message.reply_photo(cek.get("data").get("file"), caption=capt)
        elif cek.get("data").get("text"):
            await message.reply(f"**{name} sedang tidak ada disini!**\nKarena: {cek.get('data').get('text')}, selama {waktu}.")
        elif cek.get("data").get("file"):
            try:
                await message.reply_sticker(cek.get("data").get("file"))
                await message.reply(f"**{name} sedang tidak ada disini!**\nSelama {waktu}.")
            except Exception:
                capt = f"**{name} sedang tidak ada disini!**\nSelama {waktu}."
                await message.reply_photo(cek.get("data").get("file"), caption=capt)
        else:
            await message.reply(f"**{name} sedang tidak ada disini!**\nSelama {waktu}.")
        if message.chat.username:
            msg_link = f"https://t.me/{message.chat.username}/{message.message_id}"
        elif (str(message.chat.id)).startswith("-100"):
            msg_link = f"https://t.me/c/{(str(message.chat.id)).replace('-100', '')}/{message.message_id}"
        add_mention(
            message.from_user.first_name,
            message.from_user.id,
            message.chat.title,
            msg_link)
    else:
        return

PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        'afk': 'menandakan bahwa kamu sedang AFK',
        'note': 'fitur ini belum sepenuhnya stabil, bila menemukan error harap lapor ke @GalonSupport'
    }
})
