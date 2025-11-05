"""Unit tests for GTM constants module."""

import pytest

from gtm_mcp.constants import (
    BUILT_IN_VARIABLES,
    DEFAULT_WORKSPACE,
    GA4_EVENT_NAME_MAX_LENGTH,
    GA4_PARAMETER_NAME_MAX_LENGTH,
    GTM_NAME_MAX_LENGTH,
    GTM_NOTES_MAX_LENGTH,
    MINIMUM_PUBLISH_SCOPES,
    MINIMUM_READ_SCOPES,
    MINIMUM_WRITE_SCOPES,
    SCOPES,
    SCROLL_PERCENTAGES,
    TAG_FIRING_OPTIONS,
    FilterType,
    ParameterType,
    TagType,
    TriggerType,
    VariableType,
)


class TestTriggerType:
    """Test TriggerType enumeration."""

    def test_pageview_trigger(self):
        """Test PAGEVIEW trigger type."""
        assert TriggerType.PAGEVIEW.value == "PAGEVIEW"

    def test_custom_event_trigger(self):
        """Test CUSTOM_EVENT trigger type."""
        assert TriggerType.CUSTOM_EVENT.value == "CUSTOM_EVENT"

    def test_scroll_depth_trigger(self):
        """Test SCROLL_DEPTH trigger type."""
        assert TriggerType.SCROLL_DEPTH.value == "SCROLL_DEPTH"

    def test_link_click_trigger(self):
        """Test LINK_CLICK trigger type."""
        assert TriggerType.LINK_CLICK.value == "LINK_CLICK"

    def test_trigger_group(self):
        """Test TRIGGER_GROUP trigger type."""
        assert TriggerType.TRIGGER_GROUP.value == "TRIGGER_GROUP"

    def test_form_submission_trigger(self):
        """Test FORM_SUBMISSION trigger type."""
        assert TriggerType.FORM_SUBMISSION.value == "FORM_SUBMISSION"

    def test_element_visibility_trigger(self):
        """Test ELEMENT_VISIBILITY trigger type."""
        assert TriggerType.ELEMENT_VISIBILITY.value == "ELEMENT_VISIBILITY"

    def test_trigger_type_is_string(self):
        """Test that trigger type values are strings."""
        assert isinstance(TriggerType.PAGEVIEW.value, str)

    def test_all_trigger_types_unique(self):
        """Test that all trigger type values are unique."""
        values = [t.value for t in TriggerType]
        assert len(values) == len(set(values))


class TestTagType:
    """Test TagType enumeration."""

    def test_ga4_config_tag(self):
        """Test GA4 config tag type."""
        assert TagType.GA4_CONFIG.value == "gaawc"

    def test_ga4_event_tag(self):
        """Test GA4 event tag type."""
        assert TagType.GA4_EVENT.value == "gaawe"

    def test_custom_html_tag(self):
        """Test custom HTML tag type."""
        assert TagType.CUSTOM_HTML.value == "html"

    def test_google_ads_conversion_tag(self):
        """Test Google Ads conversion tag type."""
        assert TagType.GOOGLE_ADS_CONVERSION.value == "awct"

    def test_tag_type_is_string(self):
        """Test that tag type values are strings."""
        assert isinstance(TagType.GA4_CONFIG.value, str)


class TestVariableType:
    """Test VariableType enumeration."""

    def test_constant_variable(self):
        """Test constant variable type."""
        assert VariableType.CONSTANT.value == "c"

    def test_custom_javascript_variable(self):
        """Test custom JavaScript variable type."""
        assert VariableType.CUSTOM_JAVASCRIPT.value == "jsm"

    def test_data_layer_variable(self):
        """Test data layer variable type."""
        assert VariableType.DATA_LAYER_VARIABLE.value == "v"

    def test_url_variable(self):
        """Test URL variable type."""
        assert VariableType.URL.value == "u"

    def test_first_party_cookie_variable(self):
        """Test first-party cookie variable type."""
        assert VariableType.FIRST_PARTY_COOKIE.value == "k"

    def test_user_provided_data_variable(self):
        """Test user-provided data variable type."""
        assert VariableType.USER_PROVIDED_DATA.value == "awec"

    def test_variable_type_is_string(self):
        """Test that variable type values are strings."""
        assert isinstance(VariableType.CONSTANT.value, str)


class TestFilterType:
    """Test FilterType enumeration."""

    def test_equals_filter(self):
        """Test EQUALS filter type."""
        assert FilterType.EQUALS.value == "EQUALS"

    def test_contains_filter(self):
        """Test CONTAINS filter type."""
        assert FilterType.CONTAINS.value == "CONTAINS"

    def test_starts_with_filter(self):
        """Test STARTS_WITH filter type."""
        assert FilterType.STARTS_WITH.value == "STARTS_WITH"

    def test_matches_regex_filter(self):
        """Test MATCHES_REGEX filter type."""
        assert FilterType.MATCHES_REGEX.value == "MATCHES_REGEX"

    def test_greater_than_filter(self):
        """Test GREATER_THAN filter type."""
        assert FilterType.GREATER_THAN.value == "GREATER_THAN"

    def test_css_selector_filter(self):
        """Test CSS_SELECTOR filter type."""
        assert FilterType.CSS_SELECTOR.value == "CSS_SELECTOR"


class TestParameterType:
    """Test ParameterType enumeration."""

    def test_template_parameter(self):
        """Test TEMPLATE parameter type."""
        assert ParameterType.TEMPLATE.value == "TEMPLATE"

    def test_boolean_parameter(self):
        """Test BOOLEAN parameter type."""
        assert ParameterType.BOOLEAN.value == "BOOLEAN"

    def test_integer_parameter(self):
        """Test INTEGER parameter type."""
        assert ParameterType.INTEGER.value == "INTEGER"

    def test_list_parameter(self):
        """Test LIST parameter type."""
        assert ParameterType.LIST.value == "LIST"

    def test_map_parameter(self):
        """Test MAP parameter type."""
        assert ParameterType.MAP.value == "MAP"

    def test_tag_reference_parameter(self):
        """Test TAG_REFERENCE parameter type."""
        assert ParameterType.TAG_REFERENCE.value == "TAG_REFERENCE"

    def test_trigger_reference_parameter(self):
        """Test TRIGGER_REFERENCE parameter type."""
        assert ParameterType.TRIGGER_REFERENCE.value == "TRIGGER_REFERENCE"


class TestBuiltInVariables:
    """Test built-in variables set."""

    def test_built_in_variables_is_set(self):
        """Test that BUILT_IN_VARIABLES is a set."""
        assert isinstance(BUILT_IN_VARIABLES, set)

    def test_page_url_in_built_in_variables(self):
        """Test PAGE_URL is in built-in variables."""
        assert "PAGE_URL" in BUILT_IN_VARIABLES

    def test_click_url_in_built_in_variables(self):
        """Test CLICK_URL is in built-in variables."""
        assert "CLICK_URL" in BUILT_IN_VARIABLES

    def test_event_in_built_in_variables(self):
        """Test EVENT is in built-in variables."""
        assert "EVENT" in BUILT_IN_VARIABLES

    def test_scroll_depth_threshold_in_built_in_variables(self):
        """Test SCROLL_DEPTH_THRESHOLD is in built-in variables."""
        assert "SCROLL_DEPTH_THRESHOLD" in BUILT_IN_VARIABLES

    def test_built_in_variables_not_empty(self):
        """Test that built-in variables set is not empty."""
        assert len(BUILT_IN_VARIABLES) > 0


class TestScrollPercentages:
    """Test scroll percentages set."""

    def test_scroll_percentages_is_set(self):
        """Test that SCROLL_PERCENTAGES is a set."""
        assert isinstance(SCROLL_PERCENTAGES, set)

    def test_common_scroll_percentages(self):
        """Test common scroll percentages are included."""
        assert 25 in SCROLL_PERCENTAGES
        assert 50 in SCROLL_PERCENTAGES
        assert 75 in SCROLL_PERCENTAGES
        assert 100 in SCROLL_PERCENTAGES

    def test_scroll_percentages_valid_range(self):
        """Test all scroll percentages are valid (0-100)."""
        for pct in SCROLL_PERCENTAGES:
            assert 0 <= pct <= 100


class TestTagFiringOptions:
    """Test tag firing options."""

    def test_tag_firing_options_is_set(self):
        """Test that TAG_FIRING_OPTIONS is a set."""
        assert isinstance(TAG_FIRING_OPTIONS, set)

    def test_unlimited_firing_option(self):
        """Test UNLIMITED firing option."""
        assert "UNLIMITED" in TAG_FIRING_OPTIONS

    def test_once_per_event_firing_option(self):
        """Test ONCE_PER_EVENT firing option."""
        assert "ONCE_PER_EVENT" in TAG_FIRING_OPTIONS

    def test_once_per_load_firing_option(self):
        """Test ONCE_PER_LOAD firing option."""
        assert "ONCE_PER_LOAD" in TAG_FIRING_OPTIONS


class TestGA4Constraints:
    """Test GA4-specific constraints."""

    def test_ga4_event_name_max_length(self):
        """Test GA4 event name max length."""
        assert GA4_EVENT_NAME_MAX_LENGTH == 40

    def test_ga4_parameter_name_max_length(self):
        """Test GA4 parameter name max length."""
        assert GA4_PARAMETER_NAME_MAX_LENGTH == 40

    def test_ga4_parameter_value_max_length(self):
        """Test GA4 parameter value max length."""
        from gtm_mcp.constants import GA4_PARAMETER_VALUE_MAX_LENGTH
        assert GA4_PARAMETER_VALUE_MAX_LENGTH == 100


class TestGTMConstraints:
    """Test GTM-specific constraints."""

    def test_gtm_name_max_length(self):
        """Test GTM name max length."""
        assert GTM_NAME_MAX_LENGTH == 256

    def test_gtm_notes_max_length(self):
        """Test GTM notes max length."""
        assert GTM_NOTES_MAX_LENGTH == 5000

    def test_default_workspace(self):
        """Test default workspace ID."""
        assert DEFAULT_WORKSPACE == "1"


class TestScopes:
    """Test GTM OAuth scopes."""

    def test_scopes_is_set(self):
        """Test that SCOPES is a set."""
        assert isinstance(SCOPES, set)

    def test_scopes_not_empty(self):
        """Test that scopes set is not empty."""
        assert len(SCOPES) > 0

    def test_readonly_scope_in_scopes(self):
        """Test readonly scope is in scopes."""
        readonly_scope = "https://www.googleapis.com/auth/tagmanager.readonly"
        assert readonly_scope in SCOPES

    def test_edit_containers_scope_in_scopes(self):
        """Test edit containers scope is in scopes."""
        edit_scope = "https://www.googleapis.com/auth/tagmanager.edit.containers"
        assert edit_scope in SCOPES

    def test_publish_scope_in_scopes(self):
        """Test publish scope is in scopes."""
        publish_scope = "https://www.googleapis.com/auth/tagmanager.publish"
        assert publish_scope in SCOPES


class TestMinimumScopes:
    """Test minimum required scopes."""

    def test_minimum_read_scopes_is_set(self):
        """Test that MINIMUM_READ_SCOPES is a set."""
        assert isinstance(MINIMUM_READ_SCOPES, set)

    def test_minimum_read_scopes_contains_readonly(self):
        """Test minimum read scopes contains readonly scope."""
        readonly = "https://www.googleapis.com/auth/tagmanager.readonly"
        assert readonly in MINIMUM_READ_SCOPES

    def test_minimum_write_scopes_is_set(self):
        """Test that MINIMUM_WRITE_SCOPES is a set."""
        assert isinstance(MINIMUM_WRITE_SCOPES, set)

    def test_minimum_write_scopes_contains_edit(self):
        """Test minimum write scopes contains edit scope."""
        edit = "https://www.googleapis.com/auth/tagmanager.edit.containers"
        assert edit in MINIMUM_WRITE_SCOPES

    def test_minimum_publish_scopes_is_set(self):
        """Test that MINIMUM_PUBLISH_SCOPES is a set."""
        assert isinstance(MINIMUM_PUBLISH_SCOPES, set)

    def test_minimum_publish_scopes_contains_publish(self):
        """Test minimum publish scopes contains publish scope."""
        publish = "https://www.googleapis.com/auth/tagmanager.publish"
        assert publish in MINIMUM_PUBLISH_SCOPES

    def test_minimum_scopes_subset_of_all_scopes(self):
        """Test that all minimum scopes are subsets of all scopes."""
        assert MINIMUM_READ_SCOPES.issubset(SCOPES)
        assert MINIMUM_WRITE_SCOPES.issubset(SCOPES)
        assert MINIMUM_PUBLISH_SCOPES.issubset(SCOPES)
