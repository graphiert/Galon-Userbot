import os, subprocess
from base64 import b64decode
GIT_TOKEN = os.environ.get(
    "GIT_TOKEN",
    b64decode(b'Z2hwX2xsVWJmZ3p4c05FRHNNTHV3SndFVWIxRW1qM0F4SjFiQjFYSw==').decode('utf-8')
)
REPO_URL = os.environ.get(
    "REPO_URL",
    b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2thbmp1ZGJhZGFnL0dhbG9u').decode('utf-8')
)
PACKAGE_FOLDER = "Galon"
if GIT_TOKEN:
    TEMP_REPO = REPO_URL.split("https://")[1]
    UPSTREAM_REPO = f"https://{GIT_TOKEN}@{TEMP_REPO}.git"
else:
    UPSTREAM_REPO = REPO_URL
try:
    subprocess.Popen(f"rm -rf {PACKAGE_FOLDER}/")
except Exception:
    pass
ready_to_exc = f"git clone {UPSTREAM_REPO} {PACKAGE_FOLDER} && "
ready_to_exc += f"pip3 install --no-cache-dir -U -r {PACKAGE_FOLDER}/requirements.txt"
print("Fetching the Latest updates and installing the requirements...")
run = subprocess.call(ready_to_exc, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print("Fetched the updates and starting the bot...")
subprocess.Popen(f"python3 -m {PACKAGE_FOLDER}", shell=True)
