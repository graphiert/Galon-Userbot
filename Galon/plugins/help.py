from pyrogram import Client, filters
from .. import HANDLER

HELP_CMD = {}


@Client.on_message(filters.command("help", HANDLER) & filters.me)
async def help(client, message):
    arguments = list(message.text.split(" "))
    if len(arguments) > 1:
        arg = arguments[1].lower()
        if arg in HELP_CMD:
            val = ""
            for cmd, use in HELP_CMD[arg].items():
                if cmd.lower() == 'note':
                    continue
                val += f"\n`{HANDLER}{cmd}` => {use}"
            if "note" in HELP_CMD[arg].keys():
                val += f"\n\nCatatan: {HELP_CMD[arg]['note']}"
            return await message.edit(f"Berikut ini daftar perintah untuk module **{arg}**\n{val}")
        else:
            return await message.edit(f"""**Module {arg} tidak ditemukan!**
__Cek apakah terdapat kesalahan saat menuliskan module, lalu coba lagi.__""")
    else:
        isikey = []
        mes = "**DAFTAR MODULE GALON-USERBOT**\n\n"
        for key in HELP_CMD:
            isikey.append(f"`{key}`")
        mes += str(" | ".join(isikey))
        mes += f"\n\nUntuk melihat cara penggunaannya,"
        mes += f" ketik `{HANDLER}help` diikuti nama module."
        mes += f"\nContoh: `{HANDLER}help ping`"
        return await message.edit(mes)


# Cara membuat help
"""
from .help import HELP_CMD
import os
PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    'namaperintah': 'fungsi perintah',
    'namaperintah2': 'fungsi perintah 2',
    'note': 'catatan tentang modul ini'
}})
"""
