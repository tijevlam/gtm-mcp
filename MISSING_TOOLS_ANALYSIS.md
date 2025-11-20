# Missing Tools Analysis

## Overview
This document compares the current gtm-mcp implementation with the stape-io/google-tag-manager-mcp-server reference implementation to identify missing functionality.

## Current Implementation (tijevlam/gtm-mcp)

### Available Tools (12 tools)
1. `gtm_list_accounts` - List all GTM accounts
2. `gtm_list_containers` - List containers in an account
3. `gtm_list_tags` - List tags in a workspace
4. `gtm_get_tag` - Get detailed tag configuration
5. `gtm_create_tag` - Create a new tag
6. `gtm_update_tag` - Update an existing tag
7. `gtm_list_triggers` - List triggers in a workspace
8. `gtm_create_trigger` - Create a new trigger
9. `gtm_list_variables` - List variables in a workspace
10. `gtm_get_variable` - Get detailed variable configuration
11. `gtm_create_variable` - Create a new variable
12. `gtm_publish_container` - Create and publish container version

## Reference Implementation (stape-io/google-tag-manager-mcp-server)

### Available Tool Categories (19 tool categories)
The stape-io implementation uses a unified approach where each tool supports multiple actions through an `action` parameter:

1. **gtm_account** - Account operations (get, list, update)
2. **gtm_built_in_variable** - Built-in variable operations (create, list, remove, revert)
3. **gtm_client** - Server-side client operations (create, get, list, update, remove, revert)
4. **gtm_container** - Container operations (create, get, list, update, remove, combine, lookup, moveTagId, snippet)
5. **gtm_destination** - Destination operations (create, get, list, update, remove)
6. **gtm_environment** - Environment operations (create, get, list, update, remove, reauthorize)
7. **gtm_folder** - Folder operations (create, get, list, update, remove, revert, entities)
8. **gtm_gtag_config** - Gtag config operations (create, get, list, update, remove)
9. **gtm_tag** - Tag operations (create, get, list, update, remove, revert)
10. **gtm_template** - Custom template operations (create, get, list, update, remove, revert)
11. **gtm_transformation** - Transformation operations (create, get, list, update, remove, revert)
12. **gtm_trigger** - Trigger operations (create, get, list, update, remove, revert)
13. **gtm_user_permission** - User permission operations (create, get, list, update, remove)
14. **gtm_variable** - Variable operations (create, get, list, update, remove, revert)
15. **gtm_version** - Version operations (get, live, publish, remove, setLatest, undelete, update)
16. **gtm_version_header** - Version header operations (list, latest)
17. **gtm_workspace** - Workspace operations (create, get, list, update, remove, quick_preview, resolve_conflict, sync, create_version)
18. **gtm_zone** - Zone operations (create, get, list, update, remove, revert)
19. **removeMCPServerData** - Remove OAuth data

## Missing Functionality

### 1. Missing Resource Types (Completely New)
These resource types are not supported at all in our current implementation:

- **Built-in Variables** - Enable/disable GTM built-in variables (e.g., Click ID, Page URL, etc.)
- **Clients** - Server-side GTM clients for handling incoming requests
- **Destinations** - Destination configurations (for server-side GTM)
- **Environments** - GTM environments (Preview, Debug, etc.)
- **Folders** - Organize tags, triggers, and variables into folders
- **Gtag Configs** - Google tag configuration objects
- **Templates** - Custom tag/variable templates
- **Transformations** - Server-side transformations
- **User Permissions** - Manage user access to GTM accounts/containers
- **Zones** - Security/privacy zones for controlling tag behavior

### 2. Missing Operations on Existing Resources

#### Accounts
- ❌ `get` - Get specific account details
- ❌ `update` - Update account settings

#### Containers
- ❌ `get` - Get specific container details  
- ❌ `create` - Create new container
- ❌ `update` - Update container settings
- ❌ `remove` - Delete container
- ❌ `combine` - Combine two containers
- ❌ `lookup` - Lookup container by destination ID
- ❌ `moveTagId` - Move tag ID between containers
- ❌ `snippet` - Get container snippet code

#### Tags
- ❌ `remove` - Delete tag
- ❌ `revert` - Revert tag to previous version

#### Triggers
- ❌ `get` - Get specific trigger details
- ❌ `update` - Update existing trigger
- ❌ `remove` - Delete trigger
- ❌ `revert` - Revert trigger to previous version

#### Variables
- ❌ `update` - Update existing variable
- ❌ `remove` - Delete variable
- ❌ `revert` - Revert variable to previous version

#### Versions
- ❌ `get` - Get specific version details
- ❌ `live` - Get live/published version
- ❌ `remove` - Delete version
- ❌ `setLatest` - Set as latest version
- ❌ `undelete` - Restore deleted version
- ❌ `update` - Update version metadata
- ❌ List version headers
- ❌ Get latest version

#### Workspaces
- ❌ `create` - Create workspace
- ❌ `get` - Get workspace details
- ❌ `list` - List all workspaces
- ❌ `update` - Update workspace
- ❌ `remove` - Delete workspace
- ❌ `quick_preview` - Generate quick preview
- ❌ `resolve_conflict` - Resolve workspace conflicts
- ❌ `sync` - Sync workspace with container
- ❌ `create_version` - Create version from workspace

### 3. Missing Features

#### Pagination
- Reference implementation has proper pagination support with `page` and `itemsPerPage` parameters
- Our implementation lists all items without pagination options

#### Fingerprint Management
- Reference implementation uses fingerprints for optimistic concurrency control
- Our implementation doesn't handle fingerprints for updates

#### Revert Operations
- Reference implementation supports reverting changes for most resources
- Our implementation has no revert functionality

#### Error Handling
- Reference implementation has standardized error response format
- Our implementation has basic error handling

## Architecture Differences

### Current Implementation (Separate Tools)
- Each operation is a separate tool (e.g., `gtm_create_tag`, `gtm_update_tag`)
- Total of 12 distinct tools
- Simple to understand but more tools to maintain

### Reference Implementation (Action-Based)
- Resources grouped by type with an `action` parameter
- Total of 19 tool categories with multiple actions each
- More flexible and easier to extend

## Summary Statistics

| Metric | Current | Reference | Missing |
|--------|---------|-----------|---------|
| Total Tool Categories | 12 separate tools | 19 tool categories | 7+ new categories |
| Total Operations | ~15 operations | 100+ operations | 85+ operations |
| Resource Types | 4 types (accounts, containers, tags, triggers, variables) | 14 types | 10 new types |
| Advanced Features | Basic CRUD | Full CRUD + revert, versioning, pagination | Most advanced features |

## Priority Assessment

### High Priority (Core Functionality)
1. **Workspaces** - Critical for proper GTM workflow
2. **Delete Operations** - Remove tags, triggers, variables
3. **Update Operations** - Update triggers and variables
4. **Get Operations** - Get individual trigger details
5. **Container Management** - Get, create, update containers
6. **Version Management** - Better version control operations
7. **Folders** - Organization functionality

### Medium Priority (Enhanced Functionality)
1. **Built-in Variables** - Convenient for common variables
2. **Environments** - Preview/debug functionality
3. **User Permissions** - Multi-user management
4. **Templates** - Custom template support
5. **Revert Operations** - Undo changes

### Low Priority (Advanced/Server-Side)
1. **Clients** - Server-side GTM only
2. **Destinations** - Server-side GTM only
3. **Transformations** - Server-side GTM only
4. **Zones** - Advanced privacy features
5. **Gtag Configs** - Specialized use case

## Recommendations

1. **Immediate**: Add missing CRUD operations (delete, update, get) for existing resources
2. **Short-term**: Add workspace and folder management
3. **Medium-term**: Add built-in variables, environments, and templates
4. **Long-term**: Add server-side GTM features (clients, destinations, transformations)
5. **Throughout**: Implement pagination, fingerprint management, and revert operations
