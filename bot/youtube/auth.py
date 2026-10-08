import os
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


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

    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Initialize GoogleAuth with Service Account credentials.
        
        Service Account credentials are loaded from GOOGLE_APPLICATION_CREDENTIALS
        environment variable.
        """
        self.credentials: Optional[Credentials] = None
        self._load_service_account()

    def _load_service_account(self) -> None:
        """
        Load service account credentials from GOOGLE_APPLICATION_CREDENTIALS env var.
        """
        cred_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_file or not os.path.isfile(cred_file):
            raise InvalidCredentials(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set or file not found. "
                "Please set it to your service account JSON key file path."
            )

        try:
            self.credentials = Credentials.from_service_account_file(
                cred_file, scopes=self.OAUTH_SCOPE
            )
        except Exception as e:
            raise InvalidCredentials(
                f"Failed to load service account credentials from {cred_file}: {e}"
            )

    def GetAuthUrl(self) -> str:
        """
        Service Account doesn't need user authorization.
        Returns a status message instead.
        """
        if self.credentials:
            service_account_email = self.credentials.service_account_email
            return f"Service Account authenticated: {service_account_email}. No user authorization needed."
        raise InvalidCredentials("Service Account credentials not loaded.")

    def Auth(self, code: str = None) -> None:
        """
        For Service Account, credentials are already loaded in __init__.
        This method is kept for backward compatibility but is a no-op.
        """
        if not self.credentials:
            self._load_service_account()

    def authorize(self):
        """
        Build and return the YouTube API client.
        """
        if not self.credentials:
            self._load_service_account()

        # Refresh if expired
        if self.credentials.expired:
            self.credentials.refresh(Request())

        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=self.credentials)

    def LoadCredentialsFile(self, cred_file: str) -> None:
        """
        Load credentials from a service account JSON file.
        """
        if not os.path.isfile(cred_file):
            raise NoCredentialFile(f"No credential file named {cred_file} is found.")

        try:
            self.credentials = Credentials.from_service_account_file(
                cred_file, scopes=self.OAUTH_SCOPE
            )
        except Exception as e:
            raise InvalidCredentials(f"Failed to load credentials from {cred_file}: {e}")

    def SaveCredentialsFile(self, cred_file: str) -> None:
        """
        Service Account credentials are read-only from the key file.
        This is a no-op for service accounts.
        """
        if self.credentials is None:
            raise InvalidCredentials("No credentials loaded.")

        # Service Account credentials come from the key file and are not saved elsewhere
        service_account_email = self.credentials.service_account_email
        print(f"Service Account in use: {service_account_email}")
