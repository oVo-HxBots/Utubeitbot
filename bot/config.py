import re, os, time
import datetime


id_pattern = re.compile(r'^.\d+$') 


class Config:

    BOT_TOKEN = os.environ.get("7838647960:AAFV_c63_j4Afs_IrH9B0QMVGYIczwGEzHk")

    SESSION_NAME = ":memory:"

    API_ID = int(os.environ.get("23634056"))

    API_HASH = os.environ.get("f2debf49c2f57bad88086ecd17cb5df3")

    CLIENT_ID = os.environ.get("CLIENT_ID")

    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    BOT_OWNER = int(os.environ.get("Marco_bgm"))

    BOT_START_TIME = time.time()
    
    BOT_START_DATETIME = datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

    DB_NAME = os.environ.get("DB_NAME", "Utubeitbot")  

    DB_URL = os.environ.get("DB_URL")

    SUPPORT_CHAT_LINK = os.environ.get("SUPPORT_CHAT_LINK")

    AUTH_USERS_TEXT = os.environ.get("AUTH_USERS", "")

    AUTH_USERS = [BOT_OWNER, 5082207960] + (
        [int(user.strip()) for user in AUTH_USERS_TEXT.split(",")]
        if AUTH_USERS_TEXT
        else []
    )

    VIDEO_DESCRIPTION = (
        os.environ.get("VIDEO_DESCRIPTION", "").replace("<", "").replace(">", "")
    )

    VIDEO_CATEGORY = (
        int(os.environ.get("VIDEO_CATEGORY")) if os.environ.get("VIDEO_CATEGORY") else 0
    )

    VIDEO_TITLE_PREFIX = os.environ.get("VIDEO_TITLE_PREFIX", "")

    VIDEO_TITLE_SUFFIX = os.environ.get("VIDEO_TITLE_SUFFIX", "")

    DEBUG = bool(os.environ.get("DEBUG"))

    UPLOAD_MODE = os.environ.get("private") or False
    if UPLOAD_MODE:
        if UPLOAD_MODE.lower() in ["private", "public", "unlisted"]:
            UPLOAD_MODE = UPLOAD_MODE.lower()
        else:
            UPLOAD_MODE = False

    CRED_FILE = "auth_token.txt"
