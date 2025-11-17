# Application Default Credentials Implementation

This document describes the implementation of Application Default Credentials (ADC) support for the GTM MCP server.

## Overview

The GTM MCP server now supports two authentication methods:
1. **Service Account** (Application Default Credentials)
2. **OAuth 2.0** (Original method)

Users can choose their preferred method via the `GTM_AUTH_METHOD` environment variable.

## Implementation Details

### Authentication Flow

The authentication is handled in `src/gtm_mcp/utils.py` in the `GTMAuth` class:

```python
class GTMAuth:
    def __init__(self, token_file, service_name, version, scopes):
        self.auth_method = os.getenv("GTM_AUTH_METHOD", "oauth").lower()
        # ... other initialization
    
    def authenticate(self):
        if self.auth_method == "service_account":
            return self._authenticate_service_account()
        elif self.auth_method == "oauth":
            return self._authenticate_oauth()
        else:
            raise ValueError(f"Invalid GTM_AUTH_METHOD: '{self.auth_method}'")
```

### Service Account Method

When `GTM_AUTH_METHOD=service_account`:
- Reads credentials from the file specified in `GOOGLE_APPLICATION_CREDENTIALS`
- Creates service account credentials with the required scopes
- No browser interaction needed
- Automatic token refresh handled by Google's auth library

### OAuth 2.0 Method

When `GTM_AUTH_METHOD=oauth` (or not set):
- Uses the original OAuth flow
- Requires `GTM_CLIENT_ID`, `GTM_CLIENT_SECRET`, and `GTM_PROJECT_ID`
- Opens browser for authorization on first use
- Stores tokens in `~/.gtm-mcp/token.json`

## Configuration Examples

### Service Account

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "service_account",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account.json"
      }
    }
  }
}
```

### OAuth 2.0

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "oauth",
        "GTM_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GTM_CLIENT_SECRET": "GOCSPX-your-secret",
        "GTM_PROJECT_ID": "your-project"
      }
    }
  }
}
```

## Benefits of Service Account Authentication

1. **No Browser Interaction**: Perfect for server environments and automation
2. **Simpler Setup**: No OAuth consent screen configuration required
3. **Better Security**: Credentials in a single JSON file with restrictive permissions
4. **Automatic Refresh**: Google's library handles token refresh automatically
5. **CI/CD Friendly**: Works in headless environments

## Backward Compatibility

- OAuth 2.0 remains the default method
- Existing configurations work without changes
- Users can opt-in to service account authentication when ready

## Testing

Comprehensive test suite added in `src/gtm_mcp/tests/test_auth.py`:
- 11 tests covering both authentication methods
- Tests for error conditions
- Tests for environment variable handling
- All tests passing ✓

## Security Considerations

### Service Account
- Keep JSON key file secure (chmod 600 on Unix/Linux)
- Never commit key file to version control
- Regularly rotate service account keys
- Use restrictive IAM permissions

### OAuth 2.0
- Keep client secret secure
- Never share OAuth credentials
- Revoke access when no longer needed
- Monitor OAuth app usage in Google Cloud Console

## Documentation

Complete documentation added to README.md:
- Step-by-step setup guides for both methods
- Comparison table to help users choose
- Troubleshooting section for both methods
- Security notes for both methods

## References

This implementation follows the pattern used by the Google Analytics 4 MCP server:
https://github.com/surendranb/google-analytics-mcp
