from redis.commands.json.path import Path

from .. import db as collection

lihat = collection.json().get("WELCOME", Path.root_path())
if not lihat:
    collection.json().set("WELCOME", Path.root_path(), [])

def save_welcome(chat_id, msg_id):
    doc = {chat_id: msg_id}
    result = collection.json().get("WELCOME", Path.root_path())
    for i in range(len(result)):
        for k in result[i]:
            if k == chat_id:
                del result[i]
    result.append(doc)
    collection.json().set("WELCOME", Path.root_path(), result)


def get_welcome(chat_id):
    result = collection.json().get("WELCOME", Path.root_path())
    for d in result:
        for k in d:
            if k == chat_id:
                return d[k]
    return None


def clear_welcome(chat_id):
    cek = collection.json().get("WELCOME", Path.root_path())
    for i in range(len(cek)):
        for k in cek[i]:
            if k == chat_id:
                del cek[i]
    collection.json().get("WELCOME", Path.root_path(), cek)
