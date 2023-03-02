import os

from pyrogram import Client, filters

from .. import HANDLER, PM_AUTO_BAN, PM_LIMIT
from ..database.pmpermit import *
from .help import HELP_CMD
from ..utils.pyrohelper import get_pmp

USERS_WARNS = {}

WARN_MESSAGE = """
Halo {}.
Pesan ini muncul karena kamu adalah salah satunya orang yang nyasar di Private Chat-nya orang.
Diingatkan untuk menunggu hingga Owner membalas.
Peringatan kamu sekarang berada di {}/{}.
Bila melebihi batas peringatan, kamu akan secara otomatis **diblokir oleh bot.**
Terima kasih.

Pesan ini dibuat dengan [Galon-Userbot.](https://github.com/galihpujiirianto/Galon-Userbot)
"""


@Client.on_message(
  filters.create(get_pmp) & ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69)
async def imcoming(client, message):
  if PM_AUTO_BAN == True:
    if approved_pm(message.chat.id) == True:
      return
    user = message.chat.id
    user_warns = USERS_WARNS.get(user) if user in USERS_WARNS else 0
    if user_warns < PM_LIMIT:
      USERS_WARNS.update({user: user_warns + 1})
      await message.reply(
      WARN_MESSAGE.format(message.from_user.first_name, USERS_WARNS[user], PM_LIMIT),
        disable_web_page_preview=True
      )
    elif user_warns == PM_LIMIT:
      await message.reply("Maaf, kamu telah **DIBLOKIR** karena telah melewati batas peringatan.")
      await client.block_user(user)
      del USERS_WARNS[user]
  else:
    return

@Client.on_message(filters.command("y", HANDLER) & filters.me)
async def approve(client, message):
  user = message.chat.id
  if approved_pm(message.chat.id) == True:
    await message.edit(f"{message.chat.first_name} telah ada di **PMPERMIT WHITELIST**.")
  else:
    approve_pm(message.chat.id)
    await message.edit(f"{message.chat.first_name} berhasil ditambahkan ke **PMPERMIT WHITELIST**!")
    del USERS_WARNS[user]

@Client.on_message(filters.command("n", HANDLER) & filters.me)
async def reject(client, message):
  if approved_pm(message.chat.id) == False:
    await message.edit(f"{message.chat.first_name} tidak ada di **PMPERMIT WHITELIST**.")
  else:
    reject_pm(message.chat.id)
    await message.edit(f"{message.chat.first_name} berhasil dihapus dalam **PMPERMIT WHITELIST**!")

PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "setvar PM_AUTO_BAN 1": "Mengaktifkan fitur PMPERMIT (defaultnya nonaktif)",
    "delvar PM_AUTO_BAN": "Menonaktifkan fitur PMPERMIT",
    "setvar PM_LIMIT [angka]": "Mengatur batasan peringatan",
    "y": "Menerima Private Chat dari seseorang",
    "n": "Menolak Private Chat dari seseorang"
}})
