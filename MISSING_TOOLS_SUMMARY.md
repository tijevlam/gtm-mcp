# Missing Tools - Quick Reference

## Summary
Our gtm-mcp implementation currently has **12 tools** covering basic GTM operations. The reference stape-io implementation has **19 tool categories** with **100+ operations**. This document provides a quick reference for what's missing.

## Missing by Category

### 🔴 Critical Missing (Complete Resource Types)
These entire resource types are not yet supported:

| Resource | Operations | Priority | Use Case |
|----------|-----------|----------|----------|
| **Workspaces** | 8 operations | 🔥 HIGH | Essential for GTM workflow |
| **Folders** | 7 operations | ⭐ MEDIUM | Organization of resources |
| **Built-in Variables** | 4 operations | ⭐ MEDIUM | Quick access to common variables |
| **Environments** | 6 operations | ⭐ MEDIUM | Preview and debugging |
| **Templates** | 6 operations | ⭐ MEDIUM | Custom tag/variable types |
| **User Permissions** | 5 operations | ⭐ MEDIUM | Multi-user management |
| **Clients** | 6 operations | 🔵 LOW | Server-side GTM only |
| **Transformations** | 6 operations | 🔵 LOW | Server-side GTM only |
| **Destinations** | 5 operations | 🔵 LOW | Server-side GTM only |
| **Gtag Configs** | 5 operations | 🔵 LOW | Google tag configs |
| **Zones** | 6 operations | 🔵 LOW | Security/privacy features |

### 🟡 Missing Operations on Existing Resources

#### Accounts (Currently: list only)
- ❌ `get` - Get account details
- ❌ `update` - Update account settings

#### Containers (Currently: list only)
- ❌ `get` - Get container details
- ❌ `create` - Create container
- ❌ `update` - Update container
- ❌ `delete` - Remove container
- ❌ `snippet` - Get snippet code
- ❌ `combine` - Merge containers
- ❌ `lookup` - Lookup by destination
- ❌ `moveTagId` - Move tag ID

#### Tags (Currently: list, get, create, update)
- ❌ `delete` - Remove tag
- ❌ `revert` - Revert changes

#### Triggers (Currently: list, create)
- ❌ `get` - Get trigger details
- ❌ `update` - Update trigger
- ❌ `delete` - Remove trigger
- ❌ `revert` - Revert changes

#### Variables (Currently: list, get, create)
- ❌ `update` - Update variable
- ❌ `delete` - Remove variable
- ❌ `revert` - Revert changes

#### Versions (Currently: create, publish combined)
- ❌ `get` - Get version details
- ❌ `list` - List all versions
- ❌ `live` - Get published version
- ❌ `latest` - Get latest version
- ❌ `delete` - Remove version
- ❌ `undelete` - Restore version
- ❌ `update` - Update version metadata
- ❌ `setLatest` - Mark as latest

## Missing by Priority

### 🔥 HIGH PRIORITY (Must Have)
These are critical for basic GTM management:

1. **Delete Operations** (tags, triggers, variables)
2. **Update Operations** (triggers, variables)
3. **Get Operations** (individual triggers)
4. **Workspaces** (create, list, manage)
5. **Container Management** (get, create, update, delete)
6. **Version Management** (list, get, better control)

### ⭐ MEDIUM PRIORITY (Should Have)
These enhance usability significantly:

1. **Folders** (organize resources)
2. **Built-in Variables** (quick setup)
3. **Environments** (preview/debug)
4. **Templates** (custom types)
5. **User Permissions** (collaboration)
6. **Revert Operations** (undo changes)

### 🔵 LOW PRIORITY (Nice to Have)
These are specialized or advanced features:

1. **Server-Side GTM** (clients, transformations, destinations)
2. **Zones** (privacy features)
3. **Gtag Configs** (specialized configs)
4. **Advanced Container Ops** (combine, moveTagId)

## Implementation Recommendation

### Immediate (Week 1-2)
```
✅ Phase 1: Complete existing resources
   - Add delete/update/revert for tags, triggers, variables
   - Add container management operations
   - Add account get/update

✅ Phase 2: Workspaces
   - Full workspace lifecycle management
   - Critical for proper GTM workflow
```

### Short-term (Week 3-4)
```
✅ Phase 3: Version management
   - List, get, and manage versions properly
   - Better control over publishing

✅ Phase 4: Folders
   - Organize tags, triggers, variables
   - Improves user experience
```

### Medium-term (Week 5-8)
```
✅ Phase 5-8: Enhanced features
   - Built-in variables
   - Environments
   - Custom templates
   - User permissions
```

### Long-term (Week 9+)
```
✅ Phase 9-11: Advanced features
   - Server-side GTM support
   - Zones
   - Advanced container operations
```

## Tool Count Comparison

| Implementation | Tool Count | Coverage |
|----------------|------------|----------|
| **Current (ours)** | 12 tools | ~15% of operations |
| **Reference (stape-io)** | 19 categories | 100% coverage |
| **Proposed (after all phases)** | 100+ tools | 100% coverage |

## Key Architectural Differences

| Aspect | Current | Reference | Proposed |
|--------|---------|-----------|----------|
| **Tool Design** | One tool per operation | Action-based tools | One tool per operation |
| **Pagination** | None | Yes (page, itemsPerPage) | Yes |
| **Fingerprints** | Not used | Yes (concurrency control) | Yes |
| **Error Handling** | Basic | Comprehensive | Comprehensive |
| **Revert Support** | None | Yes | Yes |

## Quick Stats

- **Missing Resource Types**: 11 complete categories
- **Missing Operations**: 85+ operations
- **Estimated Implementation**: 29 days (6 weeks full-time)
- **Estimated Tools to Add**: 90+ new tools

## Next Steps

1. ✅ Review analysis documents
2. ⬜ Approve implementation plan
3. ⬜ Begin Phase 1 development
4. ⬜ Set up comprehensive testing
5. ⬜ Update documentation
6. ⬜ Release incremental versions

---

**See detailed documents:**
- `MISSING_TOOLS_ANALYSIS.md` - Complete analysis
- `PROPOSED_ADDITIONS.md` - Detailed implementation plan
