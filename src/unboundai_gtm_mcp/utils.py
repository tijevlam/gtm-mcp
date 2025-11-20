import os
from pathlib import Path
from typing import List
from googleapiclient.discovery import build
import google.auth


class GTMAuth:
    """Handle Google Tag Manager authentication and service creation using Application Default Credentials."""

    def __init__(self, token_file: Path, service_name: str, version: str, scopes: List[str]) -> None:
        """
        Initialize GTM authentication handler.

        Args:
            token_file: Path to store OAuth token (unused but kept for backward compatibility)
            service_name: Google API service name (e.g., 'tagmanager')
            version: API version (e.g., 'v2')
            scopes: List of OAuth scopes required
        """
        self.token_file = token_file
        self.service_name = service_name
        self.version = version
        self.scopes = scopes
        self.credentials = None

    def authenticate(self):
        """
        Authenticate with Google Tag Manager API using Application Default Credentials.
        
        Requires the following environment variables to be set:
        - GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON file
        - GOOGLE_PROJECT_ID: Google Cloud Project ID

        Returns:
            Google API service client
        """
        credentials = self._create_credentials()
        self.credentials = credentials
        service = build(self.service_name, self.version, credentials=credentials)
        return service

    def _create_credentials(self) -> google.auth.credentials.Credentials:
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
        # Check for required environment variables
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("GOOGLE_PROJECT_ID")
        
        if not credentials_path:
            raise ValueError(
                "Missing required environment variable: GOOGLE_APPLICATION_CREDENTIALS\n\n"
                "Please set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account JSON file.\n\n"
                "Example MCP configuration:\n"
                '{\n'
                '  "mcpServers": {\n'
                '    "gtm-mcp": {\n'
                '      "command": "gtm-mcp",\n'
                '      "env": {\n'
                '        "GOOGLE_APPLICATION_CREDENTIALS": "PATH_TO_CREDENTIALS_JSON",\n'
                '        "GOOGLE_PROJECT_ID": "YOUR_PROJECT_ID"\n'
                '      }\n'
                '    }\n'
                '  }\n'
                '}\n\n'
                "See the README for detailed setup instructions."
            )
        
        if not project_id:
            raise ValueError(
                "Missing required environment variable: GOOGLE_PROJECT_ID\n\n"
                "Please set GOOGLE_PROJECT_ID to your Google Cloud Project ID.\n\n"
                "Example MCP configuration:\n"
                '{\n'
                '  "mcpServers": {\n'
                '    "gtm-mcp": {\n'
                '      "command": "gtm-mcp",\n'
                '      "env": {\n'
                '        "GOOGLE_APPLICATION_CREDENTIALS": "PATH_TO_CREDENTIALS_JSON",\n'
                '        "GOOGLE_PROJECT_ID": "YOUR_PROJECT_ID"\n'
                '      }\n'
                '    }\n'
                '  }\n'
                '}\n\n'
                "See the README for detailed setup instructions."
            )
        
        try:
            credentials, project = google.auth.default(scopes=self.scopes)
            
            print(f"✓ Authenticated using Application Default Credentials")
            print(f"✓ Credentials file: {credentials_path}")
            print(f"✓ Project ID: {project_id}")
            
            return credentials
        except google.auth.exceptions.DefaultCredentialsError as e:
            raise ValueError(
                "Failed to load Application Default Credentials!\n\n"
                "Please ensure:\n"
                "1. GOOGLE_APPLICATION_CREDENTIALS points to a valid service account JSON file\n"
                "2. The file exists and is readable\n"
                "3. The JSON file contains valid credentials\n\n"
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
