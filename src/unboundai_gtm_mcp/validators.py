"""Input validation functions for GTM MCP server.

This module provides comprehensive validation for GTM API inputs including
IDs, names, paths, and configuration values with clear error messages.
"""

import re
from typing import Any, Dict, List, Optional, Union

from .constants import (
    GA4_EVENT_NAME_MAX_LENGTH,
    GA4_PARAMETER_NAME_MAX_LENGTH,
    GTM_NAME_MAX_LENGTH,
    GTM_NOTES_MAX_LENGTH,
    SCROLL_PERCENTAGES,
    FilterType,
    ParameterType,
    TagType,
    TriggerType,
    VariableType,
)
from .exceptions import ValidationError


def validate_account_id(account_id: str) -> str:
    """Validate GTM account ID format.

    Args:
        account_id: Account ID to validate

    Returns:
        The validated account ID

    Raises:
        ValidationError: If account ID is invalid
    """
    if not account_id:
        raise ValidationError("Account ID cannot be empty", field="account_id")

    if not account_id.isdigit():
        raise ValidationError(
            "Account ID must contain only digits",
            field="account_id",
            value=account_id,
            expected="numeric string"
        )

    if len(account_id) < 10:
        raise ValidationError(
            "Account ID must be at least 10 digits",
            field="account_id",
            value=account_id
        )

    return account_id


def validate_container_id(container_id: str) -> str:
    """Validate GTM container ID format.

    Args:
        container_id: Container ID to validate

    Returns:
        The validated container ID

    Raises:
        ValidationError: If container ID is invalid
    """
    if not container_id:
        raise ValidationError("Container ID cannot be empty", field="container_id")

    if not container_id.isdigit():
        raise ValidationError(
            "Container ID must contain only digits",
            field="container_id",
            value=container_id,
            expected="numeric string"
        )

    return container_id


def validate_workspace_id(workspace_id: str) -> str:
    """Validate GTM workspace ID format.

    Args:
        workspace_id: Workspace ID to validate

    Returns:
        The validated workspace ID

    Raises:
        ValidationError: If workspace ID is invalid
    """
    if not workspace_id:
        raise ValidationError("Workspace ID cannot be empty", field="workspace_id")

    if not workspace_id.isdigit():
        raise ValidationError(
            "Workspace ID must contain only digits",
            field="workspace_id",
            value=workspace_id,
            expected="numeric string"
        )

    return workspace_id


def validate_gtm_path(
    path: str,
    expected_type: Optional[str] = None
) -> str:
    """Validate GTM resource path format.

    Args:
        path: GTM resource path (e.g., 'accounts/123/containers/456')
        expected_type: Optional type to validate (e.g., 'container', 'workspace')

    Returns:
        The validated path

    Raises:
        ValidationError: If path format is invalid
    """
    if not path:
        raise ValidationError("Path cannot be empty", field="path")

    # Path should start with 'accounts/'
    if not path.startswith("accounts/"):
        raise ValidationError(
            "Path must start with 'accounts/'",
            field="path",
            value=path,
            expected="accounts/{accountId}/..."
        )

    parts = path.split("/")
    if len(parts) < 2:
        raise ValidationError(
            "Invalid path format",
            field="path",
            value=path,
            expected="accounts/{accountId}/..."
        )

    # Validate account ID part
    if not parts[1].isdigit():
        raise ValidationError(
            "Account ID in path must be numeric",
            field="path",
            value=path
        )

    # Validate expected type if provided
    if expected_type:
        if expected_type not in path:
            raise ValidationError(
                f"Path does not contain expected type '{expected_type}'",
                field="path",
                value=path,
                expected=f"path containing '/{expected_type}s/'"
            )

    return path


def validate_name(
    name: str,
    field_name: str = "name",
    max_length: int = GTM_NAME_MAX_LENGTH
) -> str:
    """Validate entity name.

    Args:
        name: Name to validate
        field_name: Name of the field being validated
        max_length: Maximum allowed length

    Returns:
        The validated name

    Raises:
        ValidationError: If name is invalid
    """
    if not name:
        raise ValidationError(
            f"{field_name.capitalize()} cannot be empty",
            field=field_name
        )

    if not isinstance(name, str):
        raise ValidationError(
            f"{field_name.capitalize()} must be a string",
            field=field_name,
            value=type(name).__name__,
            expected="string"
        )

    if len(name) > max_length:
        raise ValidationError(
            f"{field_name.capitalize()} exceeds maximum length of {max_length}",
            field=field_name,
            value=f"{len(name)} characters",
            expected=f"<= {max_length} characters"
        )

    return name.strip()


def validate_notes(notes: str) -> str:
    """Validate notes/description field.

    Args:
        notes: Notes text to validate

    Returns:
        The validated notes

    Raises:
        ValidationError: If notes are invalid
    """
    if not isinstance(notes, str):
        raise ValidationError(
            "Notes must be a string",
            field="notes",
            value=type(notes).__name__,
            expected="string"
        )

    if len(notes) > GTM_NOTES_MAX_LENGTH:
        raise ValidationError(
            f"Notes exceed maximum length of {GTM_NOTES_MAX_LENGTH}",
            field="notes",
            value=f"{len(notes)} characters",
            expected=f"<= {GTM_NOTES_MAX_LENGTH} characters"
        )

    return notes


def validate_trigger_type(trigger_type: str) -> str:
    """Validate trigger type.

    Args:
        trigger_type: Trigger type to validate

    Returns:
        The validated trigger type

    Raises:
        ValidationError: If trigger type is invalid
    """
    try:
        TriggerType(trigger_type)
        return trigger_type
    except ValueError:
        valid_types = [t.value for t in TriggerType]
        raise ValidationError(
            f"Invalid trigger type: {trigger_type}",
            field="trigger_type",
            value=trigger_type,
            expected=f"one of {valid_types}"
        )


def validate_tag_type(tag_type: str) -> str:
    """Validate tag type.

    Args:
        tag_type: Tag type to validate

    Returns:
        The validated tag type

    Raises:
        ValidationError: If tag type is invalid

    Note:
        This is a lenient validation since GTM supports many tag types
        including custom templates. We only validate known types.
    """
    if not tag_type:
        raise ValidationError("Tag type cannot be empty", field="tag_type")

    if not isinstance(tag_type, str):
        raise ValidationError(
            "Tag type must be a string",
            field="tag_type",
            value=type(tag_type).__name__,
            expected="string"
        )

    return tag_type


def validate_variable_type(variable_type: str) -> str:
    """Validate variable type.

    Args:
        variable_type: Variable type to validate

    Returns:
        The validated variable type

    Raises:
        ValidationError: If variable type is invalid

    Note:
        This is a lenient validation since GTM supports custom variable types.
    """
    if not variable_type:
        raise ValidationError("Variable type cannot be empty", field="variable_type")

    if not isinstance(variable_type, str):
        raise ValidationError(
            "Variable type must be a string",
            field="variable_type",
            value=type(variable_type).__name__,
            expected="string"
        )

    return variable_type


def validate_scroll_percentages(percentages: List[int]) -> List[int]:
    """Validate scroll depth percentages.

    Args:
        percentages: List of scroll depth percentages

    Returns:
        The validated and sorted percentages

    Raises:
        ValidationError: If percentages are invalid
    """
    if not percentages:
        raise ValidationError(
            "Scroll percentages cannot be empty",
            field="percentages"
        )

    if not isinstance(percentages, list):
        raise ValidationError(
            "Scroll percentages must be a list",
            field="percentages",
            value=type(percentages).__name__,
            expected="list of integers"
        )

    for i, pct in enumerate(percentages):
        if not isinstance(pct, int):
            raise ValidationError(
                f"Percentage at index {i} must be an integer",
                field="percentages",
                value=type(pct).__name__,
                expected="integer"
            )

        if pct < 0 or pct > 100:
            raise ValidationError(
                f"Percentage at index {i} must be between 0 and 100",
                field="percentages",
                value=pct,
                expected="0-100"
            )

    # Remove duplicates and sort
    return sorted(set(percentages))


def validate_ga4_event_name(event_name: str) -> str:
    """Validate GA4 event name.

    Args:
        event_name: Event name to validate

    Returns:
        The validated event name

    Raises:
        ValidationError: If event name is invalid

    References:
        https://support.google.com/analytics/answer/9267735
    """
    if not event_name:
        raise ValidationError("Event name cannot be empty", field="event_name")

    if len(event_name) > GA4_EVENT_NAME_MAX_LENGTH:
        raise ValidationError(
            f"Event name exceeds maximum length of {GA4_EVENT_NAME_MAX_LENGTH}",
            field="event_name",
            value=f"{len(event_name)} characters",
            expected=f"<= {GA4_EVENT_NAME_MAX_LENGTH} characters"
        )

    # GA4 event names must start with a letter
    if not event_name[0].isalpha():
        raise ValidationError(
            "Event name must start with a letter",
            field="event_name",
            value=event_name,
            expected="starts with a letter"
        )

    # GA4 event names can only contain letters, numbers, and underscores
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', event_name):
        raise ValidationError(
            "Event name can only contain letters, numbers, and underscores",
            field="event_name",
            value=event_name,
            expected="alphanumeric with underscores"
        )

    return event_name


def validate_ga4_parameter_name(param_name: str) -> str:
    """Validate GA4 event parameter name.

    Args:
        param_name: Parameter name to validate

    Returns:
        The validated parameter name

    Raises:
        ValidationError: If parameter name is invalid
    """
    if not param_name:
        raise ValidationError("Parameter name cannot be empty", field="parameter_name")

    if len(param_name) > GA4_PARAMETER_NAME_MAX_LENGTH:
        raise ValidationError(
            f"Parameter name exceeds maximum length of {GA4_PARAMETER_NAME_MAX_LENGTH}",
            field="parameter_name",
            value=f"{len(param_name)} characters",
            expected=f"<= {GA4_PARAMETER_NAME_MAX_LENGTH} characters"
        )

    # GA4 parameter names must start with a letter
    if not param_name[0].isalpha():
        raise ValidationError(
            "Parameter name must start with a letter",
            field="parameter_name",
            value=param_name,
            expected="starts with a letter"
        )

    # GA4 parameter names can only contain letters, numbers, and underscores
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', param_name):
        raise ValidationError(
            "Parameter name can only contain letters, numbers, and underscores",
            field="parameter_name",
            value=param_name,
            expected="alphanumeric with underscores"
        )

    return param_name


def validate_event_parameters(
    parameters: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Validate GA4 event parameters list.

    Args:
        parameters: List of parameter dictionaries with 'name' and 'value' keys

    Returns:
        The validated parameters

    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(parameters, list):
        raise ValidationError(
            "Event parameters must be a list",
            field="parameters",
            value=type(parameters).__name__,
            expected="list of dictionaries"
        )

    for i, param in enumerate(parameters):
        if not isinstance(param, dict):
            raise ValidationError(
                f"Parameter at index {i} must be a dictionary",
                field="parameters",
                value=type(param).__name__,
                expected="dictionary"
            )

        if "name" not in param:
            raise ValidationError(
                f"Parameter at index {i} missing 'name' key",
                field="parameters"
            )

        if "value" not in param:
            raise ValidationError(
                f"Parameter at index {i} missing 'value' key",
                field="parameters"
            )

        validate_ga4_parameter_name(param["name"])

    return parameters


def validate_filter_type(filter_type: str) -> str:
    """Validate filter comparison type.

    Args:
        filter_type: Filter type to validate

    Returns:
        The validated filter type

    Raises:
        ValidationError: If filter type is invalid
    """
    try:
        FilterType(filter_type)
        return filter_type
    except ValueError:
        valid_types = [t.value for t in FilterType]
        raise ValidationError(
            f"Invalid filter type: {filter_type}",
            field="filter_type",
            value=filter_type,
            expected=f"one of {valid_types}"
        )


def validate_trigger_ids(trigger_ids: List[str]) -> List[str]:
    """Validate list of trigger IDs.

    Args:
        trigger_ids: List of trigger IDs

    Returns:
        The validated trigger IDs

    Raises:
        ValidationError: If trigger IDs are invalid
    """
    if not trigger_ids:
        raise ValidationError(
            "Trigger IDs list cannot be empty",
            field="trigger_ids"
        )

    if not isinstance(trigger_ids, list):
        raise ValidationError(
            "Trigger IDs must be a list",
            field="trigger_ids",
            value=type(trigger_ids).__name__,
            expected="list of strings"
        )

    for i, trigger_id in enumerate(trigger_ids):
        if not isinstance(trigger_id, str):
            raise ValidationError(
                f"Trigger ID at index {i} must be a string",
                field="trigger_ids",
                value=type(trigger_id).__name__,
                expected="string"
            )

        if not trigger_id.strip():
            raise ValidationError(
                f"Trigger ID at index {i} cannot be empty",
                field="trigger_ids"
            )

    return trigger_ids


def validate_css_selector(selector: str) -> str:
    """Validate CSS selector syntax.

    Args:
        selector: CSS selector to validate

    Returns:
        The validated selector

    Raises:
        ValidationError: If selector is invalid

    Note:
        This performs basic validation. Complex selectors may require
        browser-side validation.
    """
    if not selector:
        raise ValidationError("CSS selector cannot be empty", field="selector")

    if not isinstance(selector, str):
        raise ValidationError(
            "CSS selector must be a string",
            field="selector",
            value=type(selector).__name__,
            expected="string"
        )

    # Basic validation - must not start/end with whitespace
    if selector != selector.strip():
        raise ValidationError(
            "CSS selector cannot start or end with whitespace",
            field="selector",
            value=selector,
            expected="trimmed string"
        )

    return selector


def validate_positive_integer(
    value: int,
    field_name: str = "value",
    min_value: int = 1,
    max_value: Optional[int] = None
) -> int:
    """Validate positive integer value.

    Args:
        value: Value to validate
        field_name: Name of the field being validated
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)

    Returns:
        The validated value

    Raises:
        ValidationError: If value is invalid
    """
    if not isinstance(value, int):
        raise ValidationError(
            f"{field_name.capitalize()} must be an integer",
            field=field_name,
            value=type(value).__name__,
            expected="integer"
        )

    if value < min_value:
        raise ValidationError(
            f"{field_name.capitalize()} must be >= {min_value}",
            field=field_name,
            value=value,
            expected=f">= {min_value}"
        )

    if max_value is not None and value > max_value:
        raise ValidationError(
            f"{field_name.capitalize()} must be <= {max_value}",
            field=field_name,
            value=value,
            expected=f"<= {max_value}"
        )

    return value
