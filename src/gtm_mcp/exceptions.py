"""Custom exceptions for GTM MCP server.

This module provides specialized exception classes for handling GTM API-specific
errors and validation failures with clear error messages.
"""

from typing import Any, Dict, Optional


class GTMError(Exception):
    """Base exception for all GTM-related errors.

    Attributes:
        message: Human-readable error description
        details: Optional dictionary containing additional context
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize GTM error.

        Args:
            message: Error description
            details: Optional additional context about the error
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of error."""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ValidationError(GTMError):
    """Raised when input validation fails.

    Examples:
        - Invalid parameter types or values
        - Missing required fields
        - Invalid ID formats
        - Out of range values
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = None,
        expected: Optional[str] = None
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error description
            field: Name of the field that failed validation
            value: The invalid value provided
            expected: Description of expected value format/type
        """
        details: Dict[str, Any] = {}
        if field is not None:
            details["field"] = field
        if value is not None:
            details["value"] = value
        if expected is not None:
            details["expected"] = expected

        super().__init__(message, details)


class APIError(GTMError):
    """Raised when GTM API request fails.

    Attributes:
        status_code: HTTP status code from the API
        api_error: Original error from Google API
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        api_error: Optional[Any] = None
    ) -> None:
        """Initialize API error.

        Args:
            message: Error description
            status_code: HTTP status code if available
            api_error: Original exception from Google API client
        """
        details: Dict[str, Any] = {}
        if status_code is not None:
            details["status_code"] = status_code
        if api_error is not None:
            details["api_error"] = str(api_error)

        super().__init__(message, details)
        self.status_code = status_code
        self.api_error = api_error


class ResourceNotFoundError(GTMError):
    """Raised when a GTM resource cannot be found.

    Examples:
        - Container not found
        - Workspace not found
        - Tag/Trigger/Variable not found
    """

    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        parent_path: Optional[str] = None
    ) -> None:
        """Initialize resource not found error.

        Args:
            resource_type: Type of resource (e.g., 'tag', 'trigger', 'variable')
            resource_id: ID of the missing resource
            parent_path: Optional path to parent container/workspace
        """
        message = f"{resource_type.title()} not found: {resource_id}"
        details: Dict[str, Any] = {
            "resource_type": resource_type,
            "resource_id": resource_id
        }
        if parent_path:
            details["parent_path"] = parent_path

        super().__init__(message, details)


class PermissionError(GTMError):
    """Raised when access to a resource is denied.

    Examples:
        - Insufficient OAuth scopes
        - Account restriction violations
        - Missing container permissions
    """

    def __init__(
        self,
        message: str,
        required_scope: Optional[str] = None,
        resource_path: Optional[str] = None
    ) -> None:
        """Initialize permission error.

        Args:
            message: Error description
            required_scope: OAuth scope required for the operation
            resource_path: Path to the restricted resource
        """
        details: Dict[str, Any] = {}
        if required_scope:
            details["required_scope"] = required_scope
        if resource_path:
            details["resource_path"] = resource_path

        super().__init__(message, details)


class ConfigurationError(GTMError):
    """Raised when GTM entity configuration is invalid.

    Examples:
        - Invalid trigger configuration
        - Malformed tag parameters
        - Invalid variable type
    """

    def __init__(
        self,
        message: str,
        entity_type: Optional[str] = None,
        config_key: Optional[str] = None
    ) -> None:
        """Initialize configuration error.

        Args:
            message: Error description
            entity_type: Type of GTM entity (tag, trigger, variable)
            config_key: Specific configuration key that's invalid
        """
        details: Dict[str, Any] = {}
        if entity_type:
            details["entity_type"] = entity_type
        if config_key:
            details["config_key"] = config_key

        super().__init__(message, details)


class ParameterFormatError(GTMError):
    """Raised when GTM parameter structure is invalid.

    The GTM API has specific requirements for parameter formatting
    (nested type/key/value structures). This error indicates the
    parameter structure doesn't match API expectations.
    """

    def __init__(
        self,
        message: str,
        parameter_key: Optional[str] = None,
        expected_structure: Optional[str] = None
    ) -> None:
        """Initialize parameter format error.

        Args:
            message: Error description
            parameter_key: Name of the parameter with formatting issues
            expected_structure: Description of expected parameter structure
        """
        details: Dict[str, Any] = {}
        if parameter_key:
            details["parameter_key"] = parameter_key
        if expected_structure:
            details["expected_structure"] = expected_structure

        super().__init__(message, details)
