import time
from redis.commands.json.path import Path

from .. import db

# Satu data, isian memggunakan object (dictionary)
lihat = db.json().get("AFKTYPE", Path.root_path())
if not lihat:
    db.json().set("AFKTYPE", Path.root_path(), {})

# Banyak data, isian menggunakan array (list)
lagi = db.json().get("AFKMENTION", Path.root_path())
if not lagi:
    db.json().set("AFKMENTION", Path.root_path(), [])

data_reason = lambda text=None, media=None: {"text": text, "media": media}

def add_afk(data):
    store = {"data": data, "time": int(time.time())}
    db.json().set("AFKTYPE", Path.root_path(), store)

def is_afk():
    return db.json().get("AFKTYPE", Path.root_path())

def remove_afk():
    db.json().set("AFKTYPE", Path.root_path(), {})

def add_mention(nameuser, userid, group, link):
    isi = db.json().get("AFKMENTION", Path.root_path())
    data = {
        "nameuser": nameuser, "userid": userid,
        "group": group, "link": link
    }
    isi.append({"data": data, "time": time.time()})
    db.json().set("AFKMENTION", Path.root_path(), isi)

def search_remove_mention():
    isi = db.json().get("AFKMENTION", Path.root_path())
    db.json().set("AFKMENTION", Path.root_path(), [])
    return isi
