"""Unit tests for GTM exceptions module."""

import pytest

from gtm_mcp.exceptions import (
    APIError,
    ConfigurationError,
    GTMError,
    ParameterFormatError,
    PermissionError,
    ResourceNotFoundError,
    ValidationError,
)


class TestGTMError:
    """Test GTMError base exception."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = GTMError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}

    def test_error_with_details(self):
        """Test error with details dictionary."""
        details = {"key": "value", "count": 42}
        error = GTMError("Test error", details)
        assert error.message == "Test error"
        assert error.details == details
        assert "Details:" in str(error)
        assert "key" in str(error)

    def test_error_inheritance(self):
        """Test that GTMError inherits from Exception."""
        error = GTMError("Test")
        assert isinstance(error, Exception)


class TestValidationError:
    """Test ValidationError exception."""

    def test_basic_validation_error(self):
        """Test basic validation error."""
        error = ValidationError("Invalid value")
        assert error.message == "Invalid value"
        assert error.details == {}

    def test_validation_error_with_field(self):
        """Test validation error with field name."""
        error = ValidationError("Invalid value", field="account_id")
        assert error.details["field"] == "account_id"

    def test_validation_error_with_value(self):
        """Test validation error with value."""
        error = ValidationError("Invalid", field="id", value="abc123")
        assert error.details["field"] == "id"
        assert error.details["value"] == "abc123"

    def test_validation_error_with_expected(self):
        """Test validation error with expected value description."""
        error = ValidationError(
            "Invalid type",
            field="count",
            value="abc",
            expected="integer"
        )
        assert error.details["field"] == "count"
        assert error.details["value"] == "abc"
        assert error.details["expected"] == "integer"

    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from GTMError."""
        error = ValidationError("Test")
        assert isinstance(error, GTMError)
        assert isinstance(error, Exception)


class TestAPIError:
    """Test APIError exception."""

    def test_basic_api_error(self):
        """Test basic API error."""
        error = APIError("Request failed")
        assert error.message == "Request failed"
        assert error.status_code is None
        assert error.api_error is None

    def test_api_error_with_status_code(self):
        """Test API error with HTTP status code."""
        error = APIError("Not found", status_code=404)
        assert error.status_code == 404
        assert error.details["status_code"] == 404

    def test_api_error_with_api_exception(self):
        """Test API error with original exception."""
        original = ValueError("Original error")
        error = APIError("API failed", api_error=original)
        assert error.api_error == original
        assert "Original error" in error.details["api_error"]

    def test_api_error_complete(self):
        """Test API error with all parameters."""
        original = Exception("Google API error")
        error = APIError(
            "Request failed",
            status_code=500,
            api_error=original
        )
        assert error.message == "Request failed"
        assert error.status_code == 500
        assert error.api_error == original
        assert error.details["status_code"] == 500


class TestResourceNotFoundError:
    """Test ResourceNotFoundError exception."""

    def test_basic_resource_not_found(self):
        """Test basic resource not found error."""
        error = ResourceNotFoundError("tag", "12345")
        assert "Tag not found" in error.message
        assert error.details["resource_type"] == "tag"
        assert error.details["resource_id"] == "12345"

    def test_resource_not_found_with_parent(self):
        """Test resource not found with parent path."""
        error = ResourceNotFoundError(
            "variable",
            "67890",
            parent_path="accounts/123/containers/456/workspaces/1"
        )
        assert "Variable not found" in error.message
        assert error.details["resource_type"] == "variable"
        assert error.details["resource_id"] == "67890"
        assert "accounts/123" in error.details["parent_path"]

    def test_resource_type_capitalization(self):
        """Test that resource type is capitalized in message."""
        error = ResourceNotFoundError("trigger", "999")
        assert "Trigger not found" in error.message


class TestPermissionError:
    """Test PermissionError exception."""

    def test_basic_permission_error(self):
        """Test basic permission error."""
        error = PermissionError("Access denied")
        assert error.message == "Access denied"
        assert error.details == {}

    def test_permission_error_with_scope(self):
        """Test permission error with required scope."""
        error = PermissionError(
            "Insufficient permissions",
            required_scope="tagmanager.publish"
        )
        assert error.details["required_scope"] == "tagmanager.publish"

    def test_permission_error_with_resource_path(self):
        """Test permission error with resource path."""
        error = PermissionError(
            "Access denied",
            resource_path="accounts/123/containers/456"
        )
        assert error.details["resource_path"] == "accounts/123/containers/456"

    def test_permission_error_complete(self):
        """Test permission error with all parameters."""
        error = PermissionError(
            "Cannot publish",
            required_scope="tagmanager.publish",
            resource_path="accounts/123/containers/456/versions/7"
        )
        assert error.message == "Cannot publish"
        assert error.details["required_scope"] == "tagmanager.publish"
        assert "versions/7" in error.details["resource_path"]


class TestConfigurationError:
    """Test ConfigurationError exception."""

    def test_basic_configuration_error(self):
        """Test basic configuration error."""
        error = ConfigurationError("Invalid configuration")
        assert error.message == "Invalid configuration"
        assert error.details == {}

    def test_configuration_error_with_entity_type(self):
        """Test configuration error with entity type."""
        error = ConfigurationError(
            "Missing required field",
            entity_type="tag"
        )
        assert error.details["entity_type"] == "tag"

    def test_configuration_error_with_config_key(self):
        """Test configuration error with config key."""
        error = ConfigurationError(
            "Invalid value",
            entity_type="trigger",
            config_key="verticalScrollPercentageList"
        )
        assert error.details["entity_type"] == "trigger"
        assert error.details["config_key"] == "verticalScrollPercentageList"


class TestParameterFormatError:
    """Test ParameterFormatError exception."""

    def test_basic_parameter_format_error(self):
        """Test basic parameter format error."""
        error = ParameterFormatError("Invalid parameter structure")
        assert error.message == "Invalid parameter structure"
        assert error.details == {}

    def test_parameter_format_error_with_key(self):
        """Test parameter format error with parameter key."""
        error = ParameterFormatError(
            "Missing type field",
            parameter_key="eventParameters"
        )
        assert error.details["parameter_key"] == "eventParameters"

    def test_parameter_format_error_with_expected_structure(self):
        """Test parameter format error with expected structure."""
        error = ParameterFormatError(
            "Invalid list structure",
            parameter_key="verticalScrollPercentageList",
            expected_structure="{'type': 'LIST', 'list': [...]}"
        )
        assert error.details["parameter_key"] == "verticalScrollPercentageList"
        assert "LIST" in error.details["expected_structure"]
