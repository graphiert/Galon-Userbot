import os, time, asyncio
from datetime import datetime
from speedtest import Speedtest
from platform import python_version as pyver

from pyrogram import Client, filters, __version__ as pyro_ver
from .. import HANDLER, BOT_VER, ALIVE_TEXT, ALIVE_PIC
from ..utils.time import *
from .help import HELP_CMD

SPEEDTEST = (
    "Speedtest Started: `{start}`\n\n"
    "Ping: `{ping} ms`\n"
    "Download: `{download}`\n"
    "Upload: `{upload}`\n"
    "ISP: `{isp}`"
)


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@Client.on_message(filters.command("ping", HANDLER) & filters.me)
async def ping(client, message):
    uptime = get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await message.edit("`Pinging...`")
    end = datetime.now()
    pong = (end - start).microseconds / 1000
    owner = await client.get_me()
    await message.edit_text(
        f"**Ping -** `{pong} ms`\n"
        f"**Uptime -** `{uptime}`\n"
        f"**Owner**: [{owner.first_name}](tg://user?id={owner.id})"
    )


@Client.on_message(filters.command(["speedtest",
                  "speed"], HANDLER) & filters.me)
async def speedtest(client, message):
    teks = await message.edit_text("`Running Speedtest . . .`")
    speed = Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    speed.results.share()
    results = speed.results.dict()
    speed_text = SPEEDTEST.format(
        start=results["timestamp"],
        ping=results["ping"],
        download=speed_convert(results["download"]),
        upload=speed_convert(results["upload"]),
        isp=results["client"]["isp"],
    )
    await teks.edit(speed_text, disable_web_page_preview=True)


@Client.on_message(filters.command("alive", HANDLER) & filters.me)
async def _alive(client, message):
    text = await message.edit("`Yahoo...`")
    await asyncio.sleep(0.5)
    uptime = get_readable_time((time.time() - StartTime))
    owner = await client.get_me()
    TEXT = f"🔥 [Galon-Userbot](https://github.com/galihpujiirianto/Galon-Userbot) **Aktif!**\n\n"
    TEXT += f"**{ALIVE_TEXT}**\n\n"
    TEXT += f"📍 **Master**: [{owner.first_name}](tg://user?id={owner.id})\n"
    TEXT += f"📍 **Versi Bot**: `{BOT_VER}`\n"
    TEXT += f"📍 **Versi Python**: `{pyver()}`\n"
    TEXT += f"📍 **Versi Pyrogram**: `{pyro_ver}`\n"
    TEXT += f"📍 **Uptime**: `{uptime}`\n"
    TEXT += f"📍 **Support**: [Group](https://t.me/GalonSupport) | [Channel](https://t.me/GalonUpdates)"
    await text.delete()
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=TEXT)


@Client.on_message(filters.command(["repo", "repository"], HANDLER) & filters.me)
async def _ping(client, message):
    TEXT = "Hi, I'm Using 🔥 **Galon-Userbot** 🔥\n\n"
    TEXT += f"• Userbot Version: `{BOT_VER}`\n"
    TEXT += "• Updates Channel: [Galon Updates](https://t.me/GalonUpdates)\n"
    TEXT += "• Support Group: [Galon Support](https://t.me/GalonSupport)\n"
    TEXT += "• Owner Repo: [Galih](https://t.me/graphiert) & [Dion](https://t.me/xflzu)\n"
    TEXT += "• Link Repo: [Galon-Userbot](https://github.com/galihpujiirianto/Galon-Userbot)"
    await message.edit_text(TEXT, disable_web_page_preview=True)


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"ping": "Cek latensi dari userbot.",
        f"speedtest": "Cek kecepatan server userbot.",
        f"alive": "Cek bot hidup atau tidak.",
        f"repo": "Cek repository."
    }
})
