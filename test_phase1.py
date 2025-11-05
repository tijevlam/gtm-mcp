#!/usr/bin/env python3.12
"""Quick test script for Phase 1 implementation."""

import sys
sys.path.insert(0, 'src')

from gtm_mcp.exceptions import ValidationError, GTMError, ParameterFormatError
from gtm_mcp.constants import TriggerType, TagType, VariableType, SCROLL_PERCENTAGES
from gtm_mcp.validators import (
    validate_account_id,
    validate_ga4_event_name,
    validate_scroll_percentages,
)
from gtm_mcp.helpers import (
    build_ga4_config_tag,
    build_ga4_event_tag,
    build_scroll_percentage_list,
    parse_workspace_path,
)

def test_exceptions():
    """Test exception classes."""
    print("Testing exceptions...")

    # Test basic GTMError
    error = GTMError("Test error", {"key": "value"})
    assert "Test error" in str(error)

    # Test ValidationError
    error = ValidationError("Invalid", field="account_id", value="abc", expected="numeric")
    assert error.details["field"] == "account_id"

    print("  ✓ Exceptions work correctly")

def test_constants():
    """Test constants and enums."""
    print("Testing constants...")

    # Test trigger types
    assert TriggerType.PAGEVIEW.value == "PAGEVIEW"
    assert TriggerType.SCROLL_DEPTH.value == "SCROLL_DEPTH"

    # Test tag types
    assert TagType.GA4_CONFIG.value == "gaawc"
    assert TagType.GA4_EVENT.value == "gaawe"

    # Test variable types
    assert VariableType.CONSTANT.value == "c"
    assert VariableType.DATA_LAYER_VARIABLE.value == "v"

    # Test scroll percentages
    assert 25 in SCROLL_PERCENTAGES
    assert 50 in SCROLL_PERCENTAGES

    print("  ✓ Constants defined correctly")

def test_validators():
    """Test validation functions."""
    print("Testing validators...")

    # Test account ID validation
    assert validate_account_id("1234567890") == "1234567890"

    try:
        validate_account_id("abc")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass

    # Test GA4 event name validation
    assert validate_ga4_event_name("purchase") == "purchase"
    assert validate_ga4_event_name("add_to_cart") == "add_to_cart"

    try:
        validate_ga4_event_name("123invalid")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass

    # Test scroll percentages validation
    result = validate_scroll_percentages([75, 25, 50])
    assert result == [25, 50, 75], "Should be sorted"

    result = validate_scroll_percentages([50, 50, 75])
    assert result == [50, 75], "Should remove duplicates"

    print("  ✓ Validators work correctly")

def test_helpers():
    """Test helper functions."""
    print("Testing helpers...")

    # Test building GA4 config tag
    tag = build_ga4_config_tag("GA4 - Config", "G-SMVP1L4HEW")
    assert tag["name"] == "GA4 - Config"
    assert tag["type"] == "gaawc"
    assert len(tag["parameter"]) == 2

    # Test building GA4 event tag
    tag = build_ga4_event_tag(
        "GA4 - Purchase",
        "GA4 - Config",
        "purchase",
        event_parameters=[{"name": "currency", "value": "DKK"}]
    )
    assert tag["name"] == "GA4 - Purchase"
    assert tag["type"] == "gaawe"

    # Test building scroll percentage list
    scroll_list = build_scroll_percentage_list([25, 50, 75])
    assert scroll_list["type"] == "LIST"
    assert scroll_list["key"] == "verticalScrollPercentageList"
    assert len(scroll_list["list"]) == 3
    assert scroll_list["list"][0]["value"] == "25"

    # Test parsing workspace path
    path = "accounts/6321366409/containers/233765626/workspaces/1"
    parsed = parse_workspace_path(path)
    assert parsed["account_id"] == "6321366409"
    assert parsed["container_id"] == "233765626"
    assert parsed["workspace_id"] == "1"

    print("  ✓ Helpers work correctly")

def test_scroll_depth_trigger_structure():
    """Test building the exact structure needed for scroll depth triggers."""
    print("Testing scroll depth trigger structure...")

    # This is the structure that was failing before
    scroll_params = build_scroll_percentage_list([25, 50, 75, 100])

    # Verify it matches the expected GTM API format
    expected = {
        "type": "LIST",
        "key": "verticalScrollPercentageList",
        "list": [
            {"type": "TEMPLATE", "value": "25"},
            {"type": "TEMPLATE", "value": "50"},
            {"type": "TEMPLATE", "value": "75"},
            {"type": "TEMPLATE", "value": "100"}
        ]
    }

    assert scroll_params == expected, "Scroll percentage structure doesn't match"
    print("  ✓ Scroll depth trigger structure is correct")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Phase 1 Foundation Module Tests")
    print("=" * 60 + "\n")

    try:
        test_exceptions()
        test_constants()
        test_validators()
        test_helpers()
        test_scroll_depth_trigger_structure()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60 + "\n")

        print("Phase 1 implementation is complete and working!")
        print("\nModules created:")
        print("  • src/gtm_mcp/exceptions.py")
        print("  • src/gtm_mcp/constants.py")
        print("  • src/gtm_mcp/validators.py")
        print("  • src/gtm_mcp/helpers.py")
        print("\nTest files created:")
        print("  • src/gtm_mcp/tests/test_exceptions.py")
        print("  • src/gtm_mcp/tests/test_constants.py")
        print("  • src/gtm_mcp/tests/test_validators.py")
        print("  • src/gtm_mcp/tests/test_helpers.py")

        return 0

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
