"""GTM MCP Server - Google Tag Manager Model Context Protocol Server.

This package provides a Model Context Protocol server for Google Tag Manager,
enabling AI assistants to manage GTM containers, tags, triggers, and variables.

Phase 1 Foundation Modules:
    - exceptions: Custom exception classes for GTM operations
    - constants: Type-safe enumerations for GTM entities
    - validators: Input validation functions
    - helpers: Utility functions for building GTM API structures
"""

__version__ = "0.0.1"

# Import commonly used items for convenience
from .exceptions import (
    GTMError,
    ValidationError,
    APIError,
    ResourceNotFoundError,
    PermissionError,
    ConfigurationError,
    ParameterFormatError,
)

from .constants import (
    TriggerType,
    TagType,
    VariableType,
    FilterType,
    ParameterType,
)

__all__ = [
    # Version
    "__version__",
    # Exceptions
    "GTMError",
    "ValidationError",
    "APIError",
    "ResourceNotFoundError",
    "PermissionError",
    "ConfigurationError",
    "ParameterFormatError",
    # Constants
    "TriggerType",
    "TagType",
    "VariableType",
    "FilterType",
    "ParameterType",
]
