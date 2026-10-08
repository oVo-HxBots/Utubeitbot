import json
import os
from typing import Optional

from google.auth import default
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
        Initialize GoogleAuth with Service Account or OAuth credentials.
        
        If GOOGLE_APPLICATION_CREDENTIALS env var is set, uses Service Account.
        Otherwise, falls back to client_id/client_secret (for backward compatibility).
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials: Optional[Credentials] = None
        self.use_service_account = False

    def GetAuthUrl(self) -> str:
        """
        For Service Account, this returns a message since no user auth is needed.
        For OAuth, this would return the authorization URL.
        """
        if self.use_service_account:
            return "Service Account authenticated. No user authorization needed."
        
        # Fallback to OAuth flow (not implemented for this version)
        raise InvalidCredentials(
            "Service Account credentials not found. "
            "Please set GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )

    def Auth(self, code: str = None) -> None:
        """
        For Service Account, this loads credentials from the JSON key file.
        The 'code' parameter is ignored for Service Account auth.
        """
        try:
            cred_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            if not cred_file or not os.path.isfile(cred_file):
                raise NoCredentialFile(
                    "GOOGLE_APPLICATION_CREDENTIALS environment variable not set or file not found."
                )

            self.credentials = Credentials.from_service_account_file(
                cred_file, scopes=self.OAUTH_SCOPE
            )
            self.use_service_account = True
        except Exception as e:
            raise AuthCodeInvalidError(f"Failed to authenticate with service account: {e}")

    def authorize(self):
        """
        Build and return the YouTube API client.
        """
        if not self.credentials:
            raise InvalidCredentials("No credentials loaded. Call Auth() first.")

        if not self.credentials.valid:
            if self.credentials.expired:
                self.credentials.refresh(Request())

        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=self.credentials)

    def LoadCredentialsFile(self, cred_file: str) -> None:
        """
        Load credentials from a JSON file (Service Account format).
        """
        if not os.path.isfile(cred_file):
            raise NoCredentialFile(f"No credential file named {cred_file} is found.")

        try:
            self.credentials = Credentials.from_service_account_file(
                cred_file, scopes=self.OAUTH_SCOPE
            )
            self.use_service_account = True
        except Exception as e:
            raise InvalidCredentials(f"Failed to load credentials from {cred_file}: {e}")

    def SaveCredentialsFile(self, cred_file: str) -> None:
        """
        For Service Account, credentials are saved to the environment variable path.
        This method is a no-op for service accounts but kept for backward compatibility.
        """
        if self.credentials is None:
            raise InvalidCredentials("No credentials to save.")

        # Service Account credentials are typically not saved; they come from the key file
        # If you need to save them, you would serialize the service account JSON
        # For now, just confirm they exist
        if hasattr(self.credentials, 'service_account_email'):
            print(f"Using service account: {self.credentials.service_account_email}")
        else:
            raise InvalidCredentials("Credentials are not in Service Account format.")
