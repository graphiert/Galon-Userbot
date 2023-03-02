import requests
from bs4 import BeautifulSoup as bs


def revimg(dl):
    file = {"encoded_image": (dl, open(dl, "rb"))}
    response = requests.get(
        requests.post(
            "https://www.google.com/searchbyimage/upload", files=file, allow_redirects=False
        ).headers.get("Location"),
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        },
    )
    alls = bs(response.text, "html.parser").find_all(
        "div", {"class": "r5a77d"})[0].find("a")
    text = alls.text
    return text
