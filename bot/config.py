import os


class Config:

    BOT_TOKEN = "1173368697:AAE4fVeu9iTqaE2EC72o_cLlzBVYdSs1CzQ"

    SESSION_NAME = os.environ.get("SESSION_NAME", "Utubeitbot")

    API_ID = "1144902"

    API_HASH = "e743e5a4f35076e4c558a4bd713082e9"

    CLIENT_ID = "61391530394-vp359e09g0begugu89i5r9majo05mduo.apps.googleusercontent.com"

    CLIENT_SECRET = "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"

    BOT_OWNER = "754495556"

    AUTH_USERS_TEXT = os.environ.get("AUTH_USERS", "")

    AUTH_USERS = [BOT_OWNER, 374321319] + (
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
