from .help import HELP_CMD
import os
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, Message
from .. import HANDLER, DEVS
from ..utils.basic import eor
from ..utils.misc import extract_user, extract_user_and_reason, list_admins

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(filters.group &
                  filters.command(["setchatphoto", "setgpic"], HANDLER) & filters.me)
async def set_chat_photo(client: Client, message: Message):
    chat_id = message.chat.id
    b = await client.get_chat_member(chat_id, "me")
    can_change_admin = b.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("You don't have enough permission")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                chat_id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo to set it !")


@Client.on_message(filters.group & filters.command("ban", "?")
                  & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group &
                  filters.command("ban", HANDLER) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    bot = await client.get_chat_member(message.chat.id, (me.id))
    if not bot.can_restrict_members:
        return await a.edit("I don't have enough permissions")
    if not user_id:
        return await a.edit("I can't find that user.")
    if user_id == me.id:
        return await a.edit("I can't ban myself.")
    if user_id in DEVS:
        return await a.edit("I can't ban my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await a.edit("I can't ban an admin, You know the rules, so do i.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await a.edit(msg)


@Client.on_message(filters.group & filters.command("unban", "?")
                  & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group &
                  filters.command("unban", HANDLER) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_restrict_members:
        return await a.edit("I don't have enough permissions")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await a.edit("You cannot unban a channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await a.edit(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    mntn = await client.get_users(user)
    umention = mntn.mention
    await a.edit(f"Unbanned! {umention}")


@Client.on_message(filters.group & filters.command(
    ["pin", "unpin"], "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["pin", "unpin"], HANDLER) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await eor(message, "Reply to a message to pin/unpin it.")
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_pin_messages:
        return await a.edit("I don't have enough permissions")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await a.edit(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await a.edit(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.group & filters.command("mute", "?")
                  & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("mute", HANDLER) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    admin_list = await list_admins(client, message.chat.id)
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_restrict_members:
        return await a.edit("I don't have enough permissions")
    if not user_id:
        return await a.edit("I can't find that user.")
    if user_id == me.id:
        return await a.edit("I can't mute myself.")
    if user_id in DEVS:
        return await a.edit("I can't mute my developer!")
    if user_id in admin_list:
        return await a.edit("I can't mute an admin, You know the rules, so do i.")
    ment = await client.get_users(user_id)
    mention = ment.mention
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await a.edit(msg)


@Client.on_message(filters.group & filters.command("unmute",
                  "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group &
                  filters.command("unmute", HANDLER) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_restrict_members:
        return await a.edit("I don't have enough permissions")
    if not user_id:
        return await a.edit("I can't find that user.")
    await message.chat.unban_member(user_id)
    tion = await client.get_users(user_id)
    umention = tion.mention
    await a.edit(f"Unmuted! {umention}")


@Client.on_message(filters.group & filters.command(
    ["kick", "dkick"], "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["kick", "dkick"], HANDLER) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    a = await eor(message, "`Processing...`")
    me = await client.get_me()
    admin_list = await list_admins(client, message.chat.id)
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_restrict_members:
        return await a.edit("I don't have enough permissions")
    if not user_id:
        return await a.edit("I can't find that user.")
    if user_id == me.id:
        return await a.edit("I can't kick myself.")
    if user_id == DEVS:
        return await a.edit("I can't kick my developer.")
    if user_id in admin_list:
        return await a.edit("I can't kick an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await a.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await a.edit("**Maaf Anda Bukan admin**")


@Client.on_message(filters.group & filters.command(
    ["promote", "fullpromote"], "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group &
                  filters.command(["promote", "fullpromote"], HANDLER) & filters.me)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    a = await eor(message, "`Processing...`")
    if not user_id:
        return await a.edit("I can't find that user.")
    me = await client.get_me()
    bot = await client.get_chat_member(message.chat.id, me.id)
    if not bot.can_promote_members:
        return await a.edit("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
        return await a.edit(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    await a.edit(f"Promoted! {umention}")


@Client.on_message(filters.group & filters.command("demote",
                  "?") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group &
                  filters.command("demote", HANDLER) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    me = await client.get_me()
    a = await eor(message, "`Processing...`")
    if not user_id:
        return await a.edit("I can't find that user.")
    if user_id == me.id:
        return await a.edit("I can't demote myself.")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await client.get_users(user_id)).mention
    await a.edit(f"Demoted! {umention}")


PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({PLUGIN_NAME: {
    "ban [reply/username/userid] [alasan]": "Membanned member dari grup.",
    "unban [reply/username/userid] [alasan]": "Membuka banned member dari grup.",
    "kick [reply/username/userid]": "Mengeluarkan pengguna dari grup.",
    "promote": "Mempromosikan member sebagai admin .",
    "fullpromote": "Mempromosikan member sebagai cofounder.",
    "demote": "Menurunkan admin sebagai member.",
    "mute [reply/username/userid]": "Membisukan member dari Grup.",
    "unmute [reply/username/userid]": "Membuka mute member dari Grup.",
    "pin [reply]": "Untuk menyematkan pesan dalam grup.",
    "unpin [reply]": "Untuk melepaskan pin pesan dalam grup.",
    "setgpic [reply ke foto]": "Untuk mengubah foto profil grup"
}})
