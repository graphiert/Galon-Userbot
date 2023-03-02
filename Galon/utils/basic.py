from pyrogram.types import Message


async def eor(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text if bool(
            message.from_user and message.from_user.is_self or message.outgoing) else (
            message.reply_to_message or message).reply_text)
    return await apa(*args, **kwargs)


def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None
