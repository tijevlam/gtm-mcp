# Application Default Credentials Implementation

This document describes the implementation of Application Default Credentials (ADC) for the GTM MCP server.

## Overview

The GTM MCP server uses Application Default Credentials (ADC) as its only authentication method. This follows the same pattern as the official [Google Analytics MCP server](https://github.com/googleanalytics/google-analytics-mcp).

## Implementation Details

### Authentication Flow

The authentication is handled in `src/unboundai_gtm_mcp/utils.py` in the `GTMAuth` class:

```python
class GTMAuth:
    def __init__(self, token_file, service_name, version, scopes):
        # No authentication method selection - ADC only
        ...
    
    def authenticate(self):
        credentials = self._create_credentials()
        service = build(self.service_name, self.version, credentials=credentials)
        return service
    
    def _create_credentials(self):
        # Check for required environment variables
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("GOOGLE_PROJECT_ID")
        
        if not credentials_path or not project_id:
            raise ValueError("Missing required environment variables")
        
        # Use google.auth.default() to discover credentials
        credentials, project = google.auth.default(scopes=self.scopes)
        return credentials
```

### Application Default Credentials (ADC) Method

The server uses `google.auth.default()` to automatically discover credentials from multiple sources:

1. **GOOGLE_APPLICATION_CREDENTIALS** environment variable pointing to a service account JSON file
2. **Google Cloud SDK credentials** (`gcloud auth application-default login`)
3. **Service account attached to GCE/GKE/Cloud Run instances**
4. **Other Google Cloud environments**

**Key Code:**
```python
def _create_credentials(self) -> google.auth.credentials.Credentials:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    
    if not credentials_path:
        raise ValueError("Missing required environment variable: GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id:
        raise ValueError("Missing required environment variable: GOOGLE_PROJECT_ID")
    
    credentials, project = google.auth.default(scopes=self.scopes)
    return credentials
```

## Required Environment Variables

The server requires two environment variables to be set in the MCP configuration:

1. **GOOGLE_APPLICATION_CREDENTIALS**: Path to the service account JSON file
2. **GOOGLE_PROJECT_ID**: Google Cloud Project ID

## Configuration Example

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account.json",
        "GOOGLE_PROJECT_ID": "your-project-id"
      }
    }
  }
}
```

## Benefits of This Approach

1. **Consistency**: Matches the Google Analytics MCP server implementation
2. **Simplicity**: One authentication method instead of two
3. **No Browser Interaction**: Perfect for server environments and automation
4. **Flexible**: Supports multiple credential sources via ADC
5. **Industry Standard**: Follows Google's recommended authentication pattern
6. **Better Security**: Service accounts with limited permissions

## Changes from Previous Version

### Removed:
- OAuth 2.0 authentication method
- `GTM_AUTH_METHOD` environment variable
- `GTM_CLIENT_ID`, `GTM_CLIENT_SECRET`, `GTM_PROJECT_ID` variables (for OAuth)
- `google-auth-oauthlib` dependency
- Dual authentication system

### Added:
- Required environment variable checks for `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_PROJECT_ID`
- Clear error messages when required variables are missing
- Simplified authentication flow

### Kept:
- Application Default Credentials support via `google.auth.default()`
- Support for service account files
- Support for gcloud CLI credentials
- Support for cloud environment credentials

## Testing

Comprehensive test suite in `src/unboundai_gtm_mcp/tests/test_auth.py`:
- 7 tests covering ADC authentication
- Tests for required environment variables
- Tests for error conditions
- All tests passing ✓

## Security Considerations

- Keep JSON key file secure (chmod 600 on Unix/Linux)
- Never commit key file to version control
- Regularly rotate service account keys
- Use restrictive IAM permissions
- Store credentials in secure locations

## References

This implementation follows the pattern used by the official Google Analytics MCP server:
- https://github.com/googleanalytics/google-analytics-mcp

The implementation uses Google's recommended `google.auth.default()` approach:
- https://cloud.google.com/docs/authentication/application-default-credentials
