# GTM MCP Phase 1 - Usage Examples

This document demonstrates how the Phase 1 foundation modules solve the original problem of complex GTM API parameter formatting.

## The Problem

Creating a scroll depth trigger previously failed because of the complex nested structure required:

```python
# This was the attempt that failed
trigger_config = {
    "verticalScrollPercentageList": [25, 50, 75]  # WRONG - GTM API rejects this
}

# GTM API actually requires:
trigger_config = {
    "verticalScrollPercentageList": {
        "type": "LIST",
        "key": "verticalScrollPercentageList",
        "list": [
            {"type": "TEMPLATE", "value": "25"},
            {"type": "TEMPLATE", "value": "50"},
            {"type": "TEMPLATE", "value": "75"}
        ]
    }
}
```

## The Solution

Phase 1 provides helper functions that handle this complexity:

```python
from gtm_mcp.helpers import build_scroll_percentage_list

# Simple Python list -> Correct GTM API structure
scroll_config = build_scroll_percentage_list([25, 50, 75])
# Returns the complex nested structure automatically
```

## Example 1: Creating a Scroll Depth Trigger

### Before (Manual API Structure)

```python
# Error-prone, hard to remember, easy to get wrong
trigger_data = {
    "name": "Scroll Depth - 25-50-75-100",
    "type": "scrollDepth",  # Wrong case
    "verticalScrollPercentageList": {
        "type": "list",  # Wrong case
        "key": "verticalScrollPercentageList",
        "list": [
            {"type": "template", "value": 25},  # Wrong: value should be string
            {"type": "template", "value": 50},
            {"type": "template", "value": 75},
            {"type": "template", "value": 100}
        ]
    }
}
```

### After (Using Phase 1 Helpers)

```python
from gtm_mcp.constants import TriggerType
from gtm_mcp.validators import validate_scroll_percentages, validate_name
from gtm_mcp.helpers import build_scroll_percentage_list

# Type-safe, validated, correct
name = validate_name("Scroll Depth - 25-50-75-100")
percentages = validate_scroll_percentages([25, 50, 75, 100])
scroll_params = build_scroll_percentage_list(percentages)

trigger_data = {
    "name": name,
    "type": TriggerType.SCROLL_DEPTH.value,  # Type-safe enum
    "verticalScrollPercentageList": scroll_params  # Correct structure
}
```

## Example 2: Creating a GA4 Event Tag

### Before (Manual API Structure)

```python
# Complex nested structure, easy to make mistakes
tag_data = {
    "name": "GA4 - Event - Purchase",
    "type": "gaawe",
    "parameter": [
        {
            "type": "tagReference",  # Wrong case
            "key": "measurementId",
            "value": "GA4 - Config"
        },
        {
            "type": "template",  # Wrong case
            "key": "eventName",
            "value": "purchase"
        },
        {
            "type": "list",  # Wrong case
            "key": "eventParameters",
            "list": [
                {
                    "type": "map",  # Wrong case
                    "map": [
                        {"type": "template", "key": "name", "value": "currency"},
                        {"type": "template", "key": "value", "value": "DKK"}
                    ]
                },
                # ... more parameters
            ]
        }
    ]
}
```

### After (Using Phase 1 Helpers)

```python
from gtm_mcp.helpers import build_ga4_event_tag
from gtm_mcp.validators import validate_ga4_event_name

# Simple, readable, correct
event_name = validate_ga4_event_name("purchase")

tag_data = build_ga4_event_tag(
    name="GA4 - Event - Purchase",
    config_tag_name="GA4 - Config",
    event_name=event_name,
    event_parameters=[
        {"name": "currency", "value": "DKK"},
        {"name": "value", "value": "{{Transaction Value}}"},
        {"name": "transaction_id", "value": "{{Transaction ID}}"}
    ],
    send_ecommerce=True
)
```

## Example 3: Creating a Custom Event Trigger

### Before (Manual API Structure)

```python
trigger_data = {
    "name": "CE - purchase",
    "type": "customEvent",  # Wrong case
    "customEventFilter": [
        {
            "type": "equals",  # Wrong case
            "parameter": [
                {
                    "type": "template",  # Wrong case
                    "key": "arg0",
                    "value": "{{_event}}"
                },
                {
                    "type": "template",  # Wrong case
                    "key": "arg1",
                    "value": "purchase"
                }
            ]
        }
    ]
}
```

### After (Using Phase 1 Helpers)

```python
from gtm_mcp.constants import TriggerType
from gtm_mcp.helpers import build_custom_event_filter
from gtm_mcp.validators import validate_name

trigger_data = {
    "name": validate_name("CE - purchase"),
    "type": TriggerType.CUSTOM_EVENT.value,
    "customEventFilter": build_custom_event_filter("purchase")
}
```

## Example 4: Creating a Data Layer Variable

### Before (Manual API Structure)

```python
variable_data = {
    "name": "DLV - ecommerce.transaction_id",
    "type": "v",
    "parameter": [
        {
            "type": "integer",  # Wrong case
            "key": "dataLayerVersion",
            "value": 2  # Wrong: should be string
        },
        {
            "type": "template",  # Wrong case
            "key": "name",
            "value": "ecommerce.transaction_id"
        }
    ]
}
```

### After (Using Phase 1 Helpers)

```python
from gtm_mcp.constants import VariableType
from gtm_mcp.helpers import build_template_parameter, build_integer_parameter

variable_data = {
    "name": "DLV - ecommerce.transaction_id",
    "type": VariableType.DATA_LAYER_VARIABLE.value,
    "parameter": [
        build_integer_parameter("dataLayerVersion", 2),
        build_template_parameter("name", "ecommerce.transaction_id")
    ]
}
```

## Example 5: Error Handling with Validation

### Before (Silent Failures or Cryptic API Errors)

```python
# Invalid event name - would fail at API level
tag_data = {
    "eventName": "123-invalid-event"  # Starts with number, has hyphens
}

# API returns: "Error 400: Invalid event name format"
```

### After (Clear Validation Errors)

```python
from gtm_mcp.validators import validate_ga4_event_name
from gtm_mcp.exceptions import ValidationError

try:
    event_name = validate_ga4_event_name("123-invalid-event")
except ValidationError as e:
    print(f"Error: {e.message}")
    # "Event name must start with a letter"
    print(f"Field: {e.details['field']}")
    # "event_name"
    print(f"Expected: {e.details['expected']}")
    # "starts with a letter"
```

## Example 6: Type Safety with Enums

### Before (String Typos)

```python
# Typo in trigger type - would fail at API level
trigger_data = {
    "type": "PAGEVEEW"  # Typo!
}

# Typo in tag type - would fail at API level
tag_data = {
    "type": "gaawce"  # Wrong!
}
```

### After (Type-Safe Enums)

```python
from gtm_mcp.constants import TriggerType, TagType

# IDE autocomplete prevents typos
trigger_data = {
    "type": TriggerType.PAGEVIEW.value  # Type-safe
}

tag_data = {
    "type": TagType.GA4_CONFIG.value  # Type-safe
}
```

## Example 7: Path Parsing

### Before (Manual String Manipulation)

```python
# Error-prone path parsing
path = "accounts/6321366409/containers/233765626/workspaces/1"
parts = path.split("/")
account_id = parts[1]  # Hope the format is correct!
container_id = parts[3]
workspace_id = parts[5]
```

### After (Safe Path Parsing)

```python
from gtm_mcp.helpers import parse_workspace_path
from gtm_mcp.exceptions import ParameterFormatError

try:
    path = "accounts/6321366409/containers/233765626/workspaces/1"
    parsed = parse_workspace_path(path)

    account_id = parsed["account_id"]      # "6321366409"
    container_id = parsed["container_id"]  # "233765626"
    workspace_id = parsed["workspace_id"]  # "1"
except ParameterFormatError as e:
    print(f"Invalid path: {e.message}")
```

## Example 8: Building Complete Tags

### Before (200+ Lines of Manual Structure)

```python
# Manually building a complete GA4 Purchase event tag
tag_data = {
    "name": "GA4 - Event - Purchase",
    "type": "gaawe",
    "parameter": [
        {"type": "TAG_REFERENCE", "key": "measurementId", "value": "GA4 - Config"},
        {"type": "TEMPLATE", "key": "eventName", "value": "purchase"},
        {
            "type": "LIST",
            "key": "eventParameters",
            "list": [
                {
                    "type": "MAP",
                    "map": [
                        {"type": "TEMPLATE", "key": "name", "value": "transaction_id"},
                        {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.transaction_id}}"}
                    ]
                },
                {
                    "type": "MAP",
                    "map": [
                        {"type": "TEMPLATE", "key": "name", "value": "value"},
                        {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.value}}"}
                    ]
                },
                {
                    "type": "MAP",
                    "map": [
                        {"type": "TEMPLATE", "key": "name", "value": "currency"},
                        {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.currency}}"}
                    ]
                },
                {
                    "type": "MAP",
                    "map": [
                        {"type": "TEMPLATE", "key": "name", "value": "items"},
                        {"type": "TEMPLATE", "key": "value", "value": "{{DLV - ecommerce.items}}"}
                    ]
                }
            ]
        },
        {"type": "BOOLEAN", "key": "sendEcommerceData", "value": "true"}
    ]
}
```

### After (10 Lines of Clear Code)

```python
from gtm_mcp.helpers import build_ga4_event_tag

tag_data = build_ga4_event_tag(
    name="GA4 - Event - Purchase",
    config_tag_name="GA4 - Config",
    event_name="purchase",
    event_parameters=[
        {"name": "transaction_id", "value": "{{DLV - ecommerce.transaction_id}}"},
        {"name": "value", "value": "{{DLV - ecommerce.value}}"},
        {"name": "currency", "value": "{{DLV - ecommerce.currency}}"},
        {"name": "items", "value": "{{DLV - ecommerce.items}}"}
    ],
    send_ecommerce=True
)
```

## Benefits Summary

1. **Correctness**: Helpers guarantee correct GTM API structure
2. **Type Safety**: Enums prevent string typos
3. **Validation**: Early error detection with clear messages
4. **Readability**: 10 lines instead of 200
5. **Maintainability**: Centralized parameter building
6. **Documentation**: Self-documenting code
7. **IDE Support**: Autocomplete and type checking

## Real-World Impact

**Before Phase 1:**
- Creating a scroll depth trigger: **FAILED** (complex structure, case sensitivity)
- Manual parameter building: **200+ lines** for a complete tag
- Error messages: **Cryptic API errors**
- Type safety: **None** (string typos common)

**After Phase 1:**
- Creating a scroll depth trigger: **SUCCESS** (one function call)
- Helper-based building: **10 lines** for a complete tag
- Error messages: **Clear, field-level validation**
- Type safety: **Full** (enums, type hints, validation)

## Next Steps

Phase 2 will build on this foundation to create even higher-level functions like:

```python
# Phase 2 preview
trigger = create_scroll_depth_trigger(
    account_id="6321366409",
    container_id="233765626",
    workspace_id="1",
    name="Scroll Depth - 25-50-75-100",
    vertical_percentages=[25, 50, 75, 100]
)
# Returns created trigger with ID, path, etc.
```

These Phase 2 functions will internally use the Phase 1 validators and helpers, making GTM management as easy as a single function call.
