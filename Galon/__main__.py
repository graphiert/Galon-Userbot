from . import *
from pyrogram import idle

START_MSG = f"""
🔥 **GALON-USERBOT ONLINE!** 🔥

✥ `Galon-Userbot v{BOT_VER}`
✥ Ketik `{HANDLER}ping` untuk melihat informasi.

Ada permasalahan/error? Laporkan ke @GalonSupport!
"""


async def startgalon():
    await galon.start()
    await galon.join_chat("GalonUpdates")
    await galon.join_chat("GalonSupport")
    await galon.send_message(BOTLOG_CHATID, START_MSG)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    print(f"Galon-UserBot v{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    LOOP.run_until_complete(startgalon())
