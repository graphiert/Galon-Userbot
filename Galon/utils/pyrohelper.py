from pyrogram import Client
from pyrogram.types import Message
from ..database.welcome import get_welcome
from .. import PM_AUTO_BAN
from ..database.pmpermit import approved_pm

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def welcome_chat(f, c: Client, m: Message):
    to_welcome = get_welcome(str(m.chat.id))
    if to_welcome:
        return True
    else:
        return False

def get_pmp(f, c: Client, m: Message):
    if not PM_AUTO_BAN:
        return False
    else:
        return True
