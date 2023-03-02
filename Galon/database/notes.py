from redis.commands.json.path import Path

from .. import db as collection

lihat = collection.json().get("NOTES", Path.root_path())
if not lihat:
    collection.json().set("NOTES", Path.root_path(), [])

def save_note(note_name, note_id):
    doc = {note_name: note_id}
    result = collection.json().get("NOTES", Path.root_path())
    result.append(doc)
    collection.json().set("NOTES", Path.root_path(), result)

def get_note(note_name):
    result = collection.json().get("NOTES", Path.root_path())
    if len(result) > 0:
        for x in result:
            for y in x:
                if y == note_name:
                    return x[y]
        return None
    else:
        return None


def rm_note(note_name):
    cek = collection.json().get("NOTES", Path.root_path())
    for i in range(len(cek)):
        for j in cek[i]:
            if j == note_name:
                del cek[i]
    collection.json().set("NOTES", Path.root_path(), cek)


def get_all_notes():
    results = collection.json().get("NOTES", Path.root_path())
    ini = []
    for x in results:
        for y in x:
            ini.append(y)
    return ini


def rm_all():
    collection.json().set("NOTES", Path.root_path(), [])
