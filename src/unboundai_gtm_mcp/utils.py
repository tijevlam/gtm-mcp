import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from google.oauth2.credentials import Credentials
from google.auth.credentials import TokenState
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.auth


class GTMAuth:
    """Handle Google Tag Manager authentication and service creation."""

    def __init__(self, token_file: Path, service_name: str, version: str, scopes: List[str]) -> None:
        """
        Initialize GTM authentication handler.

        Args:
            token_file: Path to store OAuth token
            service_name: Google API service name (e.g., 'tagmanager')
            version: API version (e.g., 'v2')
            scopes: List of OAuth scopes required
        """
        self.token_file = token_file
        self.service_name = service_name
        self.version = version
        self.scopes = scopes
        self.credentials = None
        self.auth_method = os.getenv("GTM_AUTH_METHOD", "oauth").lower()

    def authenticate(self):
        """
        Authenticate with Google Tag Manager API and return service client.
        
        Supports two authentication methods:
        1. OAuth 2.0 (default): Uses GTM_CLIENT_ID, GTM_CLIENT_SECRET, GTM_PROJECT_ID
        2. Service Account: Uses GOOGLE_APPLICATION_CREDENTIALS

        Returns:
            Google API service client
        """
        if self.auth_method == "service_account":
            credentials = self._authenticate_service_account()
        elif self.auth_method == "oauth":
            credentials = self._authenticate_oauth()
        else:
            raise ValueError(
                f"Invalid GTM_AUTH_METHOD: '{self.auth_method}'. "
                f"Must be 'oauth' or 'service_account'"
            )

        self.credentials = credentials
        service = build(self.service_name, self.version, credentials=credentials)
        return service

    def _authenticate_service_account(self) -> google.auth.credentials.Credentials:
        """
        Authenticate using Application Default Credentials (ADC).
        
        ADC automatically discovers credentials from multiple sources:
        1. GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to a service account JSON file
        2. Google Cloud SDK credentials (gcloud auth application-default login)
        3. Service account attached to GCE/GKE/Cloud Run instances
        4. Other Google Cloud environments
        
        Returns:
            Application Default Credentials
        """
        try:
            credentials, project = google.auth.default(scopes=self.scopes)
            
            # Get credential source for logging
            cred_source = "Application Default Credentials"
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if credentials_path:
                cred_source = f"service account file: {credentials_path}"
            elif hasattr(credentials, '_service_account_email'):
                cred_source = "GCE/GKE/Cloud Run service account"
            elif hasattr(credentials, 'token'):
                cred_source = "gcloud CLI credentials"
            
            print(f"✓ Authenticated using {cred_source}")
            if project:
                print(f"✓ Project: {project}")
            
            return credentials
        except google.auth.exceptions.DefaultCredentialsError as e:
            raise ValueError(
                "Failed to load Application Default Credentials!\n\n"
                "When using GTM_AUTH_METHOD=service_account, credentials can be provided via:\n"
                "1. GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to a service account JSON file\n"
                "2. Google Cloud SDK: Run 'gcloud auth application-default login'\n"
                "3. Running on GCE/GKE/Cloud Run with attached service account\n\n"
                "For service account setup:\n"
                "1. Go to Google Cloud Console\n"
                "2. Create a new service account\n"
                "3. Download the JSON key file\n"
                "4. Grant the service account access to your GTM account\n"
                "5. Set GOOGLE_APPLICATION_CREDENTIALS to the file path\n\n"
                f"Error details: {e}\n\n"
                "See the README for detailed setup instructions."
            )
        except Exception as e:
            raise ValueError(
                f"Failed to authenticate with Application Default Credentials: {e}\n\n"
                f"Please ensure your credentials are properly configured."
            )

    def _authenticate_oauth(self) -> Credentials:
        """
        Authenticate using OAuth 2.0 flow.
        
        This is the original authentication method that requires
        GTM_CLIENT_ID, GTM_CLIENT_SECRET, and GTM_PROJECT_ID.
        
        Returns:
            OAuth credentials
        """
        credentials = None

        # Load existing token if available
        if self.token_file.exists():
            try:
                credentials = Credentials.from_authorized_user_file(
                    str(self.token_file), self.scopes
                )
            except Exception as e:
                print(f"Warning: Could not load token file: {e}")
                credentials = None

        # Refresh expired credentials or run OAuth flow
        if credentials and credentials.token_state != TokenState.FRESH and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                self.token_file.parent.mkdir(parents=True, exist_ok=True)
                self.token_file.write_text(credentials.to_json())
            except Exception as e:
                print(f"Warning: Could not refresh token: {e}")
                credentials = None

        # Run OAuth flow if no valid credentials
        if not credentials or not credentials.valid:
            client_config = self._get_client_config()
            flow = InstalledAppFlow.from_client_config(client_config, self.scopes)
            credentials = flow.run_local_server(port=0)

            # Save credentials for future use
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            self.token_file.write_text(credentials.to_json())
        
        print(f"✓ Authenticated using OAuth 2.0")
        return credentials

    def _get_client_config(self) -> Dict[str, Any]:
        """
        Get OAuth client configuration from environment variables.

        Users must set these environment variables:
        - GTM_CLIENT_ID: Your Google OAuth Client ID
        - GTM_CLIENT_SECRET: Your Google OAuth Client Secret
        - GTM_PROJECT_ID: Your Google Cloud Project ID

        See setup guide for instructions on creating these credentials.
        """
        client_id = os.getenv("GTM_CLIENT_ID")
        client_secret = os.getenv("GTM_CLIENT_SECRET")
        project_id = os.getenv("GTM_PROJECT_ID")

        if not client_id or not client_secret:
            raise ValueError(
                "Missing required OAuth credentials!\n\n"
                "Please set the following environment variables:\n"
                "  - GTM_CLIENT_ID\n"
                "  - GTM_CLIENT_SECRET\n"
                "  - GTM_PROJECT_ID (optional)\n\n"
                "See the setup guide for instructions:\n"
                "https://github.com/paolbtl/gtm-mcp/"
            )

        return {
            "installed": {
                "client_id": client_id,
                "project_id": project_id or "gtm-mcp",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"]
            }
        }


def _authenticate(token_file: Path, service_name: str, version: str, scopes: List[str]):
    """
    Helper function to authenticate with Google Tag Manager API.

    Args:
        token_file: Path to store OAuth token
        service_name: Google API service name
        version: API version
        scopes: List of OAuth scopes

    Returns:
        Google API service client
    """
    auth = GTMAuth(token_file, service_name, version, scopes)
    return auth.authenticate()
