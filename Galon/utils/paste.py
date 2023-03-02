import aiohttp

URL = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def paste(content: str):
    resp = await post(f"{URL}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return URL + resp["message"]
