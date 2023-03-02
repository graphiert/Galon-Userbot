from redis.commands.json.path import Path

from .. import db

lihat = db.json().get("PMPERMIT", Path.root_path())
if not lihat:
  db.json().set("PMPERMIT", Path.root_path(), [])

def approved_pm(id):
  return True if id in db.json().get("PMPERMIT", Path.root_path()) else False

def approve_pm(id):
  cek = db.json().get("PMPERMIT", Path.root_path())
  if id not in cek:
    cek.append(id)
    db.json().set("PMPERMIT", Path.root_path(), cek)

def reject_pm(id):
  see = db.json().get("PMPERMIT", Path.root_path())
  if id in see:
    see.remove(id)
  db.json().set("PMPERMIT", Path.root_path(), see)
