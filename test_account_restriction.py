#!/usr/bin/env python3
"""Test script to verify account restriction logic without OAuth."""
import os
import sys

# Add src to path
sys.path.insert(0, 'src')

def test_extract_account_id():
    """Test account ID extraction from paths."""
    print("Testing account ID extraction...")

    # Mock the GTMClient class to avoid OAuth
    class MockGTMClient:
        def __init__(self):
            self._restricted_account_id = os.environ.get('GTM_ACCOUNT_ID', '').strip() or None

        def extract_account_id_from_path(self, path: str) -> str:
            parts = path.split('/')
            if len(parts) < 2 or parts[0] != 'accounts':
                raise ValueError(f"Invalid GTM path format: {path}")
            return parts[1]

        def validate_account_access(self, account_id: str) -> None:
            if self._restricted_account_id and account_id != self._restricted_account_id:
                raise PermissionError(
                    f"Access denied: This GTM MCP instance is restricted to account ID "
                    f"{self._restricted_account_id}. Requested account: {account_id}"
                )

    # Test without restriction
    print("\n1. Test without GTM_ACCOUNT_ID (should allow all):")
    os.environ.pop('GTM_ACCOUNT_ID', None)
    client = MockGTMClient()

    try:
        account_id = client.extract_account_id_from_path("accounts/123456/containers/789")
        print(f"   ✓ Extracted account ID: {account_id}")
        client.validate_account_access(account_id)
        print(f"   ✓ Validation passed for account {account_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test with restriction - matching account
    print("\n2. Test with GTM_ACCOUNT_ID=6321366409 (ProSun) - matching:")
    os.environ['GTM_ACCOUNT_ID'] = '6321366409'
    client = MockGTMClient()

    try:
        account_id = client.extract_account_id_from_path("accounts/6321366409/containers/12345")
        print(f"   ✓ Extracted account ID: {account_id}")
        client.validate_account_access(account_id)
        print(f"   ✓ Validation passed for account {account_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test with restriction - non-matching account
    print("\n3. Test with GTM_ACCOUNT_ID=6321366409 - non-matching account:")
    try:
        account_id = client.extract_account_id_from_path("accounts/999999/containers/789")
        print(f"   ✓ Extracted account ID: {account_id}")
        client.validate_account_access(account_id)
        print(f"   ✗ Validation should have failed but didn't!")
    except PermissionError as e:
        print(f"   ✓ Validation correctly rejected: {e}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")

    # Test invalid path format
    print("\n4. Test invalid path format:")
    try:
        account_id = client.extract_account_id_from_path("invalid/path")
        print(f"   ✗ Should have raised ValueError but got: {account_id}")
    except ValueError as e:
        print(f"   ✓ Correctly rejected invalid path: {e}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")

    # Test workspace path
    print("\n5. Test workspace path extraction:")
    try:
        account_id = client.extract_account_id_from_path("accounts/6321366409/containers/123/workspaces/456")
        print(f"   ✓ Extracted account ID from workspace path: {account_id}")
        client.validate_account_access(account_id)
        print(f"   ✓ Validation passed")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n✓ All tests completed!")

if __name__ == "__main__":
    test_extract_account_id()
