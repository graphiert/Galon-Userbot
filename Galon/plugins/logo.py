import os, asyncio
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import HANDLER, aiosession
from ..utils.basic import eor
from .help import HELP_CMD


# Thank's to TechZBots for this API
LOGO_API1 = "https://techzbotsapi.herokuapp.com/logo?text="
LOGO_API2 = "https://techzbotsapi.herokuapp.com/logo?square=true&text="


async def generate_logo(text: str, square: Optional[bool] = False ):
  try:
    square = str(square).capitalize()
  
    if square == "True":
      url = LOGO_API2 + text
    else:
      url = LOGO_API1 + text
  
    resp = await aiosession.get(url)  
    img_url = resp.url
  except Exception as err:
    return "ERROR:\n" + str(err)
      
  return str(img_url)


@Client.on_message(filters.command("logo", HANDLER) & filters.me)
async def _logo(client: Client, message: Message):
    msg = await eor(message, "`Processing...`")
    text = message.text.split(maxsplit=1)[1]
    if not text:
        await msg.edit("**Berikan text untuk membuat logo!**")
        await asyncio.sleep(4)
        return
    owner = await client.get_me()
    logo = await generate_logo(text) 
    await client.send_photo(message.chat.id, logo, caption=f"**Logo By** [{owner.first_name}](tg://user?id=owner.id)")
    await msg.delete()



PLUGIN_NAME = os.path.basename(__file__.replace(".py", ""))
HELP_CMD.update({
    PLUGIN_NAME: {
        f"logo [text]": "Membuat sebuah logo."
    }
})
