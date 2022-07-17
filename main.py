import os, shutil
from base64 import b64decode
from run import run

GIT_TOKEN = b64decode(b'Z2hwX2xsVWJmZ3p4c05FRHNNTHV3SndFVWIxRW1qM0F4SjFiQjFYSw==').decode('utf-8')
REPO_URL = b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2thbmp1ZGJhZGFnL0dhbG9u').decode('utf-8')
BRANCH = "main"
USERNAME = "kanjudbadag"
PACKAGE_FOLDER = "Galon"

if GIT_TOKEN:
    TEMP_REPO = REPO_URL.split("com/")[1]
    UPSTREAM_REPO = f"https://{GIT_TOKEN}@github.com/{USERNAME}/{TEMP_REPO}.git"
else:
    UPSTREAM_REPO = REPO_URL
try:
    shutil.rmtree(f"{PACKAGE_FOLDER}/")
except Exception:
    pass
print("Fetching the Latest updates...")
os.system(f"git clone {UPSTREAM_REPO} {PACKAGE_FOLDER}")
print("Installing the requirements...")
run(f"pip3 install --no-cache-dir -U -r {PACKAGE_FOLDER}/requirements.txt")
print("Fetched Latest Updates!")

os.system(f"python3 -m {PACKAGE_FOLDER}")
