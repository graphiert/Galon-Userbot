import os
from random import choice, randint

from pyrogram import Client, filters
from ..utils.tod import *
from ..utils.basic import eor
from .. import HANDLER
from .help import HELP_CMD


@Client.on_message(filters.command("truth", HANDLER) & filters.me)
async def _truth(client, message):
    truth = choice(TRUTH_MSG)
    await eor(message, f"**Tugas Kejujuran anda:**\n\n`{truth}`")


@Client.on_message(filters.command("dare", HANDLER) & filters.me)
async def _dare(client, message):
    dare = choice(DARE_MSG)
    await eor(message, f"**Tantangan untuk anda:**\n\n`{dare}`")


@Client.on_message(filters.command("spill", HANDLER) & filters.me)
async def _spill(client, message):
    spill = choice(SPILL_MSG)
    await eor(message, f"**Tugas Spill anda:**\n\n`{spill}`")


@Client.on_message(filters.command("wish", HANDLER) & filters.me)
async def _wish(client, message):
   if len(message.command) == 1:
       await eor(message, "**Mohon berikan keinginan anda!**")
       return

   wish = message.text.split(maxsplit=1)[1]
   angka = randint(1,100)
   await eor(message, f"**Keinginanmu**: __{wish}__\n\n**Peluang sukses**: `{angka}%`")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({ PLUGIN_NAME: {
    "truth": "Memberikan tugas kejujuran.",
    "dare": "Memberikan tantangan.",
    "spill": "Spill sesuatu.",
    "wish": "Melemparkan keinginan."
}})
