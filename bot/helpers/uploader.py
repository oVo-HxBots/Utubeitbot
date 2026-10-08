import asyncio
import logging
import os
import random
from typing import Optional, Tuple

from ..config import Config
from ..youtube import GoogleAuth, YouTube

log = logging.getLogger(__name__)


class Uploader:
    def __init__(
        self,
        file: str,
        title: Optional[str] = None,
        user_id: Optional[int] = None,
    ):
        self.file = file
        self.title = title
        self.user_id = user_id
        self.video_category = {
            1: "Film & Animation",
            2: "Autos & Vehicles",
            10: "Music",
            15: "Pets & Animal",
            17: "Sports",
            19: "Travel & Events",
            20: "Gaming",
            22: "People & Blogs",
            23: "Comedy",
            24: "Entertainment",
            25: "News & Politics",
            26: "Howto & Style",
            27: "Education",
            28: "Science & Technology",
            29: "Nonprofits & Activism",
        }

    async def start(self, progress: callable = None, *args) -> Tuple[bool, str]:
        self.progress = progress
        self.args = args
        await self._upload()
        return self.status, self.message

    async def _upload(self) -> None:
        try:
            if not self.user_id:
                raise ValueError(
                    "Telegram user ID is required for YouTube upload."
                )

            loop = asyncio.get_running_loop()
            cred_file = Config.credential_file(self.user_id)

            auth = GoogleAuth(
                Config.CLIENT_ID,
                Config.CLIENT_SECRET,
                Config.OAUTH_REDIRECT_URI,
            )

            if not cred_file.is_file():
                self.status = False
                self.message = (
                    "Upload failed because you have not authenticated YouTube. "
                    "Use /login first."
                )
                return

            auth.LoadCredentialsFile(str(cred_file))
            google = await loop.run_in_executor(None, auth.authorize)

            if (
                Config.VIDEO_CATEGORY
                and Config.VIDEO_CATEGORY in self.video_category
            ):
                category_id = Config.VIDEO_CATEGORY
            else:
                category_id = random.choice(list(self.video_category))

            category_name = self.video_category[category_id]
            title = self.title if self.title else os.path.basename(self.file)
            title = (
                (
                    Config.VIDEO_TITLE_PREFIX
                    + title
                    + Config.VIDEO_TITLE_SUFFIX
                )
                .replace("<", "")
                .replace(">", "")[:100]
            )

            description = (
                Config.VIDEO_DESCRIPTION
                + "\nUploaded to YouTube with https://tx.me/Utubeitbot"
            )[:5000]

            privacy_status = Config.UPLOAD_MODE or "private"

            properties = {
                "title": title,
                "description": description,
                "category": category_id,
                "privacyStatus": privacy_status,
            }

            log.debug("YouTube upload payload for %s: %s", self.file, properties)

            youtube = YouTube(google)
            result = await loop.run_in_executor(
                None,
                youtube.upload_video,
                self.file,
                properties,
            )

            video_id = result["id"]
            self.status = True
            self.message = (
                f"Title: {title}\n"
                f"Link: https://youtu.be/{video_id}\n\n"
                f"Category ID: {category_name} | Category Code: {category_id}\n"
                "**@HxBots | [@oVo-HxBots](https://github.com/oVo-HxBots)**"
                "\n\n"
                "**Thanks For Using Our Bot. Use /upgrade To Upload Unlimited Videos.**"
            )
        except Exception as exc:
            log.error(exc, exc_info=True)
            self.status = False
            self.message = (
                "Error occurred during upload.\n"
                f"Error details: {exc}"
            )
