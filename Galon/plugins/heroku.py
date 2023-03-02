import requests, os, asyncio, dotenv
import math, socket, heroku3

from pyrogram.types import Message
from pyrogram import Client, filters
from .. import galon, HANDLER, HEROKU_API_KEY, HEROKU_APP_NAME, DEVS
from .. import BOTLOG_CHATID as LOG

from .help import HELP_CMD
from ..utils.basic import eor

heroku_api = "https://api.heroku.com"
useragent = (
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.149 Mobile Safari/537.36"
)

Hero = heroku3.from_key(HEROKU_API_KEY)
Heroku = Hero.app(HEROKU_APP_NAME)

async def is_heroku():
    return "heroku" in socket.getfqdn()


@Client.on_message(filters.group & filters.command("restart",
                  "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("restart", HANDLER) & filters.me)
async def restart(client, message: Message):
    if (HEROKU_API_KEY or HEROKU_APP_NAME) is None:
        await eor(
            message, "Tolong tambahkan `HEROKU_APP_NAME` dan `HEROKU_API_KEY` di **Config Vars** heroku anda!"
        )
        return
    heroku = Hero.apps()[HEROKU_APP_NAME]
    await eor(message, "**Berhasil di restart!**")
    await asyncio.sleep(0.5)
    await client.send_message(LOG, f"**LOGGER**: #RESTART | #HEROKU\n\n**Merestart** `{HEROKU_APP_NAME}` **di heroku!**")
    heroku.restart()
    return


@Client.on_message(filters.command(["dyno", "usage"], HANDLER) & filters.me)
async def dyno(client, message: Message):
    txt = await eor(message, "`Processing...`")

    u_id = Hero.account().id
    if HEROKU_API_KEY is not None:
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {HEROKU_API_KEY}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }

        path = "/accounts/" + u_id + "/actions/get-quota"
        req = requests.get(heroku_api + path, headers=headers)
        if req.status_code != 200:
            await txt.edit("**Error:**\n\n" f">.`{r.reason}`\n")
        result = req.json()
        quota = result["account_quota"]
        quota_used = result["quota_used"]

        """ - Used - """
        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        hours = math.floor(minutes_remaining / 60)
        day = math.floor(hours / 24)

        """ - Current - """
        App = result["apps"]
        try:
            App[0]["quota_used"]
        except IndexError:
            AppQuotaUsed = 0
            AppPercentage = 0
        else:
            AppQuotaUsed = App[0]["quota_used"] / 60
            AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        await asyncio.sleep(2)

        teks = f"""
• **Informasi Dyno Heroku :**

-> **Penggunaan Dyno** `{HEROKU_APP_NAME}` :
     •  `{AppHours}`**Jam**  `{AppMinutes}`**Menit |**  [`{AppPercentage}`**%**]
-> **Sisa kuota dyno bulan ini** :
     •  `{hours}`**Jam**  `{minutes}`**Menit |**  [`{percentage}`**%**]

• **Sisa Dyno Heroku** `{day}` **Hari Lagi**"""
        await txt.edit(teks)


@Client.on_message(filters.group & filters.command("setvar",
                                                  "?") & filters.user(DEVS) & ~filters.me)
@galon.on_message(filters.command(["setvar", "set_var"], HANDLER) & filters.me)
async def set_var(client, message: Message):
    if len(message.command) < 3:
        return await eor(
            message, f"<b>Usage:</b> {HANDLER}setvar [Var Name] [Var Value]"
        )
    msg = await eor(message, "`Processing...`")
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if Heroku is None:
            return await msg.edit(
                "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
            )
        heroku_config = Heroku.config()
        if to_set in heroku_config:
            await msg.edit(f"Berhasil Mengubah var {to_set} menjadi {value}! Heroku akan direstart untuk melakukan ini, mohon tunggu sebentar...")
            await asyncio.sleep(0.5)
            await client.send_message(
                LOG, f"**LOGGER**: #SETVAR | #HEROKU\n\n**Mengubah var** `{to_set}` **menjadi** `{value}`", disable_web_page_preview=True)
        else:
            await msg.edit(f"Berhasil Menambahkan var {to_set} menjadi {value}")
            await asyncio.sleep(0.5)
            await client.send_message(
                LOG, f"**LOGGER**: #SETVAR | #HEROKU\n\n**Menambahkan var** `{to_set}` **dengan value** `{value}`", disable_web_page_preview=True)
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv("config.env")
        if not path:
            return await msg.edit(".env file not found.")
        dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            await msg.edit(f"Berhasil Mengubah var {to_set} menjadi {value}")
        else:
            await msg.edit(f"Berhasil Menambahkan var {to_set} menjadi {value}")
        os.system(f"kill -9 {os.getpid()} && python3 -m Galon")


@galon.on_message(filters.command(["delvar", "del_var"], HANDLER) & filters.me)
async def del_var(client, message: Message):
    if len(message.command) != 2:
        return await eor(message, f"<b>Usage:</b> {HANDLER}delvar [Var Name]")
    txt = await eor(message, "`Processing...`")
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if Heroku is None:
            return await txt.edit(
                "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
            )
        heroku_config = Heroku.config()
        if check_var in heroku_config:
            await message.edit(f"Berhasil Menghapus var {check_var}")
            await asyncio.sleep(0.5)
            await client.send_message(LOG, f"**LOGGER**: #DELVAR | #HEROKU\n\nMenghapus variable {check_var}")
            del heroku_config[check_var]
        else:
            return await message.edit(f"Tidak dapat menemukan var {check_var}")
    else:
        path = dotenv.find_dotenv("config.env")
        if not path:
            return await message.edit(".env file not found.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.edit(f"Tidak dapat menemukan var {check_var}")
        else:
            await message.edit(f"Berhasil Menghapus var {check_var}")
            os.system(f"kill -9 {os.getpid()} && python3 -m Galon")


@galon.on_message(filters.command(["getvar", "get_var"], HANDLER) & filters.me)
async def get_var(client, message: Message):
    var_name = message.text.split(None, 2)[1]
    if len(message.command) != 2:
        return await eor(message, f"**Penggunaan**: {HANDLER}getvar [nama var]"
        )
    teks = await eor(message, "`Processing...`")
    if await is_heroku():
        if Heroku is None:
            return await teks.edit(
                "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
            )
        heroku_config = Heroku.config()
        if var_name in heroku_config:
            return await teks.edit(
                f"**Heroku Config Vars:**\n\n**{var_name}**: `{heroku_config[var_name]}`"
            )
        else:
            return await teks.edit(f"Tidak dapat menemukan var {var_name}")
    else:
        path = dotenv.find_dotenv("config.env")
        if not path:
            return await teks.edit(".env file not found.")
        output = dotenv.get_key(path, var_name)
        if not output:
            await teks.edit(f"Tidak dapat menemukan var {var_name}")
        else:
            return await teks.edit(f"**{var_name}**: `{str(output)}`")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"setvar [Nama Var] [Isi Var]": "Menambahkan config vars di heroku.",
        f"delvar [Nama Var]": "Menghapus variable dari heroku.",
        f"getvar [Nama Var]": "Mengecek value dari variable tersebut.",
        f"dyno": "Mengecek dyno heroku.",
        f"restart": "Merestart ulang app heroku.",
        "note": "Untuk dapat menggunakan command ini, kamu harus menambahkan HEROKU_API_KEY & HEROKU_APP_NAME di config vars anda!"
    }
})
