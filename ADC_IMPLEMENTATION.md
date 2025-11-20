# Application Default Credentials Implementation

This document describes the implementation of Application Default Credentials (ADC) support for the GTM MCP server.

## Overview

The GTM MCP server now supports two authentication methods:
1. **Application Default Credentials (ADC)** - Automatically discovers credentials from multiple sources
2. **OAuth 2.0** (Original method) - User-level authentication via browser

Users can choose their preferred method via the `GTM_AUTH_METHOD` environment variable.

## Implementation Details

### Authentication Flow

The authentication is handled in `src/unboundai_gtm_mcp/utils.py` in the `GTMAuth` class:

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

### Application Default Credentials (ADC) Method

When `GTM_AUTH_METHOD=service_account`:
- Uses `google.auth.default()` to automatically discover credentials
- Searches for credentials in this order:
  1. `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a service account JSON file
  2. Google Cloud SDK credentials (`gcloud auth application-default login`)
  3. Service account attached to GCE/GKE/Cloud Run instances
  4. Other Google Cloud environments
- No explicit file path checking required
- No browser interaction needed
- Automatic token refresh handled by Google's auth library

**Key Code:**
```python
def _authenticate_service_account(self) -> google.auth.credentials.Credentials:
    try:
        credentials, project = google.auth.default(scopes=self.scopes)
        return credentials
    except google.auth.exceptions.DefaultCredentialsError as e:
        raise ValueError("Failed to load Application Default Credentials...")
```

### OAuth 2.0 Method

When `GTM_AUTH_METHOD=oauth` (or not set):
- Uses the original OAuth flow
- Requires `GTM_CLIENT_ID`, `GTM_CLIENT_SECRET`, and `GTM_PROJECT_ID`
- Opens browser for authorization on first use
- Stores tokens in `~/.gtm-mcp/token.json`

## Configuration Examples

### Application Default Credentials (Service Account File)

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

### Application Default Credentials (gcloud CLI)

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "service_account"
      }
    }
  }
}
```

Note: Run `gcloud auth application-default login` first.

### Application Default Credentials (Cloud Environment)

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "service_account"
      }
    }
  }
}
```

Note: Requires service account attached to GCE/GKE/Cloud Run instance.

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

## Benefits of Application Default Credentials

1. **No Browser Interaction**: Perfect for server environments and automation
2. **Flexible Credential Sources**: Automatically discovers credentials from multiple sources
3. **Simple Local Development**: Use gcloud CLI for easy local testing
4. **Cloud Native**: Seamlessly works in Google Cloud environments
5. **Better Security**: No need to hardcode file paths in some scenarios
6. **Automatic Refresh**: Google's library handles token refresh automatically
7. **CI/CD Friendly**: Works in headless environments
8. **Industry Standard**: Follows Google's recommended authentication pattern

## Backward Compatibility

- OAuth 2.0 remains the default method
- Existing configurations work without changes
- Users can opt-in to ADC authentication when ready
- Environment variable name `GTM_AUTH_METHOD=service_account` retained for compatibility

## Testing

Comprehensive test suite in `src/unboundai_gtm_mcp/tests/test_auth.py`:
- 11 tests covering both authentication methods
- Tests for ADC discovery via `google.auth.default()`
- Tests for gcloud CLI credential scenario
- Tests for error conditions
- Tests for environment variable handling
- All tests passing ✓

## Security Considerations

### Application Default Credentials (ADC)
- Keep JSON key file secure (chmod 600 on Unix/Linux)
- Never commit key file to version control
- Regularly rotate service account keys
- Use restrictive IAM permissions
- For gcloud CLI: Understand that credentials are tied to your Google account
- For cloud environments: Use least-privilege service accounts

### OAuth 2.0
- Keep client secret secure
- Never share OAuth credentials
- Revoke access when no longer needed
- Monitor OAuth app usage in Google Cloud Console

## Documentation

Complete documentation added to README.md:
- Three setup options for ADC (service account file, gcloud CLI, cloud environment)
- Step-by-step setup guides for each option
- Comparison table to help users choose
- Troubleshooting section for ADC
- Security notes for ADC

## References

This implementation follows the pattern used by the official Google Analytics MCP server:
- https://github.com/googleanalytics/google-analytics-mcp

The implementation uses Google's recommended `google.auth.default()` approach:
- https://cloud.google.com/docs/authentication/application-default-credentials
