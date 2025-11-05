"""Constants and enumerations for GTM API.

This module defines type-safe constants for GTM trigger types, tag types,
variable types, filter operators, and parameter types based on the official
Google Tag Manager API specification.
"""

from enum import Enum
from typing import Final, Set


class TriggerType(str, Enum):
    """GTM trigger types.

    Based on the official GTM API v2 trigger type enumeration.
    Reference: https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/triggers
    """

    # Web container triggers
    PAGEVIEW = "PAGEVIEW"
    DOM_READY = "DOM_READY"
    WINDOW_LOADED = "WINDOW_LOADED"
    CUSTOM_EVENT = "CUSTOM_EVENT"
    TRIGGER_GROUP = "TRIGGER_GROUP"
    FORM_SUBMISSION = "FORM_SUBMISSION"
    CLICK = "CLICK"
    LINK_CLICK = "LINK_CLICK"
    JS_ERROR = "JS_ERROR"
    HISTORY_CHANGE = "HISTORY_CHANGE"
    TIMER = "TIMER"
    SCROLL_DEPTH = "SCROLL_DEPTH"
    ELEMENT_VISIBILITY = "ELEMENT_VISIBILITY"
    YOUTUBE_VIDEO = "YOUTUBE_VIDEO"

    # Server container triggers
    SERVER_PAGEVIEW = "SERVER_PAGEVIEW"
    ALWAYS = "ALWAYS"
    CONSENT_INIT = "CONSENT_INIT"
    INIT = "INIT"

    # Mobile container triggers
    FIREBASE_APP_EXCEPTION = "FIREBASE_APP_EXCEPTION"
    FIREBASE_APP_UPDATE = "FIREBASE_APP_UPDATE"
    FIREBASE_CAMPAIGN = "FIREBASE_CAMPAIGN"
    FIREBASE_FIRST_OPEN = "FIREBASE_FIRST_OPEN"
    FIREBASE_IN_APP_PURCHASE = "FIREBASE_IN_APP_PURCHASE"
    FIREBASE_NOTIFICATION_DISMISS = "FIREBASE_NOTIFICATION_DISMISS"
    FIREBASE_NOTIFICATION_FOREGROUND = "FIREBASE_NOTIFICATION_FOREGROUND"
    FIREBASE_NOTIFICATION_OPEN = "FIREBASE_NOTIFICATION_OPEN"
    FIREBASE_NOTIFICATION_RECEIVE = "FIREBASE_NOTIFICATION_RECEIVE"
    FIREBASE_OS_UPDATE = "FIREBASE_OS_UPDATE"
    FIREBASE_SESSION_START = "FIREBASE_SESSION_START"
    FIREBASE_USER_ENGAGEMENT = "FIREBASE_USER_ENGAGEMENT"

    # AMP container triggers
    AMP_CLICK = "AMP_CLICK"
    AMP_TIMER = "AMP_TIMER"
    AMP_SCROLL = "AMP_SCROLL"
    AMP_VISIBILITY = "AMP_VISIBILITY"


class TagType(str, Enum):
    """GTM tag types.

    Common tag types used in web containers. For a complete list,
    see the GTM Tag Gallery documentation.
    """

    # Google Analytics
    GA4_CONFIG = "gaawc"  # Google Analytics 4 - Configuration
    GA4_EVENT = "gaawe"  # Google Analytics 4 - Event
    UA = "ua"  # Universal Analytics (deprecated)

    # Google Ads
    GOOGLE_ADS_CONVERSION = "awct"
    GOOGLE_ADS_REMARKETING = "sp"

    # Custom
    CUSTOM_HTML = "html"
    CUSTOM_IMAGE = "img"

    # Floodlight
    FLOODLIGHT_COUNTER = "flc"
    FLOODLIGHT_SALES = "fls"

    # Third-party
    FACEBOOK_PIXEL = "baut"
    LINKEDIN_INSIGHT = "linkedin"
    TWITTER_CONVERSION = "twitter_website_tag"


class VariableType(str, Enum):
    """GTM variable types.

    Reference: https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/variables
    """

    # Basic variables
    CONSTANT = "c"
    CUSTOM_JAVASCRIPT = "jsm"
    DATA_LAYER_VARIABLE = "v"
    URL = "u"
    FIRST_PARTY_COOKIE = "k"
    LOOKUP_TABLE = "smm"
    REGEX_TABLE = "remm"
    RANDOM_NUMBER = "r"
    JAVASCRIPT_VARIABLE = "j"

    # Google Analytics 4
    GA4_EVENT_SETTINGS = "gtes"
    GA4_CONFIG_SETTINGS = "gas"

    # Enhanced Conversions
    USER_PROVIDED_DATA = "awec"

    # Container variables
    CONTAINER_VERSION = "ctv"
    DEBUG_MODE = "dbg"
    ENVIRONMENT_NAME = "env"


class FilterType(str, Enum):
    """Filter comparison operators for triggers.

    Used in trigger filters, custom event filters, and auto-event filters.
    """

    EQUALS = "EQUALS"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    MATCHES_REGEX = "MATCHES_REGEX"
    GREATER_THAN = "GREATER_THAN"
    GREATER_OR_EQUALS = "GREATER_OR_EQUALS"
    LESS_THAN = "LESS_THAN"
    LESS_OR_EQUALS = "LESS_OR_EQUALS"
    CSS_SELECTOR = "CSS_SELECTOR"
    MATCH_REGEX = "MATCH_REGEX"


class ParameterType(str, Enum):
    """Parameter value types in GTM API.

    These define the type field in parameter objects throughout the API.
    """

    TEMPLATE = "TEMPLATE"  # String template (can include variable references)
    BOOLEAN = "BOOLEAN"  # Boolean value
    INTEGER = "INTEGER"  # Integer value
    LIST = "LIST"  # List of parameters
    MAP = "MAP"  # Map of key-value pairs
    TAG_REFERENCE = "TAG_REFERENCE"  # Reference to another tag
    TRIGGER_REFERENCE = "TRIGGER_REFERENCE"  # Reference to a trigger


# Built-in variable types
BUILT_IN_VARIABLES: Final[Set[str]] = {
    "PAGE_URL",
    "PAGE_HOSTNAME",
    "PAGE_PATH",
    "REFERRER",
    "EVENT",
    "CLICK_ELEMENT",
    "CLICK_CLASSES",
    "CLICK_ID",
    "CLICK_TARGET",
    "CLICK_URL",
    "CLICK_TEXT",
    "FORM_ELEMENT",
    "FORM_CLASSES",
    "FORM_ID",
    "FORM_TARGET",
    "FORM_URL",
    "FORM_TEXT",
    "ERROR_MESSAGE",
    "ERROR_URL",
    "ERROR_LINE",
    "NEW_HISTORY_FRAGMENT",
    "OLD_HISTORY_FRAGMENT",
    "NEW_HISTORY_STATE",
    "OLD_HISTORY_STATE",
    "HISTORY_SOURCE",
    "VIDEO_PROVIDER",
    "VIDEO_URL",
    "VIDEO_TITLE",
    "VIDEO_DURATION",
    "VIDEO_PERCENT",
    "VIDEO_VISIBLE",
    "VIDEO_STATUS",
    "VIDEO_CURRENT_TIME",
    "SCROLL_DEPTH_THRESHOLD",
    "SCROLL_DEPTH_UNITS",
    "SCROLL_DIRECTION",
    "ELEMENT_VISIBILITY_RATIO",
    "ELEMENT_VISIBILITY_TIME",
    "ELEMENT_VISIBILITY_FIRST_TIME",
    "ELEMENT_VISIBILITY_RECENT_TIME",
}

# Scroll depth percentages (common values)
SCROLL_PERCENTAGES: Final[Set[int]] = {10, 25, 50, 75, 90, 100}

# Tag firing options
TAG_FIRING_OPTIONS: Final[Set[str]] = {
    "UNLIMITED",  # Fire every time the trigger fires
    "ONCE_PER_EVENT",  # Fire once per event
    "ONCE_PER_LOAD",  # Fire once per page load
}

# GA4 event parameter name constraints
GA4_EVENT_NAME_MAX_LENGTH: Final[int] = 40
GA4_PARAMETER_NAME_MAX_LENGTH: Final[int] = 40
GA4_PARAMETER_VALUE_MAX_LENGTH: Final[int] = 100

# GTM name constraints
GTM_NAME_MAX_LENGTH: Final[int] = 256
GTM_NOTES_MAX_LENGTH: Final[int] = 5000

# Workspace IDs
DEFAULT_WORKSPACE: Final[str] = "1"  # Default workspace ID

# Tag Manager scopes
SCOPES: Final[Set[str]] = {
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.manage.accounts",
    "https://www.googleapis.com/auth/tagmanager.manage.users",
    "https://www.googleapis.com/auth/tagmanager.publish",
    "https://www.googleapis.com/auth/tagmanager.readonly",
}

# Minimum required scopes for common operations
MINIMUM_READ_SCOPES: Final[Set[str]] = {
    "https://www.googleapis.com/auth/tagmanager.readonly",
}

MINIMUM_WRITE_SCOPES: Final[Set[str]] = {
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
}

MINIMUM_PUBLISH_SCOPES: Final[Set[str]] = {
    "https://www.googleapis.com/auth/tagmanager.publish",
}
