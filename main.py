from base64 import b64decode
import os
import asyncio
import shlex
import shutil
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

GIT_TOKEN = b64decode(b'Z2hwX2xsVWJmZ3p4c05FRHNNTHV3SndFVWIxRW1qM0F4SjFiQjFYSw==').decode('utf-8')
REPO_URL = "https://github.com/kanjudbadag/Galon"
BRANCH = "main"
PACKAGE_FOLDER = "Galon"

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


if GIT_TOKEN:
    TEMP_REPO = REPO_URL.split("com/")[1]
    UPSTREAM_REPO = f"https://{GIT_TOKEN}:x-oauth-basic@github.com/{TEMP_REPO}"
else:
    UPSTREAM_REPO = REPO_URL
try:
    shutil.rmtree(f"{PACKAGE_FOLDER}/")
except Exception:
    pass
print("Fetching the Latest update...")
Repo.clone_from(UPSTREAM_REPO, PACKAGE_FOLDER)
print("Installing the requirements...")
install_req(f"pip3 install --no-cache-dir -U -r {PACKAGE_FOLDER}/requirements.txt")
print("Fetched Latest Updates!")

os.system(f"python3 -m {PACKAGE_FOLDER}")
