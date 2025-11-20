"""
Test to verify that concurrent version tool calls work properly.

This test simulates the scenario from the problem statement where
two gtm_get_version calls are made, which previously caused an MCP protocol error.
"""

import asyncio
from unittest.mock import Mock, patch
from src.unboundai_gtm_mcp.tools import GTMTools
from src.unboundai_gtm_mcp.gtm_client import GTMClient


async def test_concurrent_get_version_calls():
    """Test that multiple gtm_get_version calls can be made concurrently without errors."""
    
    # Create mock GTM client
    mock_client = Mock(spec=GTMClient)
    
    # Mock the get_version method to return different data for different versions
    def mock_get_version(version_path):
        if "versions/332" in version_path:
            return {
                "containerVersionId": "332",
                "name": "Version 332",
                "path": version_path,
                "tag": [{"tagId": "1", "name": "Tag 1"}]
            }
        elif "versions/333" in version_path:
            return {
                "containerVersionId": "333",
                "name": "Version 333",
                "path": version_path,
                "tag": [{"tagId": "2", "name": "Tag 2"}]
            }
        else:
            raise ValueError(f"Unknown version: {version_path}")
    
    mock_client.get_version = mock_get_version
    
    # Create tools instance
    tools = GTMTools()
    
    # Create tasks for concurrent calls (simulating the scenario from the problem)
    task1 = tools.execute_tool(
        "gtm_get_version",
        {"version_path": "accounts/7688143/containers/591560/versions/332"},
        mock_client
    )
    
    task2 = tools.execute_tool(
        "gtm_get_version",
        {"version_path": "accounts/7688143/containers/591560/versions/333"},
        mock_client
    )
    
    # Execute both calls concurrently
    results = await asyncio.gather(task1, task2)
    
    # Verify both calls succeeded
    assert len(results) == 2
    assert results[0]["version"]["containerVersionId"] == "332"
    assert results[1]["version"]["containerVersionId"] == "333"
    
    print("✓ Test passed: Concurrent gtm_get_version calls work correctly")


async def test_concurrent_mixed_version_tools():
    """Test that multiple different version tools can be called concurrently."""
    
    # Create mock GTM client
    mock_client = Mock(spec=GTMClient)
    
    mock_client.list_versions = lambda container_path, include_deleted=False: [
        {"containerVersionId": "1", "name": "Version 1", "path": f"{container_path}/versions/1"},
        {"containerVersionId": "2", "name": "Version 2", "path": f"{container_path}/versions/2"},
    ]
    
    mock_client.get_version = lambda version_path: {
        "containerVersionId": "1",
        "name": "Version 1",
        "path": version_path
    }
    
    mock_client.get_live_version = lambda container_path: {
        "containerVersionId": "5",
        "name": "Live Version",
        "path": f"{container_path}/versions/5"
    }
    
    mock_client.get_latest_version = lambda container_path: {
        "containerVersionId": "10",
        "name": "Latest Version",
        "path": f"{container_path}/versions/10"
    }
    
    # Create tools instance
    tools = GTMTools()
    
    # Create tasks for concurrent calls with different version tools
    tasks = [
        tools.execute_tool(
            "gtm_list_versions",
            {"container_path": "accounts/123/containers/456"},
            mock_client
        ),
        tools.execute_tool(
            "gtm_get_version",
            {"version_path": "accounts/123/containers/456/versions/1"},
            mock_client
        ),
        tools.execute_tool(
            "gtm_get_live_version",
            {"container_path": "accounts/123/containers/456"},
            mock_client
        ),
        tools.execute_tool(
            "gtm_get_latest_version",
            {"container_path": "accounts/123/containers/456"},
            mock_client
        ),
    ]
    
    # Execute all calls concurrently
    results = await asyncio.gather(*tasks)
    
    # Verify all calls succeeded
    assert len(results) == 4
    assert len(results[0]["versions"]) == 2  # list_versions
    assert results[1]["version"]["containerVersionId"] == "1"  # get_version
    assert results[2]["version"]["containerVersionId"] == "5"  # get_live_version
    assert results[3]["version"]["containerVersionId"] == "10"  # get_latest_version
    
    print("✓ Test passed: Concurrent mixed version tool calls work correctly")


async def test_concurrent_non_version_tools():
    """Test that non-version tools also work correctly with concurrent calls."""
    
    # Create mock GTM client
    mock_client = Mock(spec=GTMClient)
    
    mock_client.list_accounts = lambda: [
        {"accountId": "123", "name": "Account 1", "path": "accounts/123"},
    ]
    
    mock_client.list_containers = lambda account_id: [
        {"containerId": "456", "name": "Container 1", "path": f"accounts/{account_id}/containers/456"},
    ]
    
    mock_client.list_tags = lambda workspace_path: [
        {"tagId": "1", "name": "Tag 1", "type": "html", "path": f"{workspace_path}/tags/1"},
    ]
    
    # Create tools instance
    tools = GTMTools()
    
    # Create tasks for concurrent calls
    tasks = [
        tools.execute_tool("gtm_list_accounts", {}, mock_client),
        tools.execute_tool("gtm_list_containers", {"account_id": "123"}, mock_client),
        tools.execute_tool("gtm_list_tags", {"container_path": "accounts/123/containers/456", "workspace_id": "7"}, mock_client),
    ]
    
    # Execute all calls concurrently
    results = await asyncio.gather(*tasks)
    
    # Verify all calls succeeded
    assert len(results) == 3
    assert len(results[0]["accounts"]) == 1
    assert len(results[1]["containers"]) == 1
    assert len(results[2]["tags"]) == 1
    
    print("✓ Test passed: Concurrent non-version tool calls work correctly")


if __name__ == "__main__":
    print("Running concurrent tool call tests...\n")
    
    asyncio.run(test_concurrent_get_version_calls())
    asyncio.run(test_concurrent_mixed_version_tools())
    asyncio.run(test_concurrent_non_version_tools())
    
    print("\n✅ All tests passed! The version tools should no longer cause MCP protocol errors.")
