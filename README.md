# GTM MCP Server

[![PyPI version](https://badge.fury.io/py/gtm-mcp.svg)](https://badge.fury.io/py/gtm-mcp)
[![Python Version](https://img.shields.io/pypi/pyversions/gtm-mcp.svg)](https://pypi.org/project/gtm-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that enables Claude to interact with Google Tag Manager.

## Table of Contents

- [Features](#features)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
- [Setup Instructions](#-setup-instructions)
  - [Configure Python](#configure-python)
  - [Enable Tag Manager API](#enable-tag-manager-api)
  - [Configure Credentials](#configure-credentials)
  - [Configure Claude Desktop](#configure-claude-desktop)
- [Available Tools](#%EF%B8%8F-available-tools)
- [Troubleshooting](#-troubleshooting)
- [Security Notes](#-security-notes)
- [Development](#-development)
- [License](#-license)
- [Contributing](#-contributing)
- [Getting Help](#-getting-help)


## Features
[⬆ top](#gtm-mcp-server)
- List GTM accounts and containers
- Manage tags, triggers, and variables
- Create and publish container versions
- Full workspace management

---

## 🚀 Quick Start
[⬆ top](#gtm-mcp-server)

### Prerequisites

- Python 3.10 or higher
- Claude Desktop (or any MCP-compatible client like Cursor)
- A Google account with access to Google Tag Manager

---

## 🔧 Setup Instructions
[⬆ top](#gtm-mcp-server)

### Configure Python

Install the package using pip or pipx:

```bash
pip install gtm-mcp
```

See [PyPi](https://pypi.org/project/gtm-mcp/)

---

### Enable Tag Manager API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Go to **"APIs & Services"** → **"Library"**
4. Search for **"Tag Manager API"**
5. Click on it and click **"Enable"**

---

### Configure Credentials

This server uses [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc) for authentication. You need to set up credentials that have access to your Google Tag Manager accounts.

#### Step 1: Create a Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **"APIs & Services"** → **"Credentials"**
3. Click **"Create Credentials"** → **"Service Account"**
4. Fill in the service account details:
   - **Service account name**: gtm-mcp-service
   - **Description**: Service account for GTM MCP Server
5. Click **"Create and Continue"**
6. Skip optional steps and click **"Done"**

#### Step 2: Create and Download Service Account Key

1. Click on the service account you just created
2. Go to the **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"**
4. Select **"JSON"** format
5. Click **"Create"**
6. The JSON file will download automatically
7. **Save this file securely** - you'll need its path later
8. **Copy the service account email** (looks like: `gtm-mcp-service@your-project.iam.gserviceaccount.com`)

#### Step 3: Grant Service Account Access to GTM

1. Go to [Google Tag Manager](https://tagmanager.google.com/)
2. Select your GTM account
3. Click **"Admin"** in the top navigation
4. Under "Account", click **"User Management"**
5. Click the **"+"** button to add a user
6. Enter the **service account email** from Step 2
7. Select appropriate permissions:
   - **Read**: For read-only access
   - **Edit**: For creating/modifying tags, triggers, variables
   - **Approve**: For publishing container versions
   - **Publish**: For full publishing rights
8. Click **"Invite"**

---

### Configure Claude Desktop

Edit your Claude Desktop config file:

- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add your configuration:

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/service-account-key.json",
        "GOOGLE_PROJECT_ID": "your-project-id"
      }
    }
  }
}
```

**Important**: Replace the values with your actual paths and project ID.

**Example paths:**
- Linux/macOS: `/home/username/gtm-service-account.json`
- Windows: `C:\\Users\\YourName\\gtm-service-account.json`

**To find your Project ID:**
- Look in the Google Cloud Console top bar, next to your project name
- Or find it in your service account JSON file under the `"project_id"` field

---

### Try It Out

1. **Restart Claude Desktop** completely (close and reopen)
2. Ask Claude: "List my GTM accounts"
3. Authentication will happen automatically using the service account credentials!

---

## 🛠️ Available Tools
[⬆ top](#gtm-mcp-server)

Once configured, Claude will have access to these GTM tools:

| Tool | Description |
|------|-------------|
| `gtm_list_accounts` | List all your GTM accounts |
| `gtm_list_containers` | List containers in an account |
| `gtm_list_tags` | List tags in a workspace |
| `gtm_get_tag` | Get detailed configuration of a specific tag |
| `gtm_create_tag` | Create a new tag |
| `gtm_update_tag` | Update an existing tag |
| `gtm_list_triggers` | List triggers in a workspace |
| `gtm_create_trigger` | Create a new trigger |
| `gtm_list_variables` | List variables in a workspace |
| `gtm_get_variable` | Get detailed configuration of a specific variable |
| `gtm_create_variable` | Create a new variable (constant, data layer, cookie, URL, etc.) |
| `gtm_publish_container` | Create and publish a new container version |
| `gtm_list_versions` | List all versions of a container |
| `gtm_get_version` | Get detailed information about a specific version |
| `gtm_get_live_version` | Get the currently published (live) version |
| `gtm_get_latest_version` | Get the latest version (may not be published) |
| `gtm_delete_version` | Delete (archive) a container version |
| `gtm_undelete_version` | Restore a deleted version |
| `gtm_update_version` | Update version metadata (name, description, notes) |
| `gtm_set_latest_version` | Mark a version as the latest |

---

## ❓ Troubleshooting
[⬆ top](#gtm-mcp-server)

### "Missing required environment variable" Error

**Problem**: The MCP server can't find the required environment variables.

**Solution**:
1. Ensure both `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_PROJECT_ID` are set in your Claude Desktop config
2. Verify the path to your service account JSON file is correct and absolute
3. On Windows, use double backslashes: `C:\\Users\\...`
4. Restart Claude Desktop after editing the config

### "Failed to load Application Default Credentials" Error

**Problem**: The credentials file cannot be loaded or is invalid.

**Solution**:
1. Verify the service account JSON file exists at the specified path
2. Check that the JSON file is valid and not corrupted
3. Ensure the file has proper read permissions
4. Try downloading a new key from Google Cloud Console

### "Service account has no access" Error

**Problem**: The service account doesn't have permission to access your GTM account.

**Solution**:
1. Go to GTM → Admin → User Management
2. Verify the service account email is listed with appropriate permissions
3. Grant at least "Read" permission (or higher based on your needs)

### Can't Access GTM Accounts

**Possible causes**:
- Service account doesn't have GTM permissions
- Tag Manager API isn't enabled in your Google Cloud project
- Wrong service account email was added to GTM

**Solution**:
1. Verify Tag Manager API is enabled in Google Cloud Console
2. Check that the service account email is added to your GTM account
3. Ensure proper permissions are granted in GTM User Management

### Package Not Found After Install

**Problem**: `gtm-mcp` command not found after installation.

**Solution**:
```bash
# Ensure pip install location is in PATH
pip install --user gtm-mcp

# Or use pipx for isolated installation
pipx install gtm-mcp
```

---

## 🔒 Security Notes
[⬆ top](#gtm-mcp-server)

- **Keep your JSON key file secure** - it provides full access to whatever permissions you've granted
- **Never commit the JSON file to version control** - add it to `.gitignore`
- **Use restrictive file permissions** - `chmod 600 service-account.json` on Unix/Linux
- Store the file in a secure location with limited access
- You can create new keys and delete old ones in Google Cloud Console
- Regularly rotate service account keys for better security
- This server only accesses GTM - no other Google services
- Credentials are only used for Google Tag Manager API authentication
- No credentials are sent to any third-party services

---

## 💻 Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

---

## 📝 License
[⬆ top](#gtm-mcp-server)

See [LICENSE](https://github.com/tijevlam/gtm-mcp/blob/main/LICENSE) file for details

---

## 🤝 Contributing
[⬆ top](#gtm-mcp-server)

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For bugs and feature requests, please [open an issue](https://github.com/tijevlam/gtm-mcp/issues).

---

## 🆘 Getting Help
[⬆ top](#gtm-mcp-server)

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Review Claude Desktop logs for error messages
3. Verify your Google Cloud project has Tag Manager API enabled
4. Ensure environment variables are set correctly in the config
5. [Open an issue](https://github.com/tijevlam/gtm-mcp/issues) on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Error messages from Claude Desktop logs
   - Steps to reproduce the issue

---
