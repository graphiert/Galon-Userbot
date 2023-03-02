import dotenv, sys, logging, asyncio
from os import getenv
from requests import get
from pytgcalls import GroupCallFactory
from aiohttp import ClientSession
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from redis import StrictRedis

dotenv.load_dotenv()

LOOP = asyncio.get_event_loop()

aiosession = ClientSession()
DEVS = get("https://raw.githubusercontent.com/SeorangDion/Cool/dion/DEVS.json").json()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("galon.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


API_ID = getenv("API_ID", 19359139)
API_HASH = getenv("API_HASH", "1a4dd1b55d9369d172944d2028feaa2a")
SESSION_STRING = getenv("SESSION_STRING")
SESSION_STRING2 = getenv("SESSION_STRING2")
SESSION_STRING3 = getenv("SESSION_STRING3")
SESSION_STRING4 = getenv("SESSION_STRING4")
SESSION_STRING5 = getenv("SESSION_STRING5")
BOTLOG_CHATID = getenv("BOTLOG_CHATID")
HANDLER = getenv("HANDLER", ".")
ALIVE_PIC = getenv("ALIVE_PIC", "https://telegra.ph/file/ed6745ac6d7513a0eb7e4.jpg")
ALIVE_TEXT = getenv("ALIVE_TEXT", "Hey, I'm Using Galon-Userbot!")
REDIS_URI = getenv("REDIS_URI")
REDIS_PASSWORD = getenv("REDIS_PASSWORD")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
PM_AUTO_BAN = getenv("PM_AUTO_BAN", False)
PM_LIMIT = int(getenv("PM_LIMIT", 5))
BOT_VER = "main@1.1.3"


if not API_ID:
    print('API_ID tidak ada! Harap masukkan API_ID! Keluar...')
    sys.exit(1)
else:
    try:
        API_ID = int(getenv("API_ID"))
    except TypeError:
        print("API_ID hanya boleh berisi angka! Harap cek terlebih dahulu. Keluar...")
        sys.exit(1)

if not API_HASH:
    print('API_HASH tidak ada! Harap masukkan API_HASH! Keluar...')
    sys.exit(1)

if not SESSION_STRING:
    print('SESSION_STRING tidak ada! Harap masukkan SESSION_STRING! Keluar...')
    sys.exit(1)

if not BOTLOG_CHATID:
    BOTLOG_CHATID = "me"
else:
    BOTLOG_CHATID = int(BOTLOG_CHATID)

if not REDIS_URI and not REDIS_PASSWORD:
    print('REDIS_URI dan/atau REDIS_PASSWORD tidak ada! Keluar...')
    sys.exit(1)

db = StrictRedis.from_url(f"redis://default:{REDIS_PASSWORD}@{REDIS_URI}")

try:
    db.ping()
    print("Redis sudah online!")
except:
    print("Redis tidak berjalan. Pastikan kamu mengisi var REDIS_URI dan REDIS_PASSWORD dengan benar!")
    sys.exit(1)


if SESSION_STRING:
    galon = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        session_name=SESSION_STRING,
        plugins={"root": "Galon.plugins"}
    )
    group_call = GroupCallFactory(galon).get_group_call()
else:
    galon = None


if SESSION_STRING2:
    galon2 = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        session_name=SESSION_STRING2,
        plugins={"root": "Galon.plugins"}
    )
    galon2.start()
    galon2.join_chat("GalonUpdates")
    galon2.join_chat("GalonSupport")
    group_call2 = GroupCallFactory(galon2).get_group_call()
else:
    galon2 = None


if SESSION_STRING3:
    galon3 = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        session_name=SESSION_STRING3,
        plugins={"root": "Galon.plugins"}
    )
    galon3.start()
    galon3.join_chat("GalonUpdates")
    galon3.join_chat("GalonSupport")
    group_call3 = GroupCallFactory(galon3).get_group_call()
else:
    galon3 = None


if SESSION_STRING4:
    galon4 = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        session_name=SESSION_STRING4,
        plugins={"root": "Galon.plugins"}
    )
    galon4.start()
    galon4.join_chat("GalonUpdates")
    galon4.join_chat("GalonSupport")
    group_call4 = GroupCallFactory(galon4).get_group_call()
else:
    galon4 = None


if SESSION_STRING5:
    galon5 = Client(
        api_id=API_ID,
        api_hash=API_HASH,
        session_name=SESSION_STRING5,
        plugins={"root": "Galon.plugins"}
    )
    galon5.start()
    galon5.join_chat("GalonUpdates")
    galon5.join_chat("GalonSupport")
    group_call5 = GroupCallFactory(galon5).get_group_call()
else:
    galon5 = None
