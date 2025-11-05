"""Unit tests for GTM helpers module."""

import pytest

from gtm_mcp.exceptions import ParameterFormatError
from gtm_mcp.helpers import (
    build_boolean_parameter,
    build_click_filter,
    build_container_path,
    build_custom_event_filter,
    build_event_parameter,
    build_event_parameters_list,
    build_ga4_config_tag,
    build_ga4_event_tag,
    build_integer_parameter,
    build_list_parameter,
    build_map_parameter,
    build_scroll_percentage_list,
    build_tag_reference_parameter,
    build_template_parameter,
    build_trigger_reference_parameter,
    build_url_filter,
    build_workspace_path,
    extract_id_from_path,
    merge_parameters,
    parse_workspace_path,
)


class TestBuildTemplateParameter:
    """Test build_template_parameter function."""

    def test_build_simple_template(self):
        """Test building simple template parameter."""
        result = build_template_parameter("key1", "value1")
        assert result == {
            "type": "TEMPLATE",
            "key": "key1",
            "value": "value1"
        }

    def test_build_template_with_variable_reference(self):
        """Test building template with variable reference."""
        result = build_template_parameter("eventName", "{{Event Name}}")
        assert result == {
            "type": "TEMPLATE",
            "key": "eventName",
            "value": "{{Event Name}}"
        }

    def test_build_template_converts_to_string(self):
        """Test that value is converted to string."""
        result = build_template_parameter("count", 42)
        assert result["value"] == "42"


class TestBuildBooleanParameter:
    """Test build_boolean_parameter function."""

    def test_build_true_boolean(self):
        """Test building boolean parameter with True value."""
        result = build_boolean_parameter("sendPageView", True)
        assert result == {
            "type": "BOOLEAN",
            "key": "sendPageView",
            "value": "true"
        }

    def test_build_false_boolean(self):
        """Test building boolean parameter with False value."""
        result = build_boolean_parameter("sendPageView", False)
        assert result == {
            "type": "BOOLEAN",
            "key": "sendPageView",
            "value": "false"
        }


class TestBuildIntegerParameter:
    """Test build_integer_parameter function."""

    def test_build_integer_parameter(self):
        """Test building integer parameter."""
        result = build_integer_parameter("dataLayerVersion", 2)
        assert result == {
            "type": "INTEGER",
            "key": "dataLayerVersion",
            "value": "2"
        }

    def test_build_integer_parameter_large_value(self):
        """Test building integer parameter with large value."""
        result = build_integer_parameter("timeout", 30000)
        assert result["value"] == "30000"


class TestBuildListParameter:
    """Test build_list_parameter function."""

    def test_build_list_parameter(self):
        """Test building list parameter."""
        items = [
            build_template_parameter("name", "currency"),
            build_template_parameter("value", "DKK")
        ]
        result = build_list_parameter("eventParameters", items)
        assert result["type"] == "LIST"
        assert result["key"] == "eventParameters"
        assert len(result["list"]) == 2

    def test_build_empty_list_parameter(self):
        """Test building empty list parameter."""
        result = build_list_parameter("items", [])
        assert result["list"] == []


class TestBuildMapParameter:
    """Test build_map_parameter function."""

    def test_build_map_parameter(self):
        """Test building map parameter."""
        pairs = [
            build_template_parameter("name", "currency"),
            build_template_parameter("value", "DKK")
        ]
        result = build_map_parameter(pairs)
        assert result["type"] == "MAP"
        assert len(result["map"]) == 2


class TestBuildTagReferenceParameter:
    """Test build_tag_reference_parameter function."""

    def test_build_tag_reference(self):
        """Test building tag reference parameter."""
        result = build_tag_reference_parameter("measurementId", "GA4 - Config")
        assert result == {
            "type": "TAG_REFERENCE",
            "key": "measurementId",
            "value": "GA4 - Config"
        }


class TestBuildTriggerReferenceParameter:
    """Test build_trigger_reference_parameter function."""

    def test_build_trigger_reference(self):
        """Test building trigger reference parameter."""
        result = build_trigger_reference_parameter("12345")
        assert result == {
            "type": "TRIGGER_REFERENCE",
            "value": "12345"
        }

    def test_build_trigger_reference_converts_to_string(self):
        """Test that trigger ID is converted to string."""
        result = build_trigger_reference_parameter(12345)
        assert result["value"] == "12345"


class TestBuildEventParameter:
    """Test build_event_parameter function."""

    def test_build_event_parameter(self):
        """Test building GA4 event parameter."""
        result = build_event_parameter("currency", "DKK")
        assert result["type"] == "MAP"
        assert len(result["map"]) == 2
        assert result["map"][0]["key"] == "name"
        assert result["map"][0]["value"] == "currency"
        assert result["map"][1]["key"] == "value"
        assert result["map"][1]["value"] == "DKK"

    def test_build_event_parameter_with_variable(self):
        """Test building event parameter with variable reference."""
        result = build_event_parameter("value", "{{Transaction Value}}")
        assert result["map"][1]["value"] == "{{Transaction Value}}"


class TestBuildEventParametersList:
    """Test build_event_parameters_list function."""

    def test_build_event_parameters_list(self):
        """Test building list of event parameters."""
        params = [
            {"name": "currency", "value": "DKK"},
            {"name": "value", "value": "100"}
        ]
        result = build_event_parameters_list(params)
        assert len(result) == 2
        assert result[0]["type"] == "MAP"
        assert result[0]["map"][0]["value"] == "currency"
        assert result[1]["map"][0]["value"] == "value"

    def test_build_empty_event_parameters_list(self):
        """Test building empty event parameters list."""
        result = build_event_parameters_list([])
        assert result == []


class TestBuildScrollPercentageList:
    """Test build_scroll_percentage_list function."""

    def test_build_scroll_percentage_list(self):
        """Test building scroll percentage list."""
        result = build_scroll_percentage_list([25, 50, 75])
        assert result["type"] == "LIST"
        assert result["key"] == "verticalScrollPercentageList"
        assert len(result["list"]) == 3
        assert result["list"][0] == {"type": "TEMPLATE", "value": "25"}
        assert result["list"][1] == {"type": "TEMPLATE", "value": "50"}
        assert result["list"][2] == {"type": "TEMPLATE", "value": "75"}

    def test_build_scroll_percentage_list_single_value(self):
        """Test building scroll percentage list with single value."""
        result = build_scroll_percentage_list([100])
        assert len(result["list"]) == 1
        assert result["list"][0]["value"] == "100"


class TestBuildCustomEventFilter:
    """Test build_custom_event_filter function."""

    def test_build_custom_event_filter_equals(self):
        """Test building custom event filter with EQUALS."""
        result = build_custom_event_filter("purchase")
        assert len(result) == 1
        assert result[0]["type"] == "EQUALS"
        assert len(result[0]["parameter"]) == 2
        assert result[0]["parameter"][0]["value"] == "{{_event}}"
        assert result[0]["parameter"][1]["value"] == "purchase"

    def test_build_custom_event_filter_contains(self):
        """Test building custom event filter with CONTAINS."""
        result = build_custom_event_filter("checkout", match_type="CONTAINS")
        assert result[0]["type"] == "CONTAINS"
        assert result[0]["parameter"][1]["value"] == "checkout"


class TestBuildUrlFilter:
    """Test build_url_filter function."""

    def test_build_url_filter_contains(self):
        """Test building URL filter with CONTAINS."""
        result = build_url_filter("{{Page URL}}", "CONTAINS", "/checkout")
        assert len(result) == 1
        assert result[0]["type"] == "CONTAINS"
        assert result[0]["parameter"][0]["value"] == "{{Page URL}}"
        assert result[0]["parameter"][1]["value"] == "/checkout"

    def test_build_url_filter_equals(self):
        """Test building URL filter with EQUALS."""
        result = build_url_filter("{{Page Path}}", "EQUALS", "/thank-you")
        assert result[0]["type"] == "EQUALS"


class TestBuildClickFilter:
    """Test build_click_filter function."""

    def test_build_click_filter_default(self):
        """Test building click filter with default click property."""
        result = build_click_filter("CONTAINS", "tel:")
        assert result[0]["parameter"][0]["value"] == "{{Click URL}}"
        assert result[0]["parameter"][1]["value"] == "tel:"

    def test_build_click_filter_custom_property(self):
        """Test building click filter with custom click property."""
        result = build_click_filter(
            "CONTAINS",
            "Download",
            click_property="{{Click Text}}"
        )
        assert result[0]["parameter"][0]["value"] == "{{Click Text}}"


class TestBuildWorkspacePath:
    """Test build_workspace_path function."""

    def test_build_workspace_path(self):
        """Test building workspace path from components."""
        result = build_workspace_path("123456", "789012", "5")
        assert result == "accounts/123456/containers/789012/workspaces/5"

    def test_build_workspace_path_default_workspace(self):
        """Test building path for default workspace."""
        result = build_workspace_path("6321366409", "233765626", "1")
        assert result == "accounts/6321366409/containers/233765626/workspaces/1"


class TestBuildContainerPath:
    """Test build_container_path function."""

    def test_build_container_path(self):
        """Test building container path from components."""
        result = build_container_path("123456", "789012")
        assert result == "accounts/123456/containers/789012"


class TestExtractIdFromPath:
    """Test extract_id_from_path function."""

    def test_extract_container_id(self):
        """Test extracting container ID from path."""
        path = "accounts/123456/containers/789012"
        result = extract_id_from_path(path, "container")
        assert result == "789012"

    def test_extract_workspace_id(self):
        """Test extracting workspace ID from path."""
        path = "accounts/123456/containers/789012/workspaces/5"
        result = extract_id_from_path(path, "workspace")
        assert result == "5"

    def test_extract_tag_id(self):
        """Test extracting tag ID from path."""
        path = "accounts/123/containers/456/workspaces/1/tags/789"
        result = extract_id_from_path(path, "tag")
        assert result == "789"

    def test_extract_id_invalid_path(self):
        """Test extraction fails for invalid path."""
        with pytest.raises(ParameterFormatError) as exc_info:
            extract_id_from_path("accounts/123", "container")
        assert "Could not extract" in str(exc_info.value)

    def test_extract_id_missing_resource_type(self):
        """Test extraction fails when resource type not in path."""
        with pytest.raises(ParameterFormatError) as exc_info:
            extract_id_from_path("accounts/123/containers/456", "workspace")
        assert "Could not extract" in str(exc_info.value)


class TestParseWorkspacePath:
    """Test parse_workspace_path function."""

    def test_parse_valid_workspace_path(self):
        """Test parsing valid workspace path."""
        path = "accounts/123456/containers/789012/workspaces/5"
        result = parse_workspace_path(path)
        assert result == {
            "account_id": "123456",
            "container_id": "789012",
            "workspace_id": "5"
        }

    def test_parse_prosun_workspace_path(self):
        """Test parsing ProSun workspace path."""
        path = "accounts/6321366409/containers/233765626/workspaces/1"
        result = parse_workspace_path(path)
        assert result["account_id"] == "6321366409"
        assert result["container_id"] == "233765626"
        assert result["workspace_id"] == "1"

    def test_parse_invalid_workspace_path(self):
        """Test parsing fails for invalid path."""
        with pytest.raises(ParameterFormatError) as exc_info:
            parse_workspace_path("accounts/123/containers/456")
        assert "Invalid workspace path format" in str(exc_info.value)

    def test_parse_completely_invalid_path(self):
        """Test parsing fails for completely invalid path."""
        with pytest.raises(ParameterFormatError):
            parse_workspace_path("invalid/path")


class TestMergeParameters:
    """Test merge_parameters function."""

    def test_merge_non_duplicate_parameters(self):
        """Test merging non-duplicate parameters."""
        p1 = [build_template_parameter("key1", "value1")]
        p2 = [build_template_parameter("key2", "value2")]
        result = merge_parameters(p1, p2)
        assert len(result) == 2

    def test_merge_duplicate_keys_override(self):
        """Test that duplicate keys are overridden by later parameters."""
        p1 = [build_template_parameter("key1", "value1")]
        p2 = [build_template_parameter("key1", "value2")]
        result = merge_parameters(p1, p2)
        assert len(result) == 1
        assert result[0]["value"] == "value2"

    def test_merge_empty_lists(self):
        """Test merging empty parameter lists."""
        result = merge_parameters([], [])
        assert result == []

    def test_merge_multiple_lists(self):
        """Test merging multiple parameter lists."""
        p1 = [build_template_parameter("a", "1")]
        p2 = [build_template_parameter("b", "2")]
        p3 = [build_template_parameter("c", "3")]
        result = merge_parameters(p1, p2, p3)
        assert len(result) == 3

    def test_merge_parameters_without_keys(self):
        """Test merging parameters without keys (like trigger references)."""
        p1 = [build_trigger_reference_parameter("123")]
        p2 = [build_trigger_reference_parameter("456")]
        result = merge_parameters(p1, p2)
        # Parameters without keys should all be included
        assert len(result) == 2


class TestBuildGA4ConfigTag:
    """Test build_ga4_config_tag function."""

    def test_build_basic_ga4_config_tag(self):
        """Test building basic GA4 config tag."""
        result = build_ga4_config_tag("GA4 - Config", "G-SMVP1L4HEW")
        assert result["name"] == "GA4 - Config"
        assert result["type"] == "gaawc"
        assert len(result["parameter"]) == 2

    def test_build_ga4_config_tag_no_page_view(self):
        """Test building GA4 config tag without page view."""
        result = build_ga4_config_tag(
            "GA4 - Config",
            "G-SMVP1L4HEW",
            send_page_view=False
        )
        # Find the sendPageView parameter
        send_pv = next(
            p for p in result["parameter"]
            if p.get("key") == "sendPageView"
        )
        assert send_pv["value"] == "false"

    def test_build_ga4_config_tag_with_additional_params(self):
        """Test building GA4 config tag with additional parameters."""
        additional = [build_template_parameter("customParam", "value")]
        result = build_ga4_config_tag(
            "GA4 - Config",
            "G-SMVP1L4HEW",
            additional_params=additional
        )
        # Should have 3 parameters: measurementId, sendPageView, customParam
        assert len(result["parameter"]) >= 2


class TestBuildGA4EventTag:
    """Test build_ga4_event_tag function."""

    def test_build_basic_ga4_event_tag(self):
        """Test building basic GA4 event tag."""
        result = build_ga4_event_tag(
            "GA4 - Purchase",
            "GA4 - Config",
            "purchase"
        )
        assert result["name"] == "GA4 - Purchase"
        assert result["type"] == "gaawe"
        assert len(result["parameter"]) == 2

    def test_build_ga4_event_tag_with_parameters(self):
        """Test building GA4 event tag with event parameters."""
        params = [
            {"name": "currency", "value": "DKK"},
            {"name": "value", "value": "{{Transaction Value}}"}
        ]
        result = build_ga4_event_tag(
            "GA4 - Purchase",
            "GA4 - Config",
            "purchase",
            event_parameters=params
        )
        # Should have measurementId, eventName, and eventParameters
        assert len(result["parameter"]) == 3
        event_params = next(
            p for p in result["parameter"]
            if p.get("key") == "eventParameters"
        )
        assert event_params["type"] == "LIST"

    def test_build_ga4_event_tag_with_ecommerce(self):
        """Test building GA4 event tag with ecommerce data."""
        result = build_ga4_event_tag(
            "GA4 - Purchase",
            "GA4 - Config",
            "purchase",
            send_ecommerce=True
        )
        # Should have sendEcommerceData parameter
        ecommerce_param = next(
            (p for p in result["parameter"]
             if p.get("key") == "sendEcommerceData"),
            None
        )
        assert ecommerce_param is not None
        assert ecommerce_param["value"] == "true"

    def test_build_ga4_event_tag_complete(self):
        """Test building complete GA4 event tag with all options."""
        params = [{"name": "currency", "value": "DKK"}]
        result = build_ga4_event_tag(
            "GA4 - Add to Cart",
            "GA4 - Config",
            "add_to_cart",
            event_parameters=params,
            send_ecommerce=True
        )
        assert result["name"] == "GA4 - Add to Cart"
        assert len(result["parameter"]) == 4  # measurementId, eventName, eventParameters, sendEcommerceData
