from redis.commands.json.path import Path

from .. import db as filters


lihat = filters.json().get("FILTERS", Path.root_path())
if not lihat:
    filters.json().set("FILTERS", Path.root_path(), [])

def add_filters(keyword, chat_id, message_id) -> None:
    fetch = filters.json().get("FILTERS", Path.root_path())
    fetch.append({"keyword": keyword, "chat_id": chat_id, "msg_id": message_id})
    filters.json().set("FILTERS", Path.root_path(), fetch)


def del_filters(keyword, chat_id):
    fetch = filters.json().get("FILTERS", Path.root_path())
    i = 0
    for fe in fetch:
        if fe["keyword"] == keyword and fe["chat_id"] == chat_id:
            del fetch[i]
        i += 1
    filters.json().set("FILTERS", Path.root_path(), fetch)


def filters_info(keyword, chat_id):
    fetch = filters.json().get("FILTERS", Path.root_path())
    ini = {}
    for fe in fetch:
        if fe["keyword"] == keyword and fe["chat_id"] == chat_id:
            ini.update(fe)
    if ini != {}:
        return ini
    else:
        return False


def filters_del(chat_id):
    fetch = filters.json().get("FILTERS", Path.root_path())
    for i in range(len(fetch)):
        if fetch[i]["chat_id"] == chat_id:
            del fetch[i]
    filters.json().set("FILTERS", Path.root_path(), fetch)
            

def all_filters(chat_id):
    fetch = filters.json().get("FILTERS", Path.root_path())
    all = []
    if len(fetch) != 0:
        for fe in fetch:
            if fe["chat_id"] == chat_id:
                all.append(fe)
    if len(all) > 0:
        return all
    else:
        return False
