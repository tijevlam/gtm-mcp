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

    def test_init(self, mock_token_file, mock_scopes):
        """Test GTMAuth initialization."""
        auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
        assert auth.token_file == mock_token_file
        assert auth.service_name == "tagmanager"
        assert auth.version == "v2"
        assert auth.scopes == mock_scopes

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    @patch('unboundai_gtm_mcp.utils.build')
    def test_authenticate_success(
        self, mock_build, mock_default_auth, mock_token_file, mock_scopes, tmp_path
    ):
        """Test successful authentication using ADC."""
        # Create a mock service account file
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
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file),
            "GOOGLE_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            service = auth.authenticate()
            
            # Verify google.auth.default was called with scopes
            mock_default_auth.assert_called_once_with(scopes=mock_scopes)
            
            # Verify the service was built
            mock_build.assert_called_once_with("tagmanager", "v2", credentials=mock_credentials)
            assert service == mock_service

    def test_authenticate_missing_credentials_env_var(self, mock_token_file, mock_scopes):
        """Test authentication fails when GOOGLE_APPLICATION_CREDENTIALS is not set."""
        with patch.dict(os.environ, {
            "GOOGLE_PROJECT_ID": "test-project"
        }, clear=True):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Missing required environment variable: GOOGLE_APPLICATION_CREDENTIALS"):
                auth.authenticate()

    def test_authenticate_missing_project_id(self, mock_token_file, mock_scopes, tmp_path):
        """Test authentication fails when GOOGLE_PROJECT_ID is not set."""
        sa_file = tmp_path / "service-account.json"
        sa_file.write_text('{"type": "service_account"}')
        
        with patch.dict(os.environ, {
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file)
        }, clear=True):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Missing required environment variable: GOOGLE_PROJECT_ID"):
                auth.authenticate()

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    def test_authenticate_default_credentials_error(self, mock_default_auth, mock_token_file, mock_scopes, tmp_path):
        """Test authentication fails when google.auth.default raises DefaultCredentialsError."""
        sa_file = tmp_path / "service-account.json"
        sa_file.write_text('{"type": "service_account"}')
        
        # Mock google.auth.default to raise DefaultCredentialsError
        import google.auth.exceptions
        mock_default_auth.side_effect = google.auth.exceptions.DefaultCredentialsError("Could not find credentials")
        
        with patch.dict(os.environ, {
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file),
            "GOOGLE_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Failed to load Application Default Credentials"):
                auth.authenticate()

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    def test_authenticate_generic_error(self, mock_default_auth, mock_token_file, mock_scopes, tmp_path):
        """Test authentication fails gracefully on generic error."""
        sa_file = tmp_path / "service-account.json"
        sa_file.write_text('{"type": "service_account"}')
        
        # Mock google.auth.default to raise a generic exception
        mock_default_auth.side_effect = Exception("Some unexpected error")
        
        with patch.dict(os.environ, {
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file),
            "GOOGLE_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            with pytest.raises(ValueError, match="Failed to authenticate with Application Default Credentials"):
                auth.authenticate()

    @patch('unboundai_gtm_mcp.utils.google.auth.default')
    @patch('unboundai_gtm_mcp.utils.build')
    def test_create_credentials(self, mock_build, mock_default_auth, mock_token_file, mock_scopes, tmp_path):
        """Test _create_credentials method."""
        sa_file = tmp_path / "service-account.json"
        sa_file.write_text('{"type": "service_account"}')
        
        mock_credentials = MagicMock()
        mock_project = "test-project"
        mock_default_auth.return_value = (mock_credentials, mock_project)
        
        with patch.dict(os.environ, {
            "GOOGLE_APPLICATION_CREDENTIALS": str(sa_file),
            "GOOGLE_PROJECT_ID": "test-project"
        }):
            auth = GTMAuth(mock_token_file, "tagmanager", "v2", mock_scopes)
            credentials = auth._create_credentials()
            
            # Verify google.auth.default was called with scopes
            mock_default_auth.assert_called_once_with(scopes=mock_scopes)
            assert credentials == mock_credentials
