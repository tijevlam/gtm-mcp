"""GTM tool implementations for MCP."""

import asyncio
from typing import Any, Dict, Optional
from .gtm_client import GTMClient
from .helpers import build_custom_event_filter


class GTMTools:
    """Container for GTM tool implementations."""

    async def execute_tool(
        self, name: str, arguments: Optional[Dict[str, Any]], client: GTMClient
    ) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool_map = {
            "gtm_list_accounts": self._list_accounts,
            "gtm_list_containers": self._list_containers,
            "gtm_list_tags": self._list_tags,
            "gtm_get_tag": self._get_tag,
            "gtm_create_tag": self._create_tag,
            "gtm_update_tag": self._update_tag,
            "gtm_list_triggers": self._list_triggers,
            "gtm_create_trigger": self._create_trigger,
            "gtm_list_variables": self._list_variables,
            "gtm_get_variable": self._get_variable,
            "gtm_create_variable": self._create_variable,
            "gtm_publish_container": self._publish_container,
            "gtm_list_versions": self._list_versions,
            "gtm_get_version": self._get_version,
            "gtm_get_live_version": self._get_live_version,
            "gtm_get_latest_version": self._get_latest_version,
            "gtm_delete_version": self._delete_version,
            "gtm_undelete_version": self._undelete_version,
            "gtm_update_version": self._update_version,
            "gtm_set_latest_version": self._set_latest_version,
        }

        handler = tool_map.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")

        return await handler(arguments or {}, client)

    async def _list_accounts(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List GTM accounts."""
        accounts = client.list_accounts()
        return {
            "accounts": [
                {
                    "accountId": acc.get("accountId"),
                    "name": acc.get("name"),
                    "path": acc.get("path"),
                }
                for acc in accounts
            ]
        }

    async def _list_containers(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List containers in an account."""
        account_id = args["account_id"]
        containers = client.list_containers(account_id)
        return {
            "containers": [
                {
                    "containerId": cont.get("containerId"),
                    "name": cont.get("name"),
                    "path": cont.get("path"),
                    "publicId": cont.get("publicId"),
                }
                for cont in containers
            ]
        }

    async def _list_tags(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List tags in a workspace."""
        container_path = args["container_path"]
        workspace_id = args.get("workspace_id")

        # Get workspace path
        if not workspace_id:
            workspaces = client.list_workspaces(container_path)
            if workspaces:
                workspace_path = workspaces[0]["path"]  # Use default workspace
            else:
                raise ValueError("No workspaces found in container")
        else:
            workspace_path = f"{container_path}/workspaces/{workspace_id}"

        tags = client.list_tags(workspace_path)
        return {
            "tags": [
                {
                    "tagId": tag.get("tagId"),
                    "name": tag.get("name"),
                    "type": tag.get("type"),
                    "path": tag.get("path"),
                }
                for tag in tags
            ]
        }

    async def _get_tag(self, args: Dict[str, Any], client: GTMClient) -> Dict[str, Any]:
        """Get detailed tag configuration."""
        tag_path = args["tag_path"]
        tag = client.get_tag(tag_path)
        return {"tag": tag}

    async def _create_tag(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Create a new tag."""
        workspace_path = args["workspace_path"]

        tag_data = {"name": args["tag_name"], "type": args["tag_type"]}

        if "tag_config" in args:
            tag_data["parameter"] = self._build_parameters(args["tag_config"])

        if "firing_trigger_ids" in args:
            tag_data["firingTriggerId"] = args["firing_trigger_ids"]

        result = client.create_tag(workspace_path, tag_data)
        return {
            "success": True,
            "tag": {
                "tagId": result.get("tagId"),
                "name": result.get("name"),
                "path": result.get("path"),
            },
        }

    async def _update_tag(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Update an existing tag."""
        tag_path = args["tag_path"]
        tag_data = args["tag_data"]

        result = client.update_tag(tag_path, tag_data)
        return {
            "success": True,
            "tag": {
                "tagId": result.get("tagId"),
                "name": result.get("name"),
                "path": result.get("path"),
            },
        }

    async def _list_triggers(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List triggers in a workspace."""
        workspace_path = args["workspace_path"]
        triggers = client.list_triggers(workspace_path)
        return {
            "triggers": [
                {
                    "triggerId": trigger.get("triggerId"),
                    "name": trigger.get("name"),
                    "type": trigger.get("type"),
                    "path": trigger.get("path"),
                }
                for trigger in triggers
            ]
        }

    async def _create_trigger(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Create a new trigger.

        Supports both direct API field passing and simplified configurations.
        For Custom Event triggers, can use either:
        1. Direct customEventFilter in trigger_config
        2. Simplified custom_event_name parameter (auto-generates filter)
        """
        workspace_path = args["workspace_path"]
        trigger_type = args["trigger_type"]

        trigger_data = {
            "name": args["trigger_name"],
            "type": trigger_type
        }

        # Handle custom_event_name parameter for simplified Custom Event trigger creation
        custom_event_name = args.get("custom_event_name")

        if trigger_type == "customEvent" and custom_event_name:
            # Use helper function to build the customEventFilter
            trigger_data["customEventFilter"] = build_custom_event_filter(custom_event_name)

        if "trigger_config" in args:
            config = args["trigger_config"]

            # Handle trigger groups with trigger ID references
            if trigger_type == "triggerGroup" and "trigger_ids" in config:
                trigger_data["parameter"] = [
                    {
                        "type": "list",
                        "key": "triggerIds",
                        "list": [
                            {"type": "triggerReference", "value": str(trigger_id)}
                            for trigger_id in config["trigger_ids"]
                        ],
                    }
                ]

            # If config contains GTM API fields directly, merge them into trigger_data
            # This allows passing complete trigger configurations
            api_fields = [
                "filter",
                "autoEventFilter",
                "customEventFilter",
                "waitForTags",
                "visibilitySelector",
                "visiblePercentageMin",
                "continuousTimeMinMilliseconds",
                "visiblePercentageMax",
                "maxTimerLengthSeconds",
                "checkValidation",
                "waitForTagsTimeout",
                "uniqueTriggerId",
                "horizontalScrollPercentageList",
                "verticalScrollPercentageList",
                "totalTimeMinMilliseconds",
                "interval",
                "intervalSeconds",
                "limit",
                "videoPercentageList",
                "triggerStartDelay",
                "elementId",
                "selector",
                "notes",
                "parameter",
                "eventName",
            ]

            for field in api_fields:
                if field in config:
                    # Don't override customEventFilter if it was already set by custom_event_name
                    if field == "customEventFilter" and custom_event_name:
                        continue
                    # Don't override parameter if it was already set for trigger groups
                    if (
                        field == "parameter"
                        and trigger_type == "triggerGroup"
                        and "trigger_ids" in config
                    ):
                        continue
                    trigger_data[field] = config[field]

            # Legacy support for simplified custom event configurations
            # Only apply if customEventFilter wasn't already set
            if (
                trigger_type == "customEvent"
                and "event_name" in config
                and "customEventFilter" not in trigger_data
            ):
                match_type = config.get("match_type", "equals")
                trigger_data["customEventFilter"] = [
                    {
                        "type": match_type,
                        "parameter": [
                            {"type": "template", "key": "arg0", "value": "{{_event}}"},
                            {
                                "type": "template",
                                "key": "arg1",
                                "value": config["event_name"],
                            },
                        ],
                    }
                ]

        # Validate that Custom Event triggers have a filter
        if trigger_type == "customEvent" and "customEventFilter" not in trigger_data:
            raise ValueError(
                "Custom Event triggers require either 'custom_event_name' parameter "
                "or 'customEventFilter' in trigger_config"
            )

        result = client.create_trigger(workspace_path, trigger_data)
        return {
            "success": True,
            "trigger": {
                "triggerId": result.get("triggerId"),
                "name": result.get("name"),
                "type": result.get("type"),
                "path": result.get("path"),
            },
        }

    async def _publish_container(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Create and publish a container version."""
        workspace_path = args["workspace_path"]
        version_name = args["version_name"]
        version_notes = args.get("version_notes", "")

        # Create version
        version = await asyncio.to_thread(client.create_version, workspace_path, version_name, version_notes)
        version_path = version.get("containerVersion", {}).get("path")

        if not version_path:
            raise ValueError("Failed to create version")

        # Publish version
        result = await asyncio.to_thread(client.publish_version, version_path)
        return {
            "success": True,
            "version": {
                "versionId": result.get("containerVersion", {}).get(
                    "containerVersionId"
                ),
                "name": result.get("containerVersion", {}).get("name"),
                "published": True,
            },
        }

    async def _list_variables(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List variables in a workspace."""
        workspace_path = args["workspace_path"]
        variables = client.list_variables(workspace_path)
        return {
            "variables": [
                {
                    "variableId": var.get("variableId"),
                    "name": var.get("name"),
                    "type": var.get("type"),
                    "path": var.get("path"),
                }
                for var in variables
            ]
        }

    async def _get_variable(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Get detailed variable configuration."""
        variable_path = args["variable_path"]
        variable = client.get_variable(variable_path)
        return {"variable": variable}

    async def _create_variable(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Create a new variable."""
        workspace_path = args["workspace_path"]

        variable_data = {"name": args["variable_name"], "type": args["variable_type"]}

        # Add variable configuration based on type
        if "variable_config" in args:
            config = args["variable_config"]

            # Build parameters based on variable type
            if args["variable_type"] == "c":  # Constant
                variable_data["parameter"] = [
                    {
                        "type": "template",
                        "key": "value",
                        "value": config.get("value", ""),
                    }
                ]
            elif args["variable_type"] == "jsm":  # Custom JavaScript Variable
                variable_data["parameter"] = [
                    {
                        "type": "template",
                        "key": "javascript",
                        "value": config.get("javascript", ""),
                    }
                ]
            elif args["variable_type"] == "u":  # URL variable
                variable_data["parameter"] = [
                    {
                        "type": "template",
                        "key": "component",
                        "value": config.get("component", "URL"),
                    }
                ]
            elif args["variable_type"] == "v":  # Data Layer Variable
                variable_data["parameter"] = [
                    {
                        "type": "template",
                        "key": "name",
                        "value": config.get("data_layer_name", ""),
                    },
                    {
                        "type": "integer",
                        "key": "dataLayerVersion",
                        "value": config.get("version", "2"),
                    },
                ]
            elif args["variable_type"] == "k":  # First-Party Cookie
                variable_data["parameter"] = [
                    {
                        "type": "template",
                        "key": "name",
                        "value": config.get("cookie_name", ""),
                    }
                ]
            elif (
                args["variable_type"] == "awec"
            ):  # User-Provided Data (Enhanced Conversions)
                # Build user data parameters with proper template type for variable references
                params = [{"type": "template", "key": "mode", "value": "MANUAL"}]
                # Add user data fields
                user_data_fields = [
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "street",
                    "city",
                    "region",
                    "postal_code",
                    "country",
                ]
                for field in user_data_fields:
                    if field in config:
                        params.append(
                            {"type": "template", "key": field, "value": config[field]}
                        )
                variable_data["parameter"] = params
            else:
                # Generic parameter handling
                variable_data["parameter"] = self._build_parameters(config)

        result = client.create_variable(workspace_path, variable_data)
        return {
            "success": True,
            "variable": {
                "variableId": result.get("variableId"),
                "name": result.get("name"),
                "type": result.get("type"),
                "path": result.get("path"),
            },
        }

    def _build_parameters(self, config: Dict[str, Any]) -> list:
        """Build parameter list from configuration dictionary."""
        parameters = []
        for key, value in config.items():
            if isinstance(value, list):
                # Handle list/map parameters (for lookup tables, etc.)
                parameters.append(
                    {
                        "type": "list",
                        "key": key,
                        "list": [
                            {
                                "type": "map",
                                "map": [
                                    {"type": "template", "key": k, "value": str(v)}
                                    for k, v in item.items()
                                ],
                            }
                            for item in value
                        ],
                    }
                )
            else:
                parameters.append({"type": "template", "key": key, "value": str(value)})
        return parameters

    async def _list_versions(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """List all versions of a container."""
        container_path = args["container_path"]
        include_deleted = args.get("include_deleted", False)
        
        versions = await asyncio.to_thread(client.list_versions, container_path, include_deleted)
        return {
            "versions": [
                {
                    "containerVersionId": ver.get("containerVersionId"),
                    "name": ver.get("name"),
                    "path": ver.get("path"),
                    "deleted": ver.get("deleted", False),
                }
                for ver in versions
            ]
        }

    async def _get_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Get details of a specific container version."""
        version_path = args["version_path"]
        version = await asyncio.to_thread(client.get_version, version_path)
        return {"version": version}

    async def _get_live_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Get the currently published (live) version."""
        container_path = args["container_path"]
        version = await asyncio.to_thread(client.get_live_version, container_path)
        return {"version": version}

    async def _get_latest_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Get the latest version header."""
        container_path = args["container_path"]
        version = await asyncio.to_thread(client.get_latest_version, container_path)
        return {"version": version}

    async def _delete_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Delete (archive) a container version."""
        version_path = args["version_path"]
        await asyncio.to_thread(client.delete_version, version_path)
        return {
            "success": True,
            "message": f"Version deleted successfully: {version_path}"
        }

    async def _undelete_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Restore a deleted version."""
        version_path = args["version_path"]
        version = await asyncio.to_thread(client.undelete_version, version_path)
        return {
            "success": True,
            "version": {
                "containerVersionId": version.get("containerVersion", {}).get("containerVersionId"),
                "name": version.get("containerVersion", {}).get("name"),
                "path": version.get("containerVersion", {}).get("path"),
            }
        }

    async def _update_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Update version metadata."""
        version_path = args["version_path"]
        version_data = args["version_data"]
        version = await asyncio.to_thread(client.update_version, version_path, version_data)
        return {
            "success": True,
            "version": {
                "containerVersionId": version.get("containerVersionId"),
                "name": version.get("name"),
                "path": version.get("path"),
            }
        }

    async def _set_latest_version(
        self, args: Dict[str, Any], client: GTMClient
    ) -> Dict[str, Any]:
        """Set a version as the latest version."""
        version_path = args["version_path"]
        version = await asyncio.to_thread(client.set_latest_version, version_path)
        return {
            "success": True,
            "version": {
                "containerVersionId": version.get("containerVersion", {}).get("containerVersionId"),
                "name": version.get("containerVersion", {}).get("name"),
                "path": version.get("containerVersion", {}).get("path"),
            }
        }
