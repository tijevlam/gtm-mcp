"""Helper functions for building GTM API parameters.

This module provides utility functions to construct complex GTM API parameter
structures from simple Python data types. It handles the nested type/key/value
format required by the GTM API.
"""

from typing import Any, Dict, List, Optional, Union

from .constants import ParameterType
from .exceptions import ParameterFormatError


def build_template_parameter(key: str, value: str) -> Dict[str, str]:
    """Build a template parameter.

    Template parameters can contain variable references like {{Variable Name}}.

    Args:
        key: Parameter key name
        value: Parameter value (can include variable references)

    Returns:
        GTM API parameter structure

    Example:
        >>> build_template_parameter("measurementId", "G-XXXXXXXXXX")
        {'type': 'TEMPLATE', 'key': 'measurementId', 'value': 'G-XXXXXXXXXX'}

        >>> build_template_parameter("eventName", "{{Event Name}}")
        {'type': 'TEMPLATE', 'key': 'eventName', 'value': '{{Event Name}}'}
    """
    return {
        "type": ParameterType.TEMPLATE.value,
        "key": key,
        "value": str(value)
    }


def build_boolean_parameter(key: str, value: bool) -> Dict[str, Union[str, bool]]:
    """Build a boolean parameter.

    Args:
        key: Parameter key name
        value: Boolean value

    Returns:
        GTM API parameter structure

    Example:
        >>> build_boolean_parameter("sendPageView", True)
        {'type': 'BOOLEAN', 'key': 'sendPageView', 'value': 'true'}
    """
    return {
        "type": ParameterType.BOOLEAN.value,
        "key": key,
        "value": "true" if value else "false"
    }


def build_integer_parameter(key: str, value: int) -> Dict[str, Union[str, int]]:
    """Build an integer parameter.

    Args:
        key: Parameter key name
        value: Integer value

    Returns:
        GTM API parameter structure

    Example:
        >>> build_integer_parameter("dataLayerVersion", 2)
        {'type': 'INTEGER', 'key': 'dataLayerVersion', 'value': '2'}
    """
    return {
        "type": ParameterType.INTEGER.value,
        "key": key,
        "value": str(value)
    }


def build_list_parameter(
    key: str,
    items: List[Dict[str, Any]]
) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
    """Build a list parameter.

    Args:
        key: Parameter key name
        items: List of parameter items (typically maps or templates)

    Returns:
        GTM API parameter structure

    Example:
        >>> items = [
        ...     build_template_parameter("name", "transaction_id"),
        ...     build_template_parameter("value", "{{Transaction ID}}")
        ... ]
        >>> build_list_parameter("eventParameters", items)
        {
            'type': 'LIST',
            'key': 'eventParameters',
            'list': [...]
        }
    """
    return {
        "type": ParameterType.LIST.value,
        "key": key,
        "list": items
    }


def build_map_parameter(
    key_value_pairs: List[Dict[str, str]]
) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """Build a map parameter.

    Args:
        key_value_pairs: List of parameter dictionaries (typically templates)

    Returns:
        GTM API parameter structure

    Example:
        >>> pairs = [
        ...     build_template_parameter("name", "currency"),
        ...     build_template_parameter("value", "DKK")
        ... ]
        >>> build_map_parameter(pairs)
        {'type': 'MAP', 'map': [...]}
    """
    return {
        "type": ParameterType.MAP.value,
        "map": key_value_pairs
    }


def build_tag_reference_parameter(
    key: str,
    tag_name: str
) -> Dict[str, str]:
    """Build a tag reference parameter.

    Args:
        key: Parameter key name
        tag_name: Name of the referenced tag

    Returns:
        GTM API parameter structure

    Example:
        >>> build_tag_reference_parameter("measurementId", "GA4 - Config")
        {'type': 'TAG_REFERENCE', 'key': 'measurementId', 'value': 'GA4 - Config'}
    """
    return {
        "type": ParameterType.TAG_REFERENCE.value,
        "key": key,
        "value": tag_name
    }


def build_trigger_reference_parameter(
    trigger_id: str
) -> Dict[str, str]:
    """Build a trigger reference parameter.

    Args:
        trigger_id: ID of the referenced trigger

    Returns:
        GTM API parameter structure

    Example:
        >>> build_trigger_reference_parameter("12345")
        {'type': 'TRIGGER_REFERENCE', 'value': '12345'}
    """
    return {
        "type": ParameterType.TRIGGER_REFERENCE.value,
        "value": str(trigger_id)
    }


def build_event_parameter(name: str, value: str) -> Dict[str, Any]:
    """Build a GA4 event parameter map.

    Constructs the nested map structure required for GA4 event parameters.

    Args:
        name: Parameter name
        value: Parameter value (can be a variable reference)

    Returns:
        GTM API map parameter structure

    Example:
        >>> build_event_parameter("currency", "DKK")
        {
            'type': 'MAP',
            'map': [
                {'type': 'TEMPLATE', 'key': 'name', 'value': 'currency'},
                {'type': 'TEMPLATE', 'key': 'value', 'value': 'DKK'}
            ]
        }
    """
    return build_map_parameter([
        build_template_parameter("name", name),
        build_template_parameter("value", value)
    ])


def build_event_parameters_list(
    parameters: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """Build a list of GA4 event parameters.

    Args:
        parameters: List of dicts with 'name' and 'value' keys

    Returns:
        List of GTM API parameter structures

    Example:
        >>> params = [
        ...     {"name": "currency", "value": "DKK"},
        ...     {"name": "value", "value": "{{Transaction Value}}"}
        ... ]
        >>> build_event_parameters_list(params)
        [
            {
                'type': 'MAP',
                'map': [
                    {'type': 'TEMPLATE', 'key': 'name', 'value': 'currency'},
                    {'type': 'TEMPLATE', 'key': 'value', 'value': 'DKK'}
                ]
            },
            ...
        ]
    """
    return [
        build_event_parameter(param["name"], param["value"])
        for param in parameters
    ]


def build_scroll_percentage_list(
    percentages: List[int]
) -> Dict[str, Any]:
    """Build scroll percentage list parameter.

    Constructs the nested structure required for scroll depth triggers.

    Args:
        percentages: List of scroll depth percentages (0-100)

    Returns:
        GTM API parameter structure

    Example:
        >>> build_scroll_percentage_list([25, 50, 75])
        {
            'type': 'LIST',
            'key': 'verticalScrollPercentageList',
            'list': [
                {'type': 'TEMPLATE', 'value': '25'},
                {'type': 'TEMPLATE', 'value': '50'},
                {'type': 'TEMPLATE', 'value': '75'}
            ]
        }
    """
    return {
        "type": ParameterType.LIST.value,
        "key": "verticalScrollPercentageList",
        "list": [
            {"type": ParameterType.TEMPLATE.value, "value": str(pct)}
            for pct in percentages
        ]
    }


def build_custom_event_filter(
    event_name: str,
    match_type: str = "EQUALS"
) -> List[Dict[str, Any]]:
    """Build custom event filter for triggers.

    Creates the customEventFilter structure required by the GTM API for
    Custom Event triggers. This filter matches against the dataLayer event name.

    Args:
        event_name: Name of the custom event to match (non-empty string)
        match_type: Comparison type (EQUALS, CONTAINS, MATCHES_REGEX, etc.)

    Returns:
        GTM API custom event filter structure

    Raises:
        ParameterFormatError: If event_name is empty or invalid

    Example:
        >>> build_custom_event_filter("purchase")
        [
            {
                'type': 'EQUALS',
                'parameter': [
                    {'type': 'TEMPLATE', 'key': 'arg0', 'value': '{{_event}}'},
                    {'type': 'TEMPLATE', 'key': 'arg1', 'value': 'purchase'}
                ]
            }
        ]

        >>> build_custom_event_filter("add_to_cart")
        [
            {
                'type': 'EQUALS',
                'parameter': [
                    {'type': 'TEMPLATE', 'key': 'arg0', 'value': '{{_event}}'},
                    {'type': 'TEMPLATE', 'key': 'arg1', 'value': 'add_to_cart'}
                ]
            }
        ]
    """
    # Validate event_name
    if not event_name:
        raise ParameterFormatError(
            "Event name cannot be empty",
            parameter_key="event_name",
            expected_structure="non-empty string"
        )

    if not isinstance(event_name, str):
        raise ParameterFormatError(
            f"Event name must be a string, got {type(event_name).__name__}",
            parameter_key="event_name",
            expected_structure="string"
        )

    # Strip whitespace and re-validate
    event_name = event_name.strip()
    if not event_name:
        raise ParameterFormatError(
            "Event name cannot be empty or whitespace only",
            parameter_key="event_name",
            expected_structure="non-empty string"
        )

    return [
        {
            "type": match_type,
            "parameter": [
                build_template_parameter("arg0", "{{_event}}"),
                build_template_parameter("arg1", event_name)
            ]
        }
    ]


def build_url_filter(
    variable: str,
    match_type: str,
    pattern: str
) -> List[Dict[str, Any]]:
    """Build URL/page filter for triggers.

    Args:
        variable: Variable to match against (e.g., "{{Page URL}}")
        match_type: Comparison type (EQUALS, CONTAINS, MATCHES_REGEX, etc.)
        pattern: Pattern to match

    Returns:
        GTM API filter structure

    Example:
        >>> build_url_filter("{{Page URL}}", "CONTAINS", "/checkout")
        [
            {
                'type': 'CONTAINS',
                'parameter': [
                    {'type': 'TEMPLATE', 'key': 'arg0', 'value': '{{Page URL}}'},
                    {'type': 'TEMPLATE', 'key': 'arg1', 'value': '/checkout'}
                ]
            }
        ]
    """
    return [
        {
            "type": match_type,
            "parameter": [
                build_template_parameter("arg0", variable),
                build_template_parameter("arg1", pattern)
            ]
        }
    ]


def build_click_filter(
    match_type: str,
    pattern: str,
    click_property: str = "{{Click URL}}"
) -> List[Dict[str, Any]]:
    """Build click event filter.

    Args:
        match_type: Comparison type (EQUALS, CONTAINS, etc.)
        pattern: Pattern to match
        click_property: Click property to match (default: {{Click URL}})

    Returns:
        GTM API filter structure

    Example:
        >>> build_click_filter("CONTAINS", "tel:")
        [
            {
                'type': 'CONTAINS',
                'parameter': [
                    {'type': 'TEMPLATE', 'key': 'arg0', 'value': '{{Click URL}}'},
                    {'type': 'TEMPLATE', 'key': 'arg1', 'value': 'tel:'}
                ]
            }
        ]
    """
    return build_url_filter(click_property, match_type, pattern)


def build_workspace_path(
    account_id: str,
    container_id: str,
    workspace_id: str
) -> str:
    """Build workspace path from components.

    Args:
        account_id: GTM account ID
        container_id: GTM container ID
        workspace_id: GTM workspace ID

    Returns:
        Complete workspace path

    Example:
        >>> build_workspace_path("123456", "789012", "5")
        'accounts/123456/containers/789012/workspaces/5'
    """
    return f"accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}"


def build_container_path(account_id: str, container_id: str) -> str:
    """Build container path from components.

    Args:
        account_id: GTM account ID
        container_id: GTM container ID

    Returns:
        Complete container path

    Example:
        >>> build_container_path("123456", "789012")
        'accounts/123456/containers/789012'
    """
    return f"accounts/{account_id}/containers/{container_id}"


def extract_id_from_path(path: str, resource_type: str) -> str:
    """Extract resource ID from GTM path.

    Args:
        path: GTM resource path
        resource_type: Type of resource (e.g., 'container', 'workspace', 'tag')

    Returns:
        The extracted resource ID

    Raises:
        ParameterFormatError: If path format is invalid

    Example:
        >>> extract_id_from_path(
        ...     'accounts/123/containers/456/workspaces/5',
        ...     'workspace'
        ... )
        '5'
    """
    parts = path.split("/")
    try:
        # Find the index of the resource type
        plural = f"{resource_type}s"
        idx = parts.index(plural)
        # ID is the next element
        return parts[idx + 1]
    except (ValueError, IndexError):
        raise ParameterFormatError(
            f"Could not extract {resource_type} ID from path",
            parameter_key="path",
            expected_structure=f".../{resource_type}s/{{id}}/..."
        )


def parse_workspace_path(
    path: str
) -> Dict[str, str]:
    """Parse workspace path into components.

    Args:
        path: Workspace path

    Returns:
        Dictionary with account_id, container_id, and workspace_id

    Raises:
        ParameterFormatError: If path format is invalid

    Example:
        >>> parse_workspace_path('accounts/123/containers/456/workspaces/5')
        {
            'account_id': '123',
            'container_id': '456',
            'workspace_id': '5'
        }
    """
    try:
        parts = path.split("/")
        if len(parts) != 6:
            raise ValueError("Invalid path length")

        return {
            "account_id": parts[1],
            "container_id": parts[3],
            "workspace_id": parts[5]
        }
    except (ValueError, IndexError) as e:
        raise ParameterFormatError(
            "Invalid workspace path format",
            parameter_key="path",
            expected_structure="accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}"
        )


def merge_parameters(
    *param_lists: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Merge multiple parameter lists, avoiding duplicates.

    If duplicate keys exist, later parameters override earlier ones.

    Args:
        *param_lists: Variable number of parameter lists to merge

    Returns:
        Merged parameter list

    Example:
        >>> p1 = [build_template_parameter("key1", "value1")]
        >>> p2 = [build_template_parameter("key2", "value2")]
        >>> merge_parameters(p1, p2)
        [
            {'type': 'TEMPLATE', 'key': 'key1', 'value': 'value1'},
            {'type': 'TEMPLATE', 'key': 'key2', 'value': 'value2'}
        ]
    """
    merged: Dict[str, Dict[str, Any]] = {}

    for param_list in param_lists:
        for param in param_list:
            key = param.get("key")
            if key:
                merged[key] = param
            else:
                # Parameters without keys (like trigger references) are always added
                # Use a unique identifier to prevent overwrites
                unique_key = f"_no_key_{id(param)}"
                merged[unique_key] = param

    # Filter out the temporary keys we added
    return [
        param for key, param in merged.items()
        if not key.startswith("_no_key_")
    ] + [
        param for key, param in merged.items()
        if key.startswith("_no_key_")
    ]


def build_ga4_config_tag(
    name: str,
    measurement_id: str,
    send_page_view: bool = True,
    additional_params: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Build a complete GA4 Configuration tag.

    Args:
        name: Tag name
        measurement_id: GA4 Measurement ID (G-XXXXXXXXXX)
        send_page_view: Whether to send automatic page view
        additional_params: Optional additional parameters

    Returns:
        Complete tag configuration

    Example:
        >>> build_ga4_config_tag("GA4 - Config", "G-SMVP1L4HEW")
        {
            'name': 'GA4 - Config',
            'type': 'gaawc',
            'parameter': [...]
        }
    """
    params = [
        build_template_parameter("measurementId", measurement_id),
        build_boolean_parameter("sendPageView", send_page_view)
    ]

    if additional_params:
        params = merge_parameters(params, additional_params)

    return {
        "name": name,
        "type": "gaawc",
        "parameter": params
    }


def build_ga4_event_tag(
    name: str,
    config_tag_name: str,
    event_name: str,
    event_parameters: Optional[List[Dict[str, str]]] = None,
    send_ecommerce: bool = False
) -> Dict[str, Any]:
    """Build a complete GA4 Event tag.

    Args:
        name: Tag name
        config_tag_name: Name of the GA4 Config tag to reference
        event_name: GA4 event name
        event_parameters: Optional list of event parameters
        send_ecommerce: Whether to send ecommerce data

    Returns:
        Complete tag configuration

    Example:
        >>> build_ga4_event_tag(
        ...     "GA4 - Purchase",
        ...     "GA4 - Config",
        ...     "purchase",
        ...     [{"name": "currency", "value": "DKK"}]
        ... )
        {
            'name': 'GA4 - Purchase',
            'type': 'gaawe',
            'parameter': [...]
        }
    """
    params = [
        build_tag_reference_parameter("measurementId", config_tag_name),
        build_template_parameter("eventName", event_name)
    ]

    if event_parameters:
        params.append(
            build_list_parameter(
                "eventParameters",
                build_event_parameters_list(event_parameters)
            )
        )

    if send_ecommerce:
        params.append(build_boolean_parameter("sendEcommerceData", True))

    return {
        "name": name,
        "type": "gaawe",
        "parameter": params
    }
