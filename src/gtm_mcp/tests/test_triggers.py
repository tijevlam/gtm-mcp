"""Unit tests for GTM trigger functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gtm_mcp.exceptions import ParameterFormatError
from gtm_mcp.helpers import build_custom_event_filter
from gtm_mcp.tools import GTMTools


class TestBuildCustomEventFilter:
    """Test build_custom_event_filter function."""

    def test_builds_correct_structure(self):
        """Test that the filter structure matches GTM API requirements."""
        result = build_custom_event_filter("purchase")

        assert isinstance(result, list)
        assert len(result) == 1

        filter_obj = result[0]
        assert filter_obj["type"] == "EQUALS"
        assert "parameter" in filter_obj
        assert len(filter_obj["parameter"]) == 2

        # Check arg0 (the {{_event}} variable)
        arg0 = filter_obj["parameter"][0]
        assert arg0["type"] == "TEMPLATE"
        assert arg0["key"] == "arg0"
        assert arg0["value"] == "{{_event}}"

        # Check arg1 (the event name)
        arg1 = filter_obj["parameter"][1]
        assert arg1["type"] == "TEMPLATE"
        assert arg1["key"] == "arg1"
        assert arg1["value"] == "purchase"

    def test_validates_event_name_empty(self):
        """Test that empty event name raises ParameterFormatError."""
        with pytest.raises(ParameterFormatError) as exc_info:
            build_custom_event_filter("")
        assert "Event name cannot be empty" in str(exc_info.value)

    def test_validates_event_name_whitespace_only(self):
        """Test that whitespace-only event name raises ParameterFormatError."""
        with pytest.raises(ParameterFormatError) as exc_info:
            build_custom_event_filter("   ")
        assert "Event name cannot be empty" in str(exc_info.value)

    def test_validates_event_name_type(self):
        """Test that non-string event name raises ParameterFormatError."""
        with pytest.raises(ParameterFormatError) as exc_info:
            build_custom_event_filter(123)
        assert "Event name must be a string" in str(exc_info.value)

    def test_validates_event_name_none(self):
        """Test that None event name raises ParameterFormatError."""
        with pytest.raises(ParameterFormatError) as exc_info:
            build_custom_event_filter(None)
        assert "Event name cannot be empty" in str(exc_info.value)

    def test_strips_whitespace(self):
        """Test that whitespace is stripped from event name."""
        result = build_custom_event_filter("  purchase  ")
        arg1 = result[0]["parameter"][1]
        assert arg1["value"] == "purchase"

    def test_custom_match_type(self):
        """Test using custom match type."""
        result = build_custom_event_filter("checkout", match_type="CONTAINS")
        assert result[0]["type"] == "CONTAINS"

    def test_multiple_events(self):
        """Test creating filters for multiple event names."""
        events = ["add_to_cart", "begin_checkout", "purchase", "view_item"]
        filters = [build_custom_event_filter(event) for event in events]

        assert len(filters) == 4
        for i, event in enumerate(events):
            assert filters[i][0]["parameter"][1]["value"] == event


class TestCreateTriggerWithCustomEventName:
    """Test gtm_create_trigger with custom_event_name parameter."""

    @pytest.mark.asyncio
    async def test_creates_custom_event_trigger(self):
        """Test creating a Custom Event trigger with custom_event_name."""
        # Mock GTM client
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "123",
            "name": "CE - purchase",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/123"
        })

        # Create tools instance
        tools = GTMTools()

        # Call with custom_event_name
        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - purchase",
                "trigger_type": "customEvent",
                "custom_event_name": "purchase"
            },
            mock_client
        )

        # Verify the trigger was created
        assert result["success"] is True
        assert result["trigger"]["triggerId"] == "123"
        assert result["trigger"]["name"] == "CE - purchase"

        # Verify the call to create_trigger
        mock_client.create_trigger.assert_called_once()
        call_args = mock_client.create_trigger.call_args[0]

        # Check workspace path
        assert call_args[0] == "accounts/6321366409/containers/233765626/workspaces/2"

        # Check trigger data
        trigger_data = call_args[1]
        assert trigger_data["name"] == "CE - purchase"
        assert trigger_data["type"] == "customEvent"
        assert "customEventFilter" in trigger_data

        # Verify customEventFilter structure
        custom_filter = trigger_data["customEventFilter"]
        assert len(custom_filter) == 1
        assert custom_filter[0]["type"] == "EQUALS"
        assert custom_filter[0]["parameter"][0]["value"] == "{{_event}}"
        assert custom_filter[0]["parameter"][1]["value"] == "purchase"

    @pytest.mark.asyncio
    async def test_requires_custom_event_name_for_custom_events(self):
        """Test that Custom Event triggers require custom_event_name or customEventFilter."""
        mock_client = MagicMock()
        tools = GTMTools()

        # Should raise ValueError when neither custom_event_name nor customEventFilter provided
        with pytest.raises(ValueError) as exc_info:
            await tools._create_trigger(
                {
                    "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                    "trigger_name": "CE - test",
                    "trigger_type": "customEvent"
                    # No custom_event_name or trigger_config with customEventFilter
                },
                mock_client
            )
        assert "Custom Event triggers require" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_backward_compatibility_other_triggers(self):
        """Test that non-Custom Event triggers work without custom_event_name."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "456",
            "name": "All Pages",
            "type": "PAGEVIEW",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/456"
        })

        tools = GTMTools()

        # Create a pageview trigger (should not require custom_event_name)
        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "All Pages",
                "trigger_type": "pageview"
            },
            mock_client
        )

        assert result["success"] is True
        assert result["trigger"]["type"] == "PAGEVIEW"

        # Verify no customEventFilter was added
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        assert "customEventFilter" not in trigger_data

    @pytest.mark.asyncio
    async def test_custom_event_name_with_whitespace(self):
        """Test that whitespace is handled in custom_event_name."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "789",
            "name": "CE - add_to_cart",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/789"
        })

        tools = GTMTools()

        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - add_to_cart",
                "trigger_type": "customEvent",
                "custom_event_name": "  add_to_cart  "  # With whitespace
            },
            mock_client
        )

        # Verify the event name was trimmed
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        event_name = trigger_data["customEventFilter"][0]["parameter"][1]["value"]
        assert event_name == "add_to_cart"

    @pytest.mark.asyncio
    async def test_custom_event_with_config_override(self):
        """Test that trigger_config can override custom_event_name if needed."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "999",
            "name": "CE - custom",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/999"
        })

        tools = GTMTools()

        # Provide both custom_event_name and customEventFilter in config
        # custom_event_name should take precedence
        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - custom",
                "trigger_type": "customEvent",
                "custom_event_name": "from_parameter",
                "trigger_config": {
                    "customEventFilter": [
                        {
                            "type": "CONTAINS",
                            "parameter": [
                                {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                                {"type": "TEMPLATE", "key": "arg1", "value": "from_config"}
                            ]
                        }
                    ]
                }
            },
            mock_client
        )

        # custom_event_name should be used (takes precedence)
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        event_name = trigger_data["customEventFilter"][0]["parameter"][1]["value"]
        assert event_name == "from_parameter"

    @pytest.mark.asyncio
    async def test_legacy_event_name_in_config(self):
        """Test backward compatibility with event_name in trigger_config."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "111",
            "name": "CE - legacy",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/111"
        })

        tools = GTMTools()

        # Use legacy event_name in trigger_config
        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - legacy",
                "trigger_type": "customEvent",
                "trigger_config": {
                    "event_name": "legacy_event"
                }
            },
            mock_client
        )

        # Should still work via legacy path
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        assert "customEventFilter" in trigger_data
        event_name = trigger_data["customEventFilter"][0]["parameter"][1]["value"]
        assert event_name == "legacy_event"


class TestProSunWooCommerceEvents:
    """Test creating ProSun WooCommerce event triggers."""

    @pytest.mark.asyncio
    async def test_create_all_woocommerce_triggers(self):
        """Test creating all 4 WooCommerce event triggers for ProSun."""
        mock_client = MagicMock()

        # Track calls to create_trigger
        created_triggers = []

        def mock_create_trigger(workspace_path, trigger_data):
            created_triggers.append(trigger_data)
            return {
                "triggerId": str(len(created_triggers)),
                "name": trigger_data["name"],
                "type": trigger_data["type"],
                "path": f"{workspace_path}/triggers/{len(created_triggers)}"
            }

        mock_client.create_trigger = MagicMock(side_effect=mock_create_trigger)

        tools = GTMTools()
        workspace_path = "accounts/6321366409/containers/233765626/workspaces/2"

        events = [
            ("CE - add_to_cart", "add_to_cart"),
            ("CE - begin_checkout", "begin_checkout"),
            ("CE - purchase", "purchase"),
            ("CE - view_item", "view_item")
        ]

        results = []
        for trigger_name, event_name in events:
            result = await tools._create_trigger(
                {
                    "workspace_path": workspace_path,
                    "trigger_name": trigger_name,
                    "trigger_type": "customEvent",
                    "custom_event_name": event_name
                },
                mock_client
            )
            results.append(result)

        # Verify all triggers were created
        assert len(created_triggers) == 4
        assert all(result["success"] for result in results)

        # Verify each trigger has correct event name
        for i, (trigger_name, event_name) in enumerate(events):
            trigger_data = created_triggers[i]
            assert trigger_data["name"] == trigger_name
            assert trigger_data["type"] == "customEvent"

            # Verify customEventFilter
            custom_filter = trigger_data["customEventFilter"]
            assert custom_filter[0]["parameter"][1]["value"] == event_name

    @pytest.mark.asyncio
    async def test_prosun_trigger_structure_matches_container(self):
        """Test that generated triggers match ProSun container structure."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "100",
            "name": "CE - purchase",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/100"
        })

        tools = GTMTools()

        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - purchase",
                "trigger_type": "customEvent",
                "custom_event_name": "purchase"
            },
            mock_client
        )

        # Get the actual trigger data sent to API
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]

        # Expected structure from ProSun container
        expected_structure = {
            "name": "CE - purchase",
            "type": "customEvent",
            "customEventFilter": [
                {
                    "type": "EQUALS",
                    "parameter": [
                        {
                            "type": "TEMPLATE",
                            "key": "arg0",
                            "value": "{{_event}}"
                        },
                        {
                            "type": "TEMPLATE",
                            "key": "arg1",
                            "value": "purchase"
                        }
                    ]
                }
            ]
        }

        # Verify structure matches
        assert trigger_data["name"] == expected_structure["name"]
        assert trigger_data["type"] == expected_structure["type"]
        assert trigger_data["customEventFilter"] == expected_structure["customEventFilter"]


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_empty_custom_event_name_raises_error(self):
        """Test that empty custom_event_name raises ValueError (caught by validation)."""
        mock_client = MagicMock()
        tools = GTMTools()

        # Empty string is falsy, so it won't call build_custom_event_filter
        # Instead, the validation at the end will catch it
        with pytest.raises(ValueError) as exc_info:
            await tools._create_trigger(
                {
                    "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                    "trigger_name": "CE - test",
                    "trigger_type": "customEvent",
                    "custom_event_name": ""
                },
                mock_client
            )
        assert "Custom Event triggers require" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_trigger_group_not_affected(self):
        """Test that trigger groups are not affected by custom event changes."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "200",
            "name": "Trigger Group",
            "type": "TRIGGER_GROUP",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/200"
        })

        tools = GTMTools()

        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "Trigger Group",
                "trigger_type": "triggerGroup",
                "trigger_config": {
                    "trigger_ids": ["1", "2", "3"]
                }
            },
            mock_client
        )

        # Verify trigger group was created correctly
        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        assert trigger_data["type"] == "triggerGroup"
        assert "parameter" in trigger_data
        assert "customEventFilter" not in trigger_data

    @pytest.mark.asyncio
    async def test_special_characters_in_event_name(self):
        """Test event names with underscores and numbers."""
        mock_client = MagicMock()
        mock_client.create_trigger = MagicMock(return_value={
            "triggerId": "300",
            "name": "CE - test_event_123",
            "type": "CUSTOM_EVENT",
            "path": "accounts/6321366409/containers/233765626/workspaces/2/triggers/300"
        })

        tools = GTMTools()

        result = await tools._create_trigger(
            {
                "workspace_path": "accounts/6321366409/containers/233765626/workspaces/2",
                "trigger_name": "CE - test_event_123",
                "trigger_type": "customEvent",
                "custom_event_name": "test_event_123"
            },
            mock_client
        )

        call_args = mock_client.create_trigger.call_args[0]
        trigger_data = call_args[1]
        event_name = trigger_data["customEventFilter"][0]["parameter"][1]["value"]
        assert event_name == "test_event_123"
