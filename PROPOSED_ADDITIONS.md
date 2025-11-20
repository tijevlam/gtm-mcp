# Proposed Additions to GTM MCP Server

## Executive Summary

This document outlines a comprehensive plan to add missing functionality to the gtm-mcp server, bringing it to feature parity and beyond with the reference stape-io implementation. The proposal is organized into phases to allow incremental implementation and testing.

## Design Philosophy

### Approach: Hybrid Model

We propose maintaining our current simple tool naming while adding comprehensive functionality:

**Option A: Keep Current Separate Tool Approach (RECOMMENDED)**
- Maintain backward compatibility with existing tools
- Add new tools for missing operations
- Easier for users to discover specific operations
- More explicit and self-documenting

**Option B: Adopt Action-Based Approach**
- Consolidate tools into resource-based tools with action parameters
- More similar to reference implementation
- Fewer total tools but more complex parameters

**Recommendation**: We recommend **Option A** for the following reasons:
1. Maintains backward compatibility with existing integrations
2. More intuitive for AI assistants to select the right tool
3. Clearer documentation and examples
4. Easier to extend incrementally

## Implementation Phases

### Phase 1: Complete Existing Resources (HIGH PRIORITY)

#### 1.1 Tags - Missing Operations
Add complete CRUD operations for tags:

```python
# New tools to add:
- gtm_delete_tag(tag_path)
- gtm_revert_tag(tag_path, fingerprint)
```

**Implementation Notes:**
- Add delete and revert methods to GTMClient
- Update tools.py with new handlers
- Add tool definitions to server.py

#### 1.2 Triggers - Missing Operations
Complete trigger management:

```python
# New tools to add:
- gtm_get_trigger(trigger_path)
- gtm_update_trigger(trigger_path, trigger_data, fingerprint)
- gtm_delete_trigger(trigger_path)
- gtm_revert_trigger(trigger_path, fingerprint)
```

#### 1.3 Variables - Missing Operations
Complete variable management:

```python
# New tools to add:
- gtm_update_variable(variable_path, variable_data, fingerprint)
- gtm_delete_variable(variable_path)
- gtm_revert_variable(variable_path, fingerprint)
```

#### 1.4 Containers - Missing Operations
Enhanced container management:

```python
# New tools to add:
- gtm_get_container(container_path)
- gtm_create_container(account_id, container_data)
- gtm_update_container(container_path, container_data, fingerprint)
- gtm_delete_container(container_path)
- gtm_get_container_snippet(container_path)
```

#### 1.5 Accounts - Missing Operations
Complete account management:

```python
# New tools to add:
- gtm_get_account(account_id)
- gtm_update_account(account_id, account_data, fingerprint)
```

**Estimated Effort**: 2-3 days
**Testing Required**: Unit tests for each new operation
**Dependencies**: None

### Phase 2: Workspace Management (HIGH PRIORITY)

Workspaces are critical for GTM workflow and currently missing entirely.

```python
# New tools to add:
- gtm_list_workspaces(container_path)
- gtm_get_workspace(workspace_path)
- gtm_create_workspace(container_path, workspace_name, description)
- gtm_update_workspace(workspace_path, workspace_data, fingerprint)
- gtm_delete_workspace(workspace_path)
- gtm_create_workspace_version(workspace_path, version_name, notes)
- gtm_sync_workspace(workspace_path)
```

**Implementation Notes:**
- Create new workspace management methods in GTMClient
- Update tools.py with workspace handlers
- Workspace operations are foundational for most GTM operations
- Consider making workspace_id optional in existing tools (use default workspace)

**Estimated Effort**: 2-3 days
**Testing Required**: Integration tests for workspace lifecycle
**Dependencies**: Phase 1 completion

### Phase 3: Version Management (HIGH PRIORITY)

Enhanced version control capabilities:

```python
# New tools to add:
- gtm_list_versions(container_path, include_deleted=False)
- gtm_get_version(version_path)
- gtm_get_live_version(container_path)
- gtm_get_latest_version(container_path)
- gtm_delete_version(version_path)
- gtm_undelete_version(version_path)
- gtm_update_version(version_path, version_data)
- gtm_set_latest_version(version_path)
```

**Implementation Notes:**
- Extend existing version handling in GTMClient
- Add version history tracking
- Support for version comparison (future enhancement)

**Estimated Effort**: 2-3 days
**Testing Required**: Version lifecycle tests
**Dependencies**: Phase 2 completion

### Phase 4: Folders (MEDIUM PRIORITY)

Organizational features for better resource management:

```python
# New tools to add:
- gtm_list_folders(workspace_path)
- gtm_get_folder(folder_path)
- gtm_create_folder(workspace_path, folder_name)
- gtm_update_folder(folder_path, folder_data, fingerprint)
- gtm_delete_folder(folder_path)
- gtm_revert_folder(folder_path, fingerprint)
- gtm_list_folder_entities(folder_path)
```

**Implementation Notes:**
- Folders help organize tags, triggers, and variables
- Support moving resources in/out of folders
- Add folder_id optional parameter to tag/trigger/variable creation

**Estimated Effort**: 2 days
**Testing Required**: Folder operations and entity organization
**Dependencies**: Phase 1 completion

### Phase 5: Built-in Variables (MEDIUM PRIORITY)

Enable GTM's built-in variables:

```python
# New tools to add:
- gtm_list_built_in_variables(workspace_path)
- gtm_enable_built_in_variables(workspace_path, variable_types)
- gtm_disable_built_in_variables(workspace_path, variable_types)
- gtm_revert_built_in_variable(workspace_path, variable_type, fingerprint)
```

**Built-in Variable Types to Support:**
- Page URL, Page Hostname, Page Path
- Referrer
- Click Element, Click Classes, Click ID, Click Target, Click URL
- Form Element, Form Classes, Form ID, Form Target, Form URL
- Error Message, Error URL, Error Line
- Container ID, Container Version
- Random Number
- And many more...

**Estimated Effort**: 1-2 days
**Testing Required**: Built-in variable activation tests
**Dependencies**: Phase 2 completion

### Phase 6: Environments (MEDIUM PRIORITY)

Preview and debugging environments:

```python
# New tools to add:
- gtm_list_environments(container_path)
- gtm_get_environment(environment_path)
- gtm_create_environment(container_path, environment_data)
- gtm_update_environment(environment_path, environment_data, fingerprint)
- gtm_delete_environment(environment_path)
- gtm_reauthorize_environment(environment_path, environment_data)
```

**Implementation Notes:**
- Environments enable preview mode and debugging
- Support for environment-specific URLs
- Authorization management for environments

**Estimated Effort**: 2 days
**Testing Required**: Environment lifecycle and authorization
**Dependencies**: Phase 3 completion

### Phase 7: Custom Templates (MEDIUM PRIORITY)

Support for custom tag and variable templates:

```python
# New tools to add:
- gtm_list_templates(workspace_path)
- gtm_get_template(template_path)
- gtm_create_template(workspace_path, template_data)
- gtm_update_template(template_path, template_data, fingerprint)
- gtm_delete_template(template_path)
- gtm_revert_template(template_path, fingerprint)
```

**Implementation Notes:**
- Templates allow custom tag/variable types
- Support sandboxed JavaScript templates
- Template gallery integration (optional)

**Estimated Effort**: 2-3 days
**Testing Required**: Template creation and usage
**Dependencies**: Phase 1 completion

### Phase 8: User Permissions (MEDIUM PRIORITY)

Multi-user access management:

```python
# New tools to add:
- gtm_list_user_permissions(account_id)
- gtm_get_user_permission(account_id, permission_id)
- gtm_create_user_permission(account_id, email, permissions)
- gtm_update_user_permission(account_id, permission_id, permissions)
- gtm_delete_user_permission(account_id, permission_id)
```

**Permission Levels:**
- Read: View only access
- Edit: Create and modify
- Approve: Approve changes
- Publish: Publish versions
- Admin: Full account access

**Estimated Effort**: 1-2 days
**Testing Required**: Permission management tests
**Dependencies**: Phase 1 completion

### Phase 9: Server-Side GTM Features (LOW PRIORITY)

Features specific to server-side Google Tag Manager:

#### 9.1 Clients
```python
- gtm_list_clients(workspace_path)
- gtm_get_client(client_path)
- gtm_create_client(workspace_path, client_data)
- gtm_update_client(client_path, client_data, fingerprint)
- gtm_delete_client(client_path)
- gtm_revert_client(client_path, fingerprint)
```

#### 9.2 Transformations
```python
- gtm_list_transformations(workspace_path)
- gtm_get_transformation(transformation_path)
- gtm_create_transformation(workspace_path, transformation_data)
- gtm_update_transformation(transformation_path, transformation_data, fingerprint)
- gtm_delete_transformation(transformation_path)
- gtm_revert_transformation(transformation_path, fingerprint)
```

#### 9.3 Destinations
```python
- gtm_list_destinations(account_id)
- gtm_get_destination(destination_path)
- gtm_link_destination(account_id, destination_data)
- gtm_update_destination(destination_path, destination_data)
- gtm_unlink_destination(destination_path)
```

#### 9.4 Gtag Configs
```python
- gtm_list_gtag_configs(workspace_path)
- gtm_get_gtag_config(config_path)
- gtm_create_gtag_config(workspace_path, config_data)
- gtm_update_gtag_config(config_path, config_data, fingerprint)
- gtm_delete_gtag_config(config_path)
```

**Estimated Effort**: 3-4 days
**Testing Required**: Server-side GTM container tests
**Dependencies**: Phases 1-3 completion
**Note**: Requires access to server-side GTM container for testing

### Phase 10: Security & Privacy Zones (LOW PRIORITY)

Advanced security features:

```python
# New tools to add:
- gtm_list_zones(workspace_path)
- gtm_get_zone(zone_path)
- gtm_create_zone(workspace_path, zone_data)
- gtm_update_zone(zone_path, zone_data, fingerprint)
- gtm_delete_zone(zone_path)
- gtm_revert_zone(zone_path, fingerprint)
```

**Implementation Notes:**
- Zones control which tags can fire on which pages
- Privacy and security feature for GDPR/CCPA compliance
- Complex configuration with boundaries and whitelists

**Estimated Effort**: 2-3 days
**Testing Required**: Zone rule evaluation
**Dependencies**: Phase 1 completion

### Phase 11: Advanced Container Operations (LOW PRIORITY)

Specialized container management:

```python
# New tools to add:
- gtm_combine_containers(from_container_path, to_container_path, settings)
- gtm_move_tag_id(container_path, tag_id, target_account_id, settings)
- gtm_lookup_container(destination_id)
```

**Implementation Notes:**
- Container combination for mergers/reorganization
- Tag ID migration between containers
- Container lookup by destination ID

**Estimated Effort**: 1-2 days
**Testing Required**: Container merge scenarios
**Dependencies**: Phase 1 completion

## Cross-Cutting Enhancements

### Enhancement 1: Pagination Support

Add pagination to all list operations:

```python
# Updated signatures:
- gtm_list_*(path, page=1, items_per_page=50)
```

**Implementation:**
- Add pagination helpers to gtm_client.py
- Return pagination metadata: total_count, page, items_per_page, has_next_page
- Default to reasonable page sizes (20-50 items)

### Enhancement 2: Fingerprint Management

Add fingerprint support for optimistic concurrency:

```python
# All update/delete operations should:
1. Fetch current resource to get fingerprint
2. Pass fingerprint in update/delete request
3. Handle fingerprint mismatch errors
```

### Enhancement 3: Batch Operations

Support batch operations for efficiency:

```python
# New tools:
- gtm_batch_create_tags(workspace_path, tags_data)
- gtm_batch_delete_tags(tag_paths)
- gtm_batch_update_tags(updates)
```

### Enhancement 4: Quick Preview

Add quick preview support:

```python
- gtm_quick_preview(workspace_path)
  Returns preview URL for testing changes without publishing
```

### Enhancement 5: Conflict Resolution

Add workspace conflict resolution:

```python
- gtm_get_workspace_status(workspace_path)
- gtm_resolve_workspace_conflict(workspace_path, resolution_strategy)
```

## Implementation Guidelines

### Code Organization

```
src/unboundai_gtm_mcp/
├── gtm_client.py          # Core API client (expand methods)
├── server.py              # Tool definitions (add new tools)
├── tools.py               # Tool implementations (add handlers)
├── helpers.py             # Helper functions (add new utilities)
├── validators.py          # Input validation (add validators)
├── constants.py           # Constants and enums
├── exceptions.py          # Custom exceptions
└── tests/
    ├── test_accounts.py
    ├── test_containers.py
    ├── test_tags.py
    ├── test_triggers.py
    ├── test_variables.py
    ├── test_workspaces.py
    ├── test_versions.py
    └── test_folders.py
```

### Testing Strategy

1. **Unit Tests**: Test each new tool in isolation
2. **Integration Tests**: Test tool combinations and workflows
3. **Regression Tests**: Ensure existing tools still work
4. **Manual Testing**: Real GTM account testing for critical paths

### Documentation Updates

For each phase, update:
1. README.md - Add new tools to available tools table
2. EXAMPLES.md - Add usage examples for new tools
3. API documentation - Document parameters and responses
4. Inline docstrings - Add comprehensive docstrings

### Backward Compatibility

- Keep all existing tool names and signatures
- Mark deprecated approaches in documentation
- Provide migration guide if needed

## Resource Requirements

### Development Time Estimate

| Phase | Days | Cumulative |
|-------|------|------------|
| Phase 1: Complete Existing | 3 | 3 |
| Phase 2: Workspaces | 3 | 6 |
| Phase 3: Versions | 3 | 9 |
| Phase 4: Folders | 2 | 11 |
| Phase 5: Built-in Variables | 2 | 13 |
| Phase 6: Environments | 2 | 15 |
| Phase 7: Templates | 3 | 18 |
| Phase 8: User Permissions | 2 | 20 |
| Phase 9: Server-Side GTM | 4 | 24 |
| Phase 10: Zones | 3 | 27 |
| Phase 11: Advanced Ops | 2 | 29 |
| **Total** | **29 days** | - |

### Testing Requirements

- GTM account with appropriate permissions
- Test containers for development and staging
- Server-side GTM container (for Phase 9)
- Multiple user accounts (for Phase 8 testing)

## Success Metrics

1. **Feature Parity**: 95%+ of stape-io functionality
2. **Test Coverage**: 80%+ code coverage
3. **Documentation**: All tools documented with examples
4. **Performance**: <500ms average response time
5. **Reliability**: <1% error rate in normal operations

## Rollout Plan

### Phase 1-3: Foundation (Weeks 1-2)
- Complete existing resources
- Add workspace management
- Enhance version control
- Release as v2.0.0

### Phase 4-6: Organization (Weeks 3-4)
- Add folders
- Add built-in variables
- Add environments
- Release as v2.1.0

### Phase 7-8: Advanced (Weeks 5-6)
- Add custom templates
- Add user permissions
- Release as v2.2.0

### Phase 9-11: Comprehensive (Weeks 7-8)
- Add server-side GTM features
- Add zones
- Add advanced container operations
- Release as v3.0.0

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking changes to existing tools | High | Maintain backward compatibility, version bumps |
| GTM API rate limits | Medium | Implement exponential backoff, caching |
| Server-side GTM access for testing | Medium | Partner with users who have sGTM |
| Complex error scenarios | Medium | Comprehensive error handling and logging |
| Documentation lag | Low | Write docs alongside code |

## Conclusion

This comprehensive plan will bring the gtm-mcp server to full feature parity with the reference implementation while maintaining its user-friendly design philosophy. The phased approach allows for incremental delivery of value while managing complexity and risk.

**Recommended Next Steps:**
1. Review and approve this proposal
2. Begin Phase 1 implementation
3. Set up testing infrastructure
4. Create detailed task breakdown for each phase
5. Establish review and release process
