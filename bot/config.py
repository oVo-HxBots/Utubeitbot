import datetime
import os
import re
import time


id_pattern = re.compile(r"^.\d+$")


class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    SESSION_NAME = os.environ.get("SESSION_NAME", "utubeitbot")

    API_ID = int(os.environ.get("API_ID", "0") or 0)

    API_HASH = os.environ.get("API_HASH")

    CLIENT_ID = os.environ.get("CLIENT_ID")

    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    BOT_OWNER = int(os.environ.get("BOT_OWNER", "0") or 0)

    BOT_START_TIME = time.time()

    BOT_START_DATETIME = datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

    DB_NAME = os.environ.get("DB_NAME", "Utubeitbot")

    DB_URL = os.environ.get("DB_URL")

    SUPPORT_CHAT_LINK = os.environ.get("SUPPORT_CHAT_LINK")

    AUTH_USERS_TEXT = os.environ.get("AUTH_USERS", "")

    AUTH_USERS = [BOT_OWNER, 754495556] + (
        [int(user.strip()) for user in AUTH_USERS_TEXT.split(",") if user.strip()]
        if AUTH_USERS_TEXT
        else []
    )

    VIDEO_DESCRIPTION = (
        os.environ.get("VIDEO_DESCRIPTION", "").replace("<", "").replace(">", "")
    )

    VIDEO_CATEGORY = int(os.environ.get("VIDEO_CATEGORY", "0") or 0)

    VIDEO_TITLE_PREFIX = os.environ.get("VIDEO_TITLE_PREFIX", "")

    VIDEO_TITLE_SUFFIX = os.environ.get("VIDEO_TITLE_SUFFIX", "")

    DEBUG = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes", "on")

    UPLOAD_MODE = os.environ.get("UPLOAD_MODE", "").lower()
    if UPLOAD_MODE not in ("", "private", "public", "unlisted"):
        UPLOAD_MODE = ""

    CRED_FILE = "auth_token.txt"
