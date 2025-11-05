# GTM MCP Server - Account ID Restriction Feature

## Overview

The GTM MCP server now supports restricting all operations to a specific Google Tag Manager account ID. This is a security feature designed to prevent accidental modifications to the wrong GTM account when multiple accounts are accessible via the same OAuth credentials.

## Configuration

### Environment Variable

Add the `GTM_ACCOUNT_ID` environment variable to your MCP configuration:

```json
{
  "mcpServers": {
    "gtm": {
      "command": "/path/to/.venv/bin/python3",
      "args": ["-m", "gtm_mcp.server"],
      "env": {
        "GTM_CREDENTIALS_FILE": "/path/to/client_secret.json",
        "GTM_TOKEN_FILE": "/path/to/token.json",
        "GTM_ACCOUNT_ID": "6321366409"
      }
    }
  }
}
```

### Behavior

- **When `GTM_ACCOUNT_ID` is NOT set or empty**: All accessible accounts can be used (default behavior)
- **When `GTM_ACCOUNT_ID` is set**: Only the specified account ID can be accessed

## How It Works

### 1. Account Listing (`gtm_list_accounts`)

When `GTM_ACCOUNT_ID` is set:
- Returns only the specified account if it exists in your accessible accounts
- Raises `PermissionError` if the account ID is not found or not accessible

Example error:
```
Account ID 6321366409 not found in accessible accounts.
Please verify the account ID and your OAuth permissions.
```

### 2. All Other Operations

For any operation that requires an account ID (directly or via path):
- Validates the account ID matches `GTM_ACCOUNT_ID` before making API calls
- Extracts account ID from resource paths automatically

Example operations that are validated:
- `gtm_list_containers(account_id="123")` - Direct account ID parameter
- `gtm_list_tags(container_path="accounts/123/containers/456")` - Account ID extracted from path
- `gtm_create_trigger(workspace_path="accounts/123/containers/456/workspaces/789")` - Account ID extracted from path

Example error:
```
Access denied: This GTM MCP instance is restricted to account ID 6321366409.
Requested account: 999999
```

## Implementation Details

### Modified Files

1. **`src/gtm_mcp/gtm_client.py`**
   - Added `_get_restricted_account_id()` method to read `GTM_ACCOUNT_ID` from environment
   - Added `validate_account_access(account_id)` method to check access permissions
   - Added `extract_account_id_from_path(path)` helper to parse account IDs from resource paths
   - Modified `list_accounts()` to filter results when restriction is enabled
   - Added validation calls to all methods that interact with GTM resources

### Key Methods

```python
def validate_account_access(self, account_id: str) -> None:
    """Validate that the requested account_id matches the restricted account if set."""
    if self._restricted_account_id and account_id != self._restricted_account_id:
        raise PermissionError(
            f"Access denied: This GTM MCP instance is restricted to account ID "
            f"{self._restricted_account_id}. Requested account: {account_id}"
        )

def extract_account_id_from_path(self, path: str) -> str:
    """Extract account ID from a GTM path (e.g., 'accounts/123/containers/456')."""
    parts = path.split('/')
    if len(parts) < 2 or parts[0] != 'accounts':
        raise ValueError(f"Invalid GTM path format: {path}")
    return parts[1]
```

### Validation Points

All GTM client methods now validate account access:

- `list_containers(account_id)` - Direct validation
- `get_container(container_path)` - Path extraction + validation
- `list_workspaces(container_path)` - Path extraction + validation
- `list_tags(workspace_path)` - Path extraction + validation
- `get_tag(tag_path)` - Path extraction + validation
- `create_tag(workspace_path, tag_data)` - Path extraction + validation
- `update_tag(tag_path, tag_data)` - Path extraction + validation
- `list_triggers(workspace_path)` - Path extraction + validation
- `create_trigger(workspace_path, trigger_data)` - Path extraction + validation
- `list_variables(workspace_path)` - Path extraction + validation
- `get_variable(variable_path)` - Path extraction + validation
- `create_variable(workspace_path, variable_data)` - Path extraction + validation
- `update_variable(variable_path, variable_data)` - Path extraction + validation
- `create_version(workspace_path, name, notes)` - Path extraction + validation
- `publish_version(version_path)` - Path extraction + validation

## Example: ProSun Customer Configuration

For the ProSun customer with account ID `6321366409`:

```json
{
  "mcpServers": {
    "gtm": {
      "command": "/home/etma/work/mcps/gtm-mcp/.venv/bin/python3",
      "args": ["-m", "gtm_mcp.server"],
      "env": {
        "GTM_CREDENTIALS_FILE": "/home/etma/work/Vertisky/customers/ProSun/.config/google/client_secret_gtm.json",
        "GTM_TOKEN_FILE": "/home/etma/work/Vertisky/customers/ProSun/.config/google/gtm_token.json",
        "GTM_ACCOUNT_ID": "6321366409"
      }
    }
  }
}
```

With this configuration:
- Only ProSun's GTM account (6321366409) will be accessible
- Any attempt to access other accounts will be rejected with a clear error message
- The restriction happens at runtime, preventing accidental cross-account operations

## Testing

A test script is provided at `test_account_restriction.py` to verify the logic:

```bash
cd /home/etma/work/mcps/gtm-mcp
python3 test_account_restriction.py
```

The test validates:
1. Account ID extraction from various path formats
2. Validation with no restriction (allows all)
3. Validation with restriction (allows matching, rejects non-matching)
4. Error handling for invalid paths

## Security Benefits

1. **Prevents cross-account contamination**: Cannot accidentally modify the wrong account
2. **Clear error messages**: Users immediately know when they're trying to access the wrong account
3. **Runtime validation**: Checks happen on every request, not just at startup
4. **Zero-trust approach**: Even if OAuth tokens have access to multiple accounts, MCP operations are restricted
5. **Backward compatible**: Existing deployments without `GTM_ACCOUNT_ID` continue to work unchanged

## Migration Guide

To enable account restriction on an existing GTM MCP server:

1. Identify your GTM account ID:
   - Use `gtm_list_accounts` tool to see all accessible accounts
   - Find the `accountId` for the account you want to restrict to

2. Update your `.mcp.json` configuration:
   - Add `"GTM_ACCOUNT_ID": "your-account-id"` to the `env` section

3. Restart Claude Code to reload the MCP configuration

4. Test by attempting to list accounts:
   - Should only return the specified account
   - Should show error if account ID is incorrect

## Troubleshooting

### Error: "Account ID X not found in accessible accounts"

**Cause**: The account ID specified in `GTM_ACCOUNT_ID` is not accessible with your OAuth credentials.

**Solutions**:
1. Verify the account ID is correct
2. Check that your OAuth credentials have access to that account
3. Re-authenticate with GTM if needed

### Error: "Access denied: This GTM MCP instance is restricted to account ID X"

**Cause**: You're attempting to access an account that doesn't match the `GTM_ACCOUNT_ID` restriction.

**Solutions**:
1. If this is the correct account, verify the account ID in your MCP configuration
2. If you need to access multiple accounts, remove or update the `GTM_ACCOUNT_ID` setting
3. Check that you're using the correct account ID in your tool calls

### Want to disable restriction

Simply remove the `GTM_ACCOUNT_ID` environment variable from your MCP configuration and restart Claude Code.
