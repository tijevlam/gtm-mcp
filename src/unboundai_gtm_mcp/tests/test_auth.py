"""Unit tests for GTM authentication methods."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from unboundai_gtm_mcp.utils import GTMAuth


class TestGTMAuth:
    """Test GTMAuth class and authentication methods."""

    @pytest.fixture
    def mock_scopes(self):
        """Provide mock OAuth scopes."""
        return [
            "https://www.googleapis.com/auth/tagmanager.readonly",
            "https://www.googleapis.com/auth/tagmanager.edit.containers"
        ]

    @pytest.fixture
    def mock_token_file(self, tmp_path):
        """Provide a temporary token file path."""
        return tmp_path / "token.json"

    def test_init_default_oauth_method(self, mock_token_file, mock_scopes):
        """Test GTMAuth initialization defaults to OAuth method."""
        auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
        assert auth.auth_method == "oauth"
        assert auth.token_file == mock_token_file
        assert auth.service_name == "tagmanager"
        assert auth.version == "v2"
        assert auth.scopes == mock_scopes

    def test_init_service_account_method(self, mock_token_file, mock_scopes):
        """Test GTMAuth initialization with service account method."""
        with patch.dict(os.environ, {"GTM_AUTH_METHOD": "service_account"}):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            assert auth.auth_method == "service_account"

    def test_authenticate_invalid_method(self, mock_token_file, mock_scopes):
        """Test authenticate raises error for invalid method."""
        with patch.dict(os.environ, {"GTM_AUTH_METHOD": "invalid"}):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Invalid GTM_AUTH_METHOD"):
                auth.authenticate()

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    @patch('unboundai_gtm_mcp.utils.build')
    def test_authenticate_service_account_success(
        self, mock_build, mock_default_auth, mock_token_file, mock_scopes, tmp_path
    ):
        """Test successful service account authentication using ADC."""
        # Create a mock service account file (for GOOGLE_APPLICATION_CREDENTIALS)
        sa_file = tmp_path / "service-account.json"
        sa_file.write_text('{"type": "service_account"}')
        
        # Mock the credentials returned by google.auth.default
        mock_credentials = MagicMock()
        mock_project = "test-project"
        mock_default_auth.return_value = (mock_credentials, mock_project)
        
        # Mock the build function
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        with patch.dict(os.environ, {
            "GTM_AUTH_METHOD": "service_account",
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file)
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            service = auth.authenticate()
            
            # Verify google.auth.default was called with scopes
            mock_default_auth.assert_called_once_with(scopes=mock_scopes)
            
            # Verify the service was built
            mock_build.assert_called_once_with("tagmanager", "v2", credentials=mock_credentials)
            assert service == mock_service

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    def test_authenticate_service_account_missing_credentials(self, mock_default_auth, mock_token_file, mock_scopes):
        """Test service account auth fails when ADC cannot find credentials."""
        # Mock google.auth.default to raise DefaultCredentialsError
        import google.auth.exceptions
        mock_default_auth.side_effect = google.auth.exceptions.DefaultCredentialsError("Could not find credentials")
        
        with patch.dict(os.environ, {"GTM_AUTH_METHOD": "service_account"}, clear=True):
            if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Failed to load Application Default Credentials"):
                auth.authenticate()

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    def test_authenticate_service_account_gcloud_cli(self, mock_default_auth, mock_token_file, mock_scopes):
        """Test service account auth works with gcloud CLI credentials."""
        # Mock credentials from gcloud CLI (no GOOGLE_APPLICATION_CREDENTIALS set)
        mock_credentials = MagicMock()
        mock_credentials.token = "mock_token_from_gcloud"
        mock_project = "gcloud-project"
        mock_default_auth.return_value = (mock_credentials, mock_project)
        
        with patch.dict(os.environ, {"GTM_AUTH_METHOD": "service_account"}, clear=True):
            if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with patch('unboundai_gtm_mcp.utils.build') as mock_build:
                mock_build.return_value = MagicMock()
                service = auth.authenticate()
                
                # Verify google.auth.default was called
                mock_default_auth.assert_called_once_with(scopes=mock_scopes)
                # Verify service was created
                assert service is not None

    @patch('unboundai_gtm_mcp.utils.InstalledAppFlow.from_client_config')
    @patch('unboundai_gtm_mcp.utils.Credentials.from_authorized_user_file')
    @patch('unboundai_gtm_mcp.utils.build')
    def test_authenticate_oauth_existing_valid_token(
        self, mock_build, mock_creds_from_file, mock_flow_class, mock_token_file, mock_scopes
    ):
        """Test OAuth authentication with existing valid token."""
        # Create a mock token file
        mock_token_file.write_text('{"token": "mock_token"}')
        
        # Mock valid credentials
        mock_credentials = MagicMock()
        mock_credentials.valid = True
        mock_credentials.token_state = MagicMock()
        mock_credentials.to_json.return_value = '{"token": "mock_token"}'  # Fix: return string
        mock_creds_from_file.return_value = mock_credentials
        
        # Mock the build function
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Set OAuth credentials in environment
        with patch.dict(os.environ, {
            "GTM_AUTH_METHOD": "oauth",
            "GTM_CLIENT_ID": "test-client-id.apps.googleusercontent.com",
            "GTM_CLIENT_SECRET": "GOCSPX-test-secret",
            "GTM_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            service = auth.authenticate()
            
            # Verify credentials were loaded from file
            mock_creds_from_file.assert_called_once()
            
            # Verify service was built
            mock_build.assert_called_once_with("tagmanager", "v2", credentials=mock_credentials)
            assert service == mock_service
            
            # Verify flow was not called since we had valid credentials
            mock_flow_class.assert_not_called()

    def test_oauth_get_client_config_missing_credentials(self, mock_token_file, mock_scopes):
        """Test OAuth fails when client credentials are missing."""
        # Use empty strings instead of None to avoid TypeError
        with patch.dict(os.environ, {
            "GTM_AUTH_METHOD": "oauth"
        }, clear=True):
            # Ensure the OAuth env vars are not set
            for key in ["GTM_CLIENT_ID", "GTM_CLIENT_SECRET", "GTM_PROJECT_ID"]:
                os.environ.pop(key, None)
            
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Missing required OAuth credentials"):
                auth._get_client_config()

    def test_oauth_get_client_config_success(self, mock_token_file, mock_scopes):
        """Test OAuth client config is created correctly."""
        with patch.dict(os.environ, {
            "GTM_CLIENT_ID": "test-client-id.apps.googleusercontent.com",
            "GTM_CLIENT_SECRET": "GOCSPX-test-secret",
            "GTM_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            config = auth._get_client_config()
            
            assert "installed" in config
            assert config["installed"]["client_id"] == "test-client-id.apps.googleusercontent.com"
            assert config["installed"]["client_secret"] == "GOCSPX-test-secret"
            assert config["installed"]["project_id"] == "test-project"
            assert config["installed"]["auth_uri"] == "https://accounts.google.com/o/oauth2/auth"
            assert config["installed"]["token_uri"] == "https://oauth2.googleapis.com/token"


class TestAuthMethodSelection:
    """Test authentication method selection logic."""

    def test_default_to_oauth_when_env_not_set(self):
        """Test that OAuth is the default when GTM_AUTH_METHOD is not set."""
        with patch.dict(os.environ, {}, clear=True):
            if "GTM_AUTH_METHOD" in os.environ:
                del os.environ["GTM_AUTH_METHOD"]
            
            auth = GTMAuth(Path("/tmp/token.json"), "tagmanager", "v2", [])
            assert auth.auth_method == "oauth"

    def test_case_insensitive_method_name(self):
        """Test that method names are case-insensitive."""
        test_cases = [
            ("OAuth", "oauth"),
            ("OAUTH", "oauth"),
            ("Service_Account", "service_account"),
            ("SERVICE_ACCOUNT", "service_account")
        ]
        
        for input_method, expected_method in test_cases:
            with patch.dict(os.environ, {"GTM_AUTH_METHOD": input_method}):
                auth = GTMAuth(Path("/tmp/token.json"), "tagmanager", "v2", [])
                assert auth.auth_method == expected_method
