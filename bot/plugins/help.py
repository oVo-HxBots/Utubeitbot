import json
import os
from typing import Optional
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class AuthCodeInvalidError(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class NoCredentialFile(Exception):
    pass


class GoogleAuth:
    OAUTH_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
    REDIRECT_URI = "http://localhost"
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials: Optional[Credentials] = None

    def GetAuthUrl(self) -> str:
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [self.REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                }
            },
            scopes=self.OAUTH_SCOPE,
        )
        auth_url, _ = flow.authorization_url(prompt="consent")
        return auth_url

    def Auth(self, code: str) -> None:
        try:
            if not code:
                raise AuthCodeInvalidError("No authorization code provided.")

            parsed = urlparse(code)
            if parsed.scheme and parsed.netloc:
                params = parse_qs(parsed.query)
                code = params.get("code", [None])[0]

            if not code:
                raise AuthCodeInvalidError("No authorization code found in the supplied URL or string.")

            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uris": [self.REDIRECT_URI],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    }
                },
                scopes=self.OAUTH_SCOPE,
            )
            self.credentials = flow.fetch_token(code=code, redirect_uri=self.REDIRECT_URI)
        except Exception:
            raise

    def authorize(self):
        if not self.credentials:
            raise InvalidCredentials("No credentials!")

        creds = Credentials.from_authorized_user_info(self.credentials, self.OAUTH_SCOPE)
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise InvalidCredentials("Credentials are invalid or expired.")
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)

    def LoadCredentialsFile(self, cred_file: str) -> None:
        if not os.path.isfile(cred_file):
            raise NoCredentialFile(f"No credential file named {cred_file} is found.")

        with open(cred_file, "r", encoding="utf-8") as stream:
            data = json.load(stream)

        self.credentials = data

    def SaveCredentialsFile(self, cred_file: str) -> None:
        if self.credentials is None:
            raise InvalidCredentials("No credentials to save.")

        with open(cred_file, "w", encoding="utf-8") as stream:
            json.dump(self.credentials, stream)
