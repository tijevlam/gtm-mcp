import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from googleapiclient.errors import HttpError
from .utils import _authenticate

SERVICE_NAME = 'tagmanager'
VERSION = 'v2'
TOKEN_FILE = Path.home() / '.gtm-mcp' / 'token.json'
SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.manage.accounts",
    "https://www.googleapis.com/auth/tagmanager.manage.users",
    "https://www.googleapis.com/auth/tagmanager.publish",
    "https://www.googleapis.com/auth/tagmanager.readonly"
]


class GTMClient:
    def __init__(self):
        self.service = _authenticate(TOKEN_FILE, SERVICE_NAME, VERSION, SCOPES)
        self.credentials = None
        self._restricted_account_id: Optional[str] = self._get_restricted_account_id()

    def _get_restricted_account_id(self) -> Optional[str]:
        """Get the GTM_ACCOUNT_ID from environment if set."""
        account_id = os.environ.get('GTM_ACCOUNT_ID', '').strip()
        return account_id if account_id else None

    def validate_account_access(self, account_id: str) -> None:
        """
        Validate that the requested account_id matches the restricted account if set.

        Args:
            account_id: The account ID being requested

        Raises:
            PermissionError: If GTM_ACCOUNT_ID is set and doesn't match the requested account_id
        """
        if self._restricted_account_id and account_id != self._restricted_account_id:
            raise PermissionError(
                f"Access denied: This GTM MCP instance is restricted to account ID "
                f"{self._restricted_account_id}. Requested account: {account_id}"
            )

    def extract_account_id_from_path(self, path: str) -> str:
        """
        Extract account ID from a GTM path (e.g., 'accounts/123/containers/456').

        Args:
            path: GTM resource path

        Returns:
            The extracted account ID

        Raises:
            ValueError: If path format is invalid
        """
        parts = path.split('/')
        if len(parts) < 2 or parts[0] != 'accounts':
            raise ValueError(f"Invalid GTM path format: {path}")
        return parts[1]

    def list_accounts(self) -> List[Dict[str, Any]]:
        """List all Google Tag Manager accounts, filtered by GTM_ACCOUNT_ID if set."""
        try:
            response = self.service.accounts().list().execute()
            accounts = response.get("account", [])

            # Filter accounts if restriction is enabled
            if self._restricted_account_id:
                filtered_accounts = [
                    acc for acc in accounts
                    if acc.get("accountId") == self._restricted_account_id
                ]

                if not filtered_accounts:
                    raise PermissionError(
                        f"Account ID {self._restricted_account_id} not found in accessible "
                        f"accounts. Please verify the account ID and your OAuth permissions."
                    )

                return filtered_accounts

            return accounts
        except HttpError as e:
            raise Exception(f"Failed to list accounts: {e}")

    def list_containers(self, account_id: str) -> List[Dict[str, Any]]:
        """List containers in an account."""
        self.validate_account_access(account_id)

        try:
            parent = f"accounts/{account_id}"
            response = self.service.accounts().containers().list(parent=parent).execute()
            return response.get('container', [])
        except HttpError as e:
            raise Exception(f"Failed to list containers: {e}")

    def get_container(self, container_path: str) -> Dict[str, Any]:
        """Get container details."""
        account_id = self.extract_account_id_from_path(container_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().get(path=container_path).execute()
        except HttpError as e:
            raise Exception(f"Failed to get container: {e}")

    def list_workspaces(self, container_path: str) -> List[Dict[str, Any]]:
        """List all workspaces in a container."""
        account_id = self.extract_account_id_from_path(container_path)
        self.validate_account_access(account_id)

        try:
            response = self.service.accounts().containers().workspaces().list(
                parent=container_path
            ).execute()
            return response.get('workspace', [])
        except HttpError as e:
            raise Exception(f"Failed to list workspaces: {e}")

    def list_tags(self, workspace_path: str) -> List[Dict[str, Any]]:
        """List all tags in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            response = self.service.accounts().containers().workspaces().tags().list(
                parent=workspace_path
            ).execute()
            return response.get('tag', [])
        except HttpError as e:
            raise Exception(f"Failed to list tags: {e}")

    def get_tag(self, tag_path: str) -> Dict[str, Any]:
        """Get a specific tag's details."""
        account_id = self.extract_account_id_from_path(tag_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().tags().get(
                path=tag_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to get tag: {e}")

    def create_tag(self, workspace_path: str, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tag in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().tags().create(
                parent=workspace_path,
                body=tag_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to create tag: {e}")

    def update_tag(self, tag_path: str, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing tag."""
        account_id = self.extract_account_id_from_path(tag_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().tags().update(
                path=tag_path,
                body=tag_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to update tag: {e}")

    def list_triggers(self, workspace_path: str) -> List[Dict[str, Any]]:
        """List all triggers in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            response = self.service.accounts().containers().workspaces().triggers().list(
                parent=workspace_path
            ).execute()
            return response.get('trigger', [])
        except HttpError as e:
            raise Exception(f"Failed to list triggers: {e}")

    def create_trigger(self, workspace_path: str, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new trigger in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().triggers().create(
                parent=workspace_path,
                body=trigger_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to create trigger: {e}")

    def list_variables(self, workspace_path: str) -> List[Dict[str, Any]]:
        """List all variables in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            response = self.service.accounts().containers().workspaces().variables().list(
                parent=workspace_path
            ).execute()
            return response.get('variable', [])
        except HttpError as e:
            raise Exception(f"Failed to list variables: {e}")

    def get_variable(self, variable_path: str) -> Dict[str, Any]:
        """Get a specific variable's details."""
        account_id = self.extract_account_id_from_path(variable_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().variables().get(
                path=variable_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to get variable: {e}")

    def create_variable(self, workspace_path: str, variable_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new variable in a workspace."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().variables().create(
                parent=workspace_path,
                body=variable_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to create variable: {e}")

    def update_variable(self, variable_path: str, variable_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing variable."""
        account_id = self.extract_account_id_from_path(variable_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().workspaces().variables().update(
                path=variable_path,
                body=variable_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to update variable: {e}")

    def create_version(self, workspace_path: str, name: str, notes: str = "") -> Dict[str, Any]:
        """Create a new container version."""
        account_id = self.extract_account_id_from_path(workspace_path)
        self.validate_account_access(account_id)

        try:
            version_data = {
                "name": name,
                "notes": notes
            }
            return self.service.accounts().containers().workspaces().create_version(
                path=workspace_path,
                body=version_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to create version: {e}")

    def publish_version(self, version_path: str) -> Dict[str, Any]:
        """Publish a container version."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().versions().publish(
                path=version_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to publish version: {e}")

    def list_versions(self, container_path: str, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """List all versions of a container."""
        account_id = self.extract_account_id_from_path(container_path)
        self.validate_account_access(account_id)

        try:
            response = self.service.accounts().containers().version_headers().list(
                parent=container_path,
                includeDeleted=include_deleted
            ).execute()
            return response.get('containerVersionHeader', [])
        except HttpError as e:
            raise Exception(f"Failed to list versions: {e}")

    def get_version(self, version_path: str) -> Dict[str, Any]:
        """Get details of a specific container version."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().versions().get(
                path=version_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to get version: {e}")

    def get_live_version(self, container_path: str) -> Dict[str, Any]:
        """Get the currently published (live) version of a container."""
        account_id = self.extract_account_id_from_path(container_path)
        self.validate_account_access(account_id)

        try:
            result = self.service.accounts().containers().versions().live(
                parent=container_path
            ).execute()
            return result
        except HttpError as e:
            # Handle 404 specifically - no published version exists
            if e.resp.status == 404:
                raise Exception(
                    f"No published version found for container {container_path}. "
                    "Publish a version first using gtm_publish_container."
                )
            # Handle other HTTP errors
            raise Exception(f"Failed to get live version: {e}")

    def get_latest_version(self, container_path: str) -> Dict[str, Any]:
        """Get the latest version header of a container."""
        account_id = self.extract_account_id_from_path(container_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().version_headers().latest(
                parent=container_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to get latest version: {e}")

    def delete_version(self, version_path: str) -> None:
        """Delete (archive) a container version."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            self.service.accounts().containers().versions().delete(
                path=version_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to delete version: {e}")

    def undelete_version(self, version_path: str) -> Dict[str, Any]:
        """Restore a previously deleted (archived) container version."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().versions().undelete(
                path=version_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to undelete version: {e}")

    def update_version(self, version_path: str, version_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a container version's metadata (name, description, notes)."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().versions().update(
                path=version_path,
                body=version_data
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to update version: {e}")

    def set_latest_version(self, version_path: str) -> Dict[str, Any]:
        """Set a container version as the latest version."""
        account_id = self.extract_account_id_from_path(version_path)
        self.validate_account_access(account_id)

        try:
            return self.service.accounts().containers().versions().set_latest(
                path=version_path
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to set latest version: {e}")
