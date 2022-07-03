from base64 import b64decode
import os
import asyncio
import shlex
import shutil
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

GIT_TOKEN = b64decode(b'Z2hwX2JnOG9Gb3FpdHd1dEhJdmphZVVXbHhFQ1RqOGdCMzNrRFNxMw==').decode('utf-8')
REPO_URL = "https://github.com/kanjudbadag/Galon"
BRANCH = "main"

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


def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        TEMP_REPO = REPO_LINK.split("com/")[1]
        UPSTREAM_REPO = f"https://{GIT_TOKEN}:x-oauth-basic@github.com/{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL
    try:
        shutil.rmtree("Galon/")
    except Exception:
        pass
    repo = Repo.clone_from(UPSTREAM_REPO)
    install_req("pip3 install --no-cache-dir -U -r Galon/requirements.txt")
    print("Fetched Latest Updates!")

git()
os.system("python3 -m Galon")
