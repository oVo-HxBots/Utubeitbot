import json
import logging
import os
import secrets
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

log = logging.getLogger(__name__)


class AuthCodeInvalidError(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class NoCredentialFile(Exception):
    pass


class GoogleAuth:
    OAUTH_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

    # state -> (Telegram user id, OAuth Flow)
    _pending_flows: dict[str, tuple[int, Flow]] = {}

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        if not client_id or not client_secret:
            raise InvalidCredentials(
                "CLIENT_ID and CLIENT_SECRET must be configured."
            )
        if not redirect_uri:
            raise InvalidCredentials("OAUTH_REDIRECT_URI is not configured.")

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri.rstrip("/")
        self.credentials: Optional[Credentials] = None

    def _new_flow(self) -> Flow:
        return Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": self.AUTH_ENDPOINT,
                    "token_uri": self.TOKEN_ENDPOINT,
                    "redirect_uris": [self.redirect_uri],
                }
            },
            scopes=self.OAUTH_SCOPE,
        )

    def GetAuthUrl(self, telegram_user_id: int) -> str:
        flow = self._new_flow()
        flow.redirect_uri = self.redirect_uri

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            state=secrets.token_urlsafe(32),
        )
        self._pending_flows[state] = (int(telegram_user_id), flow)
        return authorization_url

    @classmethod
    def complete_callback(cls, code: str, state: str):
        item = cls._pending_flows.pop(state, None)
        if not item:
            raise AuthCodeInvalidError(
                "The authorization session is expired or invalid. "
                "Please run /login again."
            )

        telegram_user_id, flow = item
        try:
            flow.fetch_token(code=code)
        except Exception as exc:
            raise AuthCodeInvalidError(
                f"Google OAuth token exchange failed: {exc}"
            ) from exc

        credentials = flow.credentials
        if not credentials or not credentials.refresh_token:
            raise InvalidCredentials(
                "Google did not return a refresh token. Please run /login again."
            )

        return telegram_user_id, credentials

    def LoadCredentialsFile(self, cred_file: str) -> None:
        path = Path(cred_file)
        if not path.is_file():
            raise NoCredentialFile(f"No credential file named {cred_file} is found.")

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.credentials = Credentials.from_authorized_user_info(
                data, self.OAUTH_SCOPE
            )
        except Exception as exc:
            raise InvalidCredentials(
                f"Failed to load OAuth credentials from {cred_file}: {exc}"
            ) from exc

    def SaveCredentialsFile(self, cred_file: str) -> None:
        if self.credentials is None:
            raise InvalidCredentials("No OAuth credentials loaded.")

        path = Path(cred_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.credentials.to_json(), encoding="utf-8")

        try:
            os.chmod(path, 0o600)
        except OSError:
            pass

    def authorize(self):
        if not self.credentials:
            raise InvalidCredentials("No credentials loaded.")

        if self.credentials.expired:
            if not self.credentials.refresh_token:
                raise InvalidCredentials(
                    "OAuth credentials expired and no refresh token is available."
                )
            try:
                self.credentials.refresh(Request())
            except Exception as exc:
                raise InvalidCredentials(
                    f"Unable to refresh Google OAuth credentials: {exc}"
                ) from exc

        return build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            credentials=self.credentials,
            cache_discovery=False,
        )
