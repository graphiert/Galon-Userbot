from .help import HELP_CMD
import os
from asyncio import sleep
from pyrogram import Client, filters
from .. import HANDLER
from ..utils.basic import eor


@Client.on_message(filters.me & filters.command("invite", HANDLER))
async def inviteee(client, message):
    mg = await eor(message, "`Adding Users!`")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("`Give Me Users To Add! Check Help Menu For More Info!`")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"`Unable To Add Users! \nTraceBack : {e}`")
        return
    await mg.edit(f"`Sucessfully Added {len(user_list)} To This Group / Channel!`")


@Client.on_message(filters.command(["inviteall"], HANDLER) & filters.me)
async def inv(client, message):
    a = await eor(message, "Gime Title also\n ex: .inviteall @UsernameGC")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await a.edit_text(f"inviting users from {chat.username}")
    async for member in client.iter_chat_members(chat.id):
        user = member.user
        zxb = ["online", "offline", "recently", "within_week"]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
                mg = await client.send_message("me", f"error-   {e}")
                await sleep(0.3)
                await mg.delete()


@Client.on_message(filters.command("invitelink", HANDLER) & filters.me)
async def invite_link(client, message):
    a = await eor(message, "`Processing...`")
    if message.chat.type in ["group", "supergroup"]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await a.edit(f"Link Invite: {link}")
        except Exception:
            await a.edit("Denied permission")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "invitelink": "Untuk Mendapatkan Link invite ke grup Obrolan Anda. [Need Admin]",
    "invite @username": "Untuk Mengundang Anggota ke grup Anda.",
    "inviteall @usernamegc": "Untuk Mengundang Anggota dari obrolan grup lain ke obrolan grup Anda.",
    "note": "Akunmu mungkin akan terkena limitasi atau sebagainya, maka dari itu, gunakan module ini sebijak mungkin!"
}})
