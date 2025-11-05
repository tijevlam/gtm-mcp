"""Unit tests for GTM validators module."""

import pytest

from gtm_mcp.exceptions import ValidationError
from gtm_mcp.validators import (
    validate_account_id,
    validate_container_id,
    validate_css_selector,
    validate_event_parameters,
    validate_filter_type,
    validate_ga4_event_name,
    validate_ga4_parameter_name,
    validate_gtm_path,
    validate_name,
    validate_notes,
    validate_positive_integer,
    validate_scroll_percentages,
    validate_tag_type,
    validate_trigger_ids,
    validate_trigger_type,
    validate_variable_type,
    validate_workspace_id,
)


class TestValidateAccountId:
    """Test validate_account_id function."""

    def test_valid_account_id(self):
        """Test validation of valid account ID."""
        account_id = "1234567890"
        result = validate_account_id(account_id)
        assert result == account_id

    def test_valid_long_account_id(self):
        """Test validation of longer account ID."""
        account_id = "12345678901234567890"
        result = validate_account_id(account_id)
        assert result == account_id

    def test_empty_account_id(self):
        """Test validation fails for empty account ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_account_id("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_numeric_account_id(self):
        """Test validation fails for non-numeric account ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_account_id("abc123")
        assert "must contain only digits" in str(exc_info.value)

    def test_short_account_id(self):
        """Test validation fails for account ID shorter than 10 digits."""
        with pytest.raises(ValidationError) as exc_info:
            validate_account_id("123456789")
        assert "at least 10 digits" in str(exc_info.value)


class TestValidateContainerId:
    """Test validate_container_id function."""

    def test_valid_container_id(self):
        """Test validation of valid container ID."""
        container_id = "123456"
        result = validate_container_id(container_id)
        assert result == container_id

    def test_empty_container_id(self):
        """Test validation fails for empty container ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_container_id("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_numeric_container_id(self):
        """Test validation fails for non-numeric container ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_container_id("GTM-XXXXX")
        assert "must contain only digits" in str(exc_info.value)


class TestValidateWorkspaceId:
    """Test validate_workspace_id function."""

    def test_valid_workspace_id(self):
        """Test validation of valid workspace ID."""
        workspace_id = "5"
        result = validate_workspace_id(workspace_id)
        assert result == workspace_id

    def test_empty_workspace_id(self):
        """Test validation fails for empty workspace ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_workspace_id("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_numeric_workspace_id(self):
        """Test validation fails for non-numeric workspace ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_workspace_id("default")
        assert "must contain only digits" in str(exc_info.value)


class TestValidateGtmPath:
    """Test validate_gtm_path function."""

    def test_valid_container_path(self):
        """Test validation of valid container path."""
        path = "accounts/1234567890/containers/123456"
        result = validate_gtm_path(path)
        assert result == path

    def test_valid_workspace_path(self):
        """Test validation of valid workspace path."""
        path = "accounts/1234567890/containers/123456/workspaces/5"
        result = validate_gtm_path(path)
        assert result == path

    def test_empty_path(self):
        """Test validation fails for empty path."""
        with pytest.raises(ValidationError) as exc_info:
            validate_gtm_path("")
        assert "cannot be empty" in str(exc_info.value)

    def test_path_without_accounts_prefix(self):
        """Test validation fails for path without 'accounts/' prefix."""
        with pytest.raises(ValidationError) as exc_info:
            validate_gtm_path("containers/123456")
        assert "must start with 'accounts/'" in str(exc_info.value)

    def test_invalid_account_id_in_path(self):
        """Test validation fails for non-numeric account ID in path."""
        with pytest.raises(ValidationError) as exc_info:
            validate_gtm_path("accounts/abc123/containers/456")
        assert "Account ID in path must be numeric" in str(exc_info.value)

    def test_validate_expected_type_present(self):
        """Test validation succeeds when expected type is in path."""
        path = "accounts/123/containers/456/workspaces/5"
        result = validate_gtm_path(path, expected_type="workspace")
        assert result == path

    def test_validate_expected_type_missing(self):
        """Test validation fails when expected type is not in path."""
        path = "accounts/123/containers/456"
        with pytest.raises(ValidationError) as exc_info:
            validate_gtm_path(path, expected_type="workspace")
        assert "does not contain expected type" in str(exc_info.value)


class TestValidateName:
    """Test validate_name function."""

    def test_valid_name(self):
        """Test validation of valid name."""
        name = "GA4 - Config"
        result = validate_name(name)
        assert result == "GA4 - Config"

    def test_name_with_whitespace(self):
        """Test name with leading/trailing whitespace is trimmed."""
        name = "  Test Name  "
        result = validate_name(name)
        assert result == "Test Name"

    def test_empty_name(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_name("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_string_name(self):
        """Test validation fails for non-string name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_name(123)  # type: ignore
        assert "must be a string" in str(exc_info.value)

    def test_name_exceeds_max_length(self):
        """Test validation fails for name exceeding max length."""
        long_name = "x" * 300
        with pytest.raises(ValidationError) as exc_info:
            validate_name(long_name)
        assert "exceeds maximum length" in str(exc_info.value)

    def test_custom_field_name(self):
        """Test validation with custom field name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_name("", field_name="tag_name")
        assert "tag_name" in str(exc_info.value).lower()


class TestValidateNotes:
    """Test validate_notes function."""

    def test_valid_notes(self):
        """Test validation of valid notes."""
        notes = "This is a test note"
        result = validate_notes(notes)
        assert result == notes

    def test_empty_notes(self):
        """Test validation succeeds for empty notes."""
        result = validate_notes("")
        assert result == ""

    def test_non_string_notes(self):
        """Test validation fails for non-string notes."""
        with pytest.raises(ValidationError) as exc_info:
            validate_notes(123)  # type: ignore
        assert "must be a string" in str(exc_info.value)

    def test_notes_exceed_max_length(self):
        """Test validation fails for notes exceeding max length."""
        long_notes = "x" * 6000
        with pytest.raises(ValidationError) as exc_info:
            validate_notes(long_notes)
        assert "exceed maximum length" in str(exc_info.value)


class TestValidateTriggerType:
    """Test validate_trigger_type function."""

    def test_valid_pageview_trigger(self):
        """Test validation of valid PAGEVIEW trigger type."""
        result = validate_trigger_type("PAGEVIEW")
        assert result == "PAGEVIEW"

    def test_valid_custom_event_trigger(self):
        """Test validation of valid CUSTOM_EVENT trigger type."""
        result = validate_trigger_type("CUSTOM_EVENT")
        assert result == "CUSTOM_EVENT"

    def test_valid_scroll_depth_trigger(self):
        """Test validation of valid SCROLL_DEPTH trigger type."""
        result = validate_trigger_type("SCROLL_DEPTH")
        assert result == "SCROLL_DEPTH"

    def test_invalid_trigger_type(self):
        """Test validation fails for invalid trigger type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_trigger_type("INVALID_TYPE")
        assert "Invalid trigger type" in str(exc_info.value)


class TestValidateTagType:
    """Test validate_tag_type function."""

    def test_valid_tag_type(self):
        """Test validation of valid tag type."""
        result = validate_tag_type("gaawc")
        assert result == "gaawc"

    def test_custom_tag_type(self):
        """Test validation allows custom tag types."""
        result = validate_tag_type("custom_template")
        assert result == "custom_template"

    def test_empty_tag_type(self):
        """Test validation fails for empty tag type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_tag_type("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_string_tag_type(self):
        """Test validation fails for non-string tag type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_tag_type(123)  # type: ignore
        assert "must be a string" in str(exc_info.value)


class TestValidateVariableType:
    """Test validate_variable_type function."""

    def test_valid_variable_type(self):
        """Test validation of valid variable type."""
        result = validate_variable_type("c")
        assert result == "c"

    def test_custom_variable_type(self):
        """Test validation allows custom variable types."""
        result = validate_variable_type("custom_var")
        assert result == "custom_var"

    def test_empty_variable_type(self):
        """Test validation fails for empty variable type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_variable_type("")
        assert "cannot be empty" in str(exc_info.value)


class TestValidateScrollPercentages:
    """Test validate_scroll_percentages function."""

    def test_valid_scroll_percentages(self):
        """Test validation of valid scroll percentages."""
        percentages = [25, 50, 75, 100]
        result = validate_scroll_percentages(percentages)
        assert result == [25, 50, 75, 100]

    def test_scroll_percentages_sorted(self):
        """Test scroll percentages are sorted."""
        percentages = [75, 25, 100, 50]
        result = validate_scroll_percentages(percentages)
        assert result == [25, 50, 75, 100]

    def test_scroll_percentages_deduplicated(self):
        """Test duplicate scroll percentages are removed."""
        percentages = [25, 50, 50, 75, 75]
        result = validate_scroll_percentages(percentages)
        assert result == [25, 50, 75]

    def test_empty_scroll_percentages(self):
        """Test validation fails for empty percentages list."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scroll_percentages([])
        assert "cannot be empty" in str(exc_info.value)

    def test_non_list_scroll_percentages(self):
        """Test validation fails for non-list input."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scroll_percentages(50)  # type: ignore
        assert "must be a list" in str(exc_info.value)

    def test_non_integer_percentage(self):
        """Test validation fails for non-integer percentage."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scroll_percentages([25, "50", 75])  # type: ignore
        assert "must be an integer" in str(exc_info.value)

    def test_negative_percentage(self):
        """Test validation fails for negative percentage."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scroll_percentages([-10, 50])
        assert "must be between 0 and 100" in str(exc_info.value)

    def test_percentage_over_100(self):
        """Test validation fails for percentage over 100."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scroll_percentages([50, 150])
        assert "must be between 0 and 100" in str(exc_info.value)


class TestValidateGA4EventName:
    """Test validate_ga4_event_name function."""

    def test_valid_event_name(self):
        """Test validation of valid event name."""
        result = validate_ga4_event_name("purchase")
        assert result == "purchase"

    def test_valid_event_name_with_underscores(self):
        """Test validation of event name with underscores."""
        result = validate_ga4_event_name("add_to_cart")
        assert result == "add_to_cart"

    def test_valid_event_name_with_numbers(self):
        """Test validation of event name with numbers."""
        result = validate_ga4_event_name("event123")
        assert result == "event123"

    def test_empty_event_name(self):
        """Test validation fails for empty event name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_event_name("")
        assert "cannot be empty" in str(exc_info.value)

    def test_event_name_too_long(self):
        """Test validation fails for event name exceeding max length."""
        long_name = "x" * 50
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_event_name(long_name)
        assert "exceeds maximum length" in str(exc_info.value)

    def test_event_name_starts_with_number(self):
        """Test validation fails for event name starting with number."""
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_event_name("123event")
        assert "must start with a letter" in str(exc_info.value)

    def test_event_name_with_spaces(self):
        """Test validation fails for event name with spaces."""
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_event_name("my event")
        assert "can only contain" in str(exc_info.value)

    def test_event_name_with_hyphens(self):
        """Test validation fails for event name with hyphens."""
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_event_name("my-event")
        assert "can only contain" in str(exc_info.value)


class TestValidateGA4ParameterName:
    """Test validate_ga4_parameter_name function."""

    def test_valid_parameter_name(self):
        """Test validation of valid parameter name."""
        result = validate_ga4_parameter_name("currency")
        assert result == "currency"

    def test_valid_parameter_name_with_underscores(self):
        """Test validation of parameter name with underscores."""
        result = validate_ga4_parameter_name("transaction_id")
        assert result == "transaction_id"

    def test_empty_parameter_name(self):
        """Test validation fails for empty parameter name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_parameter_name("")
        assert "cannot be empty" in str(exc_info.value)

    def test_parameter_name_too_long(self):
        """Test validation fails for parameter name exceeding max length."""
        long_name = "x" * 50
        with pytest.raises(ValidationError) as exc_info:
            validate_ga4_parameter_name(long_name)
        assert "exceeds maximum length" in str(exc_info.value)


class TestValidateEventParameters:
    """Test validate_event_parameters function."""

    def test_valid_event_parameters(self):
        """Test validation of valid event parameters."""
        params = [
            {"name": "currency", "value": "DKK"},
            {"name": "value", "value": "100"}
        ]
        result = validate_event_parameters(params)
        assert result == params

    def test_empty_parameters_list(self):
        """Test validation succeeds for empty parameters list."""
        result = validate_event_parameters([])
        assert result == []

    def test_non_list_parameters(self):
        """Test validation fails for non-list input."""
        with pytest.raises(ValidationError) as exc_info:
            validate_event_parameters({"name": "test"})  # type: ignore
        assert "must be a list" in str(exc_info.value)

    def test_non_dict_parameter(self):
        """Test validation fails for non-dict parameter."""
        with pytest.raises(ValidationError) as exc_info:
            validate_event_parameters(["invalid"])  # type: ignore
        assert "must be a dictionary" in str(exc_info.value)

    def test_parameter_missing_name(self):
        """Test validation fails for parameter missing 'name' key."""
        with pytest.raises(ValidationError) as exc_info:
            validate_event_parameters([{"value": "test"}])
        assert "missing 'name' key" in str(exc_info.value)

    def test_parameter_missing_value(self):
        """Test validation fails for parameter missing 'value' key."""
        with pytest.raises(ValidationError) as exc_info:
            validate_event_parameters([{"name": "test"}])
        assert "missing 'value' key" in str(exc_info.value)


class TestValidateFilterType:
    """Test validate_filter_type function."""

    def test_valid_equals_filter(self):
        """Test validation of EQUALS filter type."""
        result = validate_filter_type("EQUALS")
        assert result == "EQUALS"

    def test_valid_contains_filter(self):
        """Test validation of CONTAINS filter type."""
        result = validate_filter_type("CONTAINS")
        assert result == "CONTAINS"

    def test_invalid_filter_type(self):
        """Test validation fails for invalid filter type."""
        with pytest.raises(ValidationError) as exc_info:
            validate_filter_type("INVALID")
        assert "Invalid filter type" in str(exc_info.value)


class TestValidateTriggerIds:
    """Test validate_trigger_ids function."""

    def test_valid_trigger_ids(self):
        """Test validation of valid trigger IDs."""
        ids = ["123", "456", "789"]
        result = validate_trigger_ids(ids)
        assert result == ids

    def test_empty_trigger_ids(self):
        """Test validation fails for empty list."""
        with pytest.raises(ValidationError) as exc_info:
            validate_trigger_ids([])
        assert "cannot be empty" in str(exc_info.value)

    def test_non_list_trigger_ids(self):
        """Test validation fails for non-list input."""
        with pytest.raises(ValidationError) as exc_info:
            validate_trigger_ids("123")  # type: ignore
        assert "must be a list" in str(exc_info.value)

    def test_non_string_trigger_id(self):
        """Test validation fails for non-string trigger ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_trigger_ids([123, 456])  # type: ignore
        assert "must be a string" in str(exc_info.value)

    def test_empty_string_trigger_id(self):
        """Test validation fails for empty string trigger ID."""
        with pytest.raises(ValidationError) as exc_info:
            validate_trigger_ids(["123", "", "789"])
        assert "cannot be empty" in str(exc_info.value)


class TestValidateCssSelector:
    """Test validate_css_selector function."""

    def test_valid_css_selector(self):
        """Test validation of valid CSS selector."""
        result = validate_css_selector("#my-element")
        assert result == "#my-element"

    def test_valid_class_selector(self):
        """Test validation of valid class selector."""
        result = validate_css_selector(".my-class")
        assert result == ".my-class"

    def test_valid_complex_selector(self):
        """Test validation of complex CSS selector."""
        result = validate_css_selector("div.class > p[data-attr='value']")
        assert result == "div.class > p[data-attr='value']"

    def test_empty_css_selector(self):
        """Test validation fails for empty selector."""
        with pytest.raises(ValidationError) as exc_info:
            validate_css_selector("")
        assert "cannot be empty" in str(exc_info.value)

    def test_non_string_css_selector(self):
        """Test validation fails for non-string selector."""
        with pytest.raises(ValidationError) as exc_info:
            validate_css_selector(123)  # type: ignore
        assert "must be a string" in str(exc_info.value)

    def test_selector_with_leading_whitespace(self):
        """Test validation fails for selector with leading whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            validate_css_selector("  #element")
        assert "cannot start or end with whitespace" in str(exc_info.value)

    def test_selector_with_trailing_whitespace(self):
        """Test validation fails for selector with trailing whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            validate_css_selector("#element  ")
        assert "cannot start or end with whitespace" in str(exc_info.value)


class TestValidatePositiveInteger:
    """Test validate_positive_integer function."""

    def test_valid_positive_integer(self):
        """Test validation of valid positive integer."""
        result = validate_positive_integer(42)
        assert result == 42

    def test_minimum_value(self):
        """Test validation with minimum value."""
        result = validate_positive_integer(1, min_value=1)
        assert result == 1

    def test_custom_minimum_value(self):
        """Test validation with custom minimum value."""
        result = validate_positive_integer(10, min_value=5)
        assert result == 10

    def test_value_below_minimum(self):
        """Test validation fails for value below minimum."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer(0, min_value=1)
        assert ">= 1" in str(exc_info.value)

    def test_maximum_value(self):
        """Test validation with maximum value."""
        result = validate_positive_integer(50, max_value=100)
        assert result == 50

    def test_value_above_maximum(self):
        """Test validation fails for value above maximum."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer(150, max_value=100)
        assert "<= 100" in str(exc_info.value)

    def test_non_integer_value(self):
        """Test validation fails for non-integer value."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer("42")  # type: ignore
        assert "must be an integer" in str(exc_info.value)

    def test_custom_field_name(self):
        """Test validation with custom field name."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_integer("test", field_name="timeout")  # type: ignore
        assert "timeout" in str(exc_info.value).lower()
