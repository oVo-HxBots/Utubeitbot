import re, os, time
import datetime

class Config:

    id_pattern = re.compile(r'^.\d+$') 

    BOT_TOKEN = "6898058070:AAEcx42alujShS2LaVA4F5EJjHmNbHlsH84"

    SESSION_NAME = ":memory:"

    BOT_START_TIME = time.time()
    
    BOT_START_DATETIME = datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

    API_ID = 924859

    API_HASH = "a4c9a18cf4d8cb24062ff6916597f832"

    CLIENT_ID = "84741382606-nl17sl25k800vj27vil35a27f85sq8bb.apps.googleusercontent.com"

    CLIENT_SECRET = "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"

    DOWNLOAD_DIRECTORY = "./downloads/"

    DB_NAME = "utubeitbot"    

    DB_URL = "mongodb+srv://user:user@cluster0.x3e1p.mongodb.net"

    BOT_OWNER = 754495556

    BOT_UPTIME  = time.time()

    SUPPORT_CHAT_LINK = "https://t.me/hxsupport"

    FORCE_SUB = "HxBots"

    AUTH_USERS_TEXT = os.environ.get("AUTH_USERS", "")

    AUTH_USERS = [BOT_OWNER, 754495556] + (
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

    UPLOAD_MODE = os.environ.get("UPLOAD_MODE") or False
    if UPLOAD_MODE:
        if UPLOAD_MODE.lower() in ["private", "public", "unlisted"]:
            UPLOAD_MODE = UPLOAD_MODE.lower()
        else:
            UPLOAD_MODE = False

    CRED_FILE = "auth_token.txt"
