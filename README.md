# GTM MCP Server

[![PyPI version](https://badge.fury.io/py/gtm-mcp.svg)](https://badge.fury.io/py/gtm-mcp)
[![Python Version](https://img.shields.io/pypi/pyversions/gtm-mcp.svg)](https://pypi.org/project/gtm-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that enables Claude to interact with Google Tag Manager.

## Table of Contents

- [Features](#features)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
- [Complete Setup Guide](#-complete-setup-guide)
  - [Part 1: Install the Package](#part-1-install-the-package)
  - [Part 2: Create Google Cloud OAuth Credentials](#part-2-create-google-cloud-oauth-credentials)
    - [Step 1: Create a Google Cloud Project](#step-1-create-a-google-cloud-project)
    - [Step 2: Enable Tag Manager API](#step-2-enable-tag-manager-api)
    - [Step 3: Configure OAuth Consent Screen](#step-3-configure-oauth-consent-screen)
    - [Step 4: Create OAuth Credentials](#step-4-create-oauth-credentials)
    - [Step 5: Save Your Credentials](#step-5-save-your-credentials)
  - [Part 3: Configure Claude Desktop](#part-3-configure-claude-desktop)
  - [Part 4: Restart and Authorize](#part-4-restart-and-authorize)
- [Available Tools](#%EF%B8%8F-available-tools)
- [How Authentication Works](#-how-authentication-works)
- [Upgrade](#upgrade)
- [Troubleshooting](#-troubleshooting)
- [Security Notes](#-security-notes)
- [Development](#-development)
  - [Running Tests](#running-tests)
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

## 📋 Complete Setup Guide
[⬆ top](#gtm-mcp-server)
### Part 1: Install the Package

```bash
pip install gtm-mcp
```

See [PyPi](https://pypi.org/project/gtm-mcp/)

---

### Part 2: Choose Your Authentication Method
[⬆ top](#gtm-mcp-server)

GTM MCP supports two authentication methods. Choose the one that best fits your needs:

#### **Method A: Application Default Credentials (Recommended for Servers)**

**Best for:**
- ✅ Server environments and automation
- ✅ No browser interaction required
- ✅ Flexible credential sources
- ✅ Better for CI/CD pipelines
- ✅ Works on Google Cloud (GCE, GKE, Cloud Run)

**Pros:**
- No OAuth consent screen setup required
- No browser popup for authorization
- Automatic credential discovery from multiple sources
- Automatic token refresh
- Works with gcloud CLI, service account files, or cloud environment

**Cons:**
- Requires initial credential setup (service account or gcloud CLI)
- Need to manually grant service account access to GTM

[→ Go to Application Default Credentials Setup](#application-default-credentials-setup-method-a)

---

#### **Method B: OAuth 2.0 (Original Method)**

**Best for:**
- ✅ Personal desktop use
- ✅ Interactive environments
- ✅ When you want user-level permissions

**Pros:**
- Uses your personal Google account
- Natural authorization flow
- Direct access through browser

**Cons:**
- Requires OAuth consent screen setup
- Requires browser interaction on first use
- More complex initial setup

[→ Go to OAuth 2.0 Setup](#oauth-20-setup-method-b)

---

### Application Default Credentials Setup (Method A)
[⬆ top](#gtm-mcp-server)

Application Default Credentials (ADC) is Google's recommended way to authenticate applications. It automatically discovers credentials from multiple sources in the following order:

1. **GOOGLE_APPLICATION_CREDENTIALS** environment variable pointing to a service account JSON file
2. **gcloud CLI** credentials (`gcloud auth application-default login`)
3. **Cloud environment** service accounts (GCE, GKE, Cloud Run, etc.)

Choose the option that works best for you:

#### Option 1: Service Account File (Most Common)

##### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown (top left)
3. Click **"New Project"**
4. Enter a project name (e.g., "GTM MCP Service")
5. Click **"Create"**
6. Wait for the project to be created and select it

##### Step 2: Enable Tag Manager API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Tag Manager API"**
3. Click on it and click **"Enable"**
4. Wait for it to enable (may take a minute)

##### Step 3: Create Service Account

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Fill in the service account details:
   - **Service account name**: gtm-mcp-service
   - **Service account ID**: (auto-filled)
   - **Description**: Service account for GTM MCP Server
4. Click **"Create and Continue"**
5. Skip the optional steps and click **"Done"**

##### Step 4: Create and Download Service Account Key

1. Click on the service account you just created
2. Go to the **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"**
4. Select **"JSON"** format
5. Click **"Create"**
6. The JSON file will download automatically
7. **Save this file securely** - you'll need its path later
8. **Copy the service account email** from the JSON file (looks like: `gtm-mcp-service@your-project.iam.gserviceaccount.com`)

##### Step 5: Grant Service Account Access to GTM

1. Go to [Google Tag Manager](https://tagmanager.google.com/)
2. Select your GTM account
3. Click **"Admin"** in the top navigation
4. Under "Account", click **"User Management"**
5. Click the **"+"** button to add a user
6. Enter the **service account email** from Step 4
7. Select appropriate permissions:
   - **Read**: For read-only access
   - **Edit**: For creating/modifying tags, triggers, variables
   - **Approve**: For publishing container versions
   - **Publish**: For full publishing rights
8. Click **"Invite"**

##### Step 6: Configure Claude Desktop (Service Account File)

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
        "GTM_AUTH_METHOD": "service_account",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/service-account-key.json"
      }
    }
  }
}
```

**Important**: Replace `/path/to/your/service-account-key.json` with the actual path to your downloaded JSON file.

**Example paths:**
- Linux/macOS: `/home/username/gtm-service-account.json`
- Windows: `C:\\Users\\YourName\\gtm-service-account.json`

---

#### Option 2: gcloud CLI Credentials (Simplest for Local Development)

If you have the Google Cloud SDK installed and want to use your own Google account credentials:

##### Step 1: Install Google Cloud SDK

If not already installed, follow the [Google Cloud SDK installation guide](https://cloud.google.com/sdk/docs/install).

##### Step 2: Authenticate with Application Default Credentials

```bash
gcloud auth application-default login
```

This will open a browser window to authenticate with your Google account and save credentials locally.

##### Step 3: Grant Your Account Access to GTM

Ensure your Google account has the appropriate permissions in Google Tag Manager (see Step 5 in Option 1, but use your Google account email instead of a service account email).

##### Step 4: Configure Claude Desktop (gcloud CLI)

Edit your Claude Desktop config file:

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "service_account"
      }
    }
  }
}
```

**Note**: No `GOOGLE_APPLICATION_CREDENTIALS` is needed when using gcloud CLI credentials.

---

#### Option 3: Cloud Environment (GCE, GKE, Cloud Run)

If you're running in a Google Cloud environment, ADC will automatically use the attached service account.

##### Step 1: Attach Service Account to Your Resource

When creating your GCE instance, GKE pod, or Cloud Run service, attach a service account with the necessary permissions.

##### Step 2: Grant Service Account Access to GTM

Follow Step 5 from Option 1 to grant the service account access to your GTM account.

##### Step 3: Configure Your Application

Set the environment variable:

```bash
GTM_AUTH_METHOD=service_account
```

No `GOOGLE_APPLICATION_CREDENTIALS` is needed - ADC will automatically discover the attached service account.

---

#### Restart and Test

1. **Restart Claude Desktop** completely
2. Ask Claude: "List my GTM accounts"
3. ADC will authenticate automatically - no browser popup needed!

[→ Skip to Available Tools](#%EF%B8%8F-available-tools)

---

### OAuth 2.0 Setup (Method B)
[⬆ top](#gtm-mcp-server)
#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown (top left)
3. Click **"New Project"**
4. Enter a project name (e.g., "My GTM MCP Server")
5. Click **"Create"**
6. Wait for the project to be created and select it

#### Step 2: Enable Tag Manager API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Tag Manager API"**
3. Click on it and click **"Enable"**
4. Wait for it to enable (may take a minute)

#### Step 3: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (unless you have a Google Workspace)
3. Click **"Create"**
4. Fill in required fields:
   - **App name**: My GTM MCP (or whatever you like)
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **"Save and Continue"**
6. Click **"Update"** then **"Save and Continue"**
7. Add your email as a **test user**
8.  Click **"Save and Continue"**

#### Step 4: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select **"Desktop app"** as the application type
4. Enter a name: "GTM MCP Desktop Client"
5. Click **"Create"**
6. **IMPORTANT**: A dialog appears with your credentials - **DO NOT CLOSE IT YET**

#### Step 5: Save Your Credentials

From the dialog that appeared:

1. Copy the **Client ID** (looks like: `123456789-abc123.apps.googleusercontent.com`)
2. Copy the **Client secret** (looks like: `GOCSPX-...`)
3. Note your **Project ID** from the Google Cloud Console (top bar, next to project name)
4. Save these somewhere safe - you'll need them in the next step

You can also download the JSON file, but you only need the three values above.

---

### Step 6: Configure Claude Desktop (OAuth 2.0)
[⬆ top](#gtm-mcp-server)
Edit your Claude Desktop config file:

- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Code**: `~/.claude.json`

Add your credentials:

```json
{
  "mcpServers": {
    "gtm-mcp": {
      "command": "gtm-mcp",
      "env": {
        "GTM_AUTH_METHOD": "oauth",
        "GTM_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GTM_CLIENT_SECRET": "GOCSPX-your-client-secret",
        "GTM_PROJECT_ID": "your-project-id"
      }
    }
  }
}
```

**Replace the values** with your actual credentials from Step 5.

> **Note**: 
> - If you have other MCP servers configured, just add the `"gtm-mcp"` entry to the existing `"mcpServers"` object.
> - The `GTM_AUTH_METHOD` can be omitted as `oauth` is the default for backward compatibility.

---

### Step 7: Restart and Authorize (OAuth 2.0)
[⬆ top](#gtm-mcp-server)
1. **Restart Claude Desktop** completely (close and reopen)

2. Ask Claude to use a GTM tool (e.g., "List my GTM accounts")

3. **First-time authorization** - a browser window will open automatically:
   - Sign in with your Google account
   - You'll see **"Google hasn't verified this app"** warning
   - Click **"Advanced"** → **"Go to [Your App Name] (unsafe)"**
   - This is safe because **you created the app yourself**
   - Grant the requested permissions
   - You'll see "The authentication flow has completed"
   - Return to Claude Desktop

4. Your authorization is saved locally - you won't need to do this again!

---

## 🛠️ Available Tools
[⬆ top](#gtm-mcp-server) </br>
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
| `gtm_create_variable` | Create a new variable (constant, data layer, cookie, URL, etc.) |
| `gtm_publish_container` | Create and publish a new container version |

---

## 🔐 How Authentication Works
[⬆ top](#gtm-mcp-server) </br>
This MCP server supports two authentication methods:

### Method A: Application Default Credentials (ADC)

With Application Default Credentials (ADC) authentication:

1. **ADC automatically discovers credentials** from multiple sources:
   - `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a service account JSON file
   - Google Cloud SDK credentials (`gcloud auth application-default login`)
   - Service account attached to GCE/GKE/Cloud Run instances
   - Other Google Cloud environments
2. **Grant the account access** to your GTM account
3. **Automatic authentication** - no browser interaction required
4. **Tokens are managed automatically** by Google's auth library

**Benefits:**
- ✅ No browser interaction required
- ✅ Perfect for server environments
- ✅ Automatic token refresh
- ✅ Flexible credential sources
- ✅ Works seamlessly in Google Cloud environments
- ✅ Simple for local development with gcloud CLI

**How it works:**
When you set `GTM_AUTH_METHOD=service_account`, the library uses `google.auth.default()` to automatically discover credentials. This is the same approach used by the official Google Analytics MCP server and is Google's recommended authentication method.

### Method B: OAuth 2.0 Authentication (Default)

With OAuth 2.0 authentication:

1. **You create OAuth credentials** in your own Google Cloud project
2. **You configure** those credentials in Claude Desktop
3. **First use**: Browser opens to authorize access to your GTM account
4. **Your tokens** are saved locally on your machine (`~/.gtm-mcp/token.json`) for future use

**Benefits:**
- ✅ You maintain full control over the OAuth app
- ✅ No shared credentials between users
- ✅ You can revoke access anytime
- ✅ Your credentials stay private
- ✅ Compliant with Google's OAuth policies

---
## Upgrade

Run `pip install --upgrade gtm-mcp`

---
## ❓ Troubleshooting
[⬆ top](#gtm-mcp-server)

### Application Default Credentials (ADC) Issues

#### "Failed to load Application Default Credentials" Error

**Problem**: The MCP server can't discover any credentials using ADC.

**Solution**: Choose one of these credential sources:

1. **Using a service account file:**
   - Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your service account JSON file
   - Ensure the path is absolute and points to a valid JSON file
   - On Windows, use double backslashes: `C:\\Users\\...`
   - Restart Claude Desktop after editing the config

2. **Using gcloud CLI:**
   - Run `gcloud auth application-default login`
   - Follow the browser flow to authenticate
   - Ensure your Google account has GTM access
   - Restart Claude Desktop

3. **Running on Google Cloud:**
   - Ensure your GCE/GKE/Cloud Run resource has a service account attached
   - Grant the service account access to your GTM account

#### "Service account has no access" Error

**Problem**: The service account or user account can't access your GTM account.

**Solution**:
1. Go to GTM → Admin → User Management
2. Verify the account email is listed with appropriate permissions
3. For service accounts: add the service account email from your JSON file
4. For gcloud CLI: add your Google account email
5. Grant at least "Read" permission (or higher based on your needs)

#### Which Authentication Method Am I Using?

Check your `claude_desktop_config.json`:
- If you see `GTM_AUTH_METHOD: "service_account"` → **Application Default Credentials (ADC)**
- If you see `GTM_CLIENT_ID`, `GTM_CLIENT_SECRET` → **OAuth 2.0**
- If no `GTM_AUTH_METHOD` is set → **OAuth 2.0** (default)

### OAuth 2.0 Issues

#### "Missing required OAuth credentials" Error

**Problem**: The MCP server can't find your OAuth credentials.

**Solution**: Make sure you:
- Set `GTM_AUTH_METHOD=oauth` (or omit it, as oauth is default)
- Set `GTM_CLIENT_ID`, `GTM_CLIENT_SECRET`, and `GTM_PROJECT_ID` correctly in `claude_desktop_config.json`
- Restarted Claude Desktop after editing the config
- Used the correct format (no extra quotes in JSON)
- The config file is valid JSON (use a JSON validator if unsure)

#### "Google hasn't verified this app" Warning

**Problem**: Google shows a security warning during first authorization.

**Solution**: This is **completely normal** for personal OAuth apps. Since you created the OAuth app yourself, Google shows this warning.

To proceed: Click **"Advanced"** → **"Go to [App Name] (unsafe)"**

This is safe because **you control the app**.

### General Issues

#### Can't Access GTM Accounts

**Possible causes**:
- Your Google account doesn't have access to any GTM accounts (OAuth)
- Service account doesn't have GTM permissions (Service Account)
- You didn't grant all requested permissions during authorization (OAuth)
- Tag Manager API isn't enabled in your Google Cloud project

**Solution**:
1. Verify your Google account or service account has GTM access
2. For OAuth: Re-authorize by deleting `~/.gtm-mcp/token.json` and trying again
3. For ADC/Service Account: Check GTM user management for the service account or user account email
4. Check that Tag Manager API is enabled in Google Cloud Console

### Connection Issues

**Debugging steps**:
1. Verify Claude Desktop is completely restarted
2. Check Claude Desktop logs for MCP server errors
3. Verify `gtm-mcp` command works: run `gtm-mcp` in terminal
4. Check your config file is valid JSON
5. Ensure all required environment variables are set correctly

### Package Not Found After Install

**Problem**: `gtm-mcp` command not found after installation.

**Solution**:
```bash
# Ensure pip install location is in PATH
pip install --user gtm-mcp

# Or use pipx for isolated installation
pipx install gtm-mcp
```

### Revoking Access

**For OAuth 2.0:**
1. Go to [Google Account Permissions](https://myaccount.google.com/permissions)
2. Find your app name in the list
3. Click **"Remove access"**
4. Delete the local token file: `rm ~/.gtm-mcp/token.json`

You can re-authorize anytime by using any GTM tool in Claude again.

**For Application Default Credentials (ADC):**

*If using a service account file:*
1. Go to GTM → Admin → User Management
2. Find the service account email
3. Click the remove button to revoke access
4. Optionally delete the service account key from Google Cloud Console

*If using gcloud CLI:*
1. Go to GTM → Admin → User Management
2. Find your Google account email
3. Click the remove button to revoke access
4. Optionally revoke ADC locally: `gcloud auth application-default revoke`

---

## 🔒 Security Notes
[⬆ top](#gtm-mcp-server)

### For OAuth 2.0:
- **Your OAuth credentials are yours alone** - keep them private
- **Never share your Client Secret** - treat it like a password
- Your access tokens are stored locally: `~/.gtm-mcp/token.json`
- You can regenerate credentials anytime in Google Cloud Console
- You can revoke access anytime from your Google account settings

### For Application Default Credentials (ADC):
- **Keep your JSON key file secure** - it provides full access
- **Never commit the JSON file to version control** - add it to `.gitignore`
- **Use restrictive file permissions** - `chmod 600 service-account.json` on Unix/Linux
- Store the file in a secure location with limited access
- You can create new keys and delete old ones in Google Cloud Console
- Regularly rotate service account keys for better security

### General:
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
see [LICENSE](https://github.com/paolobtl/gtm-mcp/blob/main/LICENSE) file for details

---

## 🤝 Contributing
[⬆ top](#gtm-mcp-server)
Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For bugs and feature requests, please [open an issue](https://github.com/paolobtl/gtm-mcp/issues).

---

## 🆘 Getting Help
[⬆ top](#gtm-mcp-server)
If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Review Claude Desktop logs for error messages
3. Verify your Google Cloud project has Tag Manager API enabled
4. Ensure environment variables are set correctly in the config
5. [Open an issue](https://github.com/paolobtl/gtm-mcp/issues) on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Error messages from Claude Desktop logs
   - Steps to reproduce the issue

---
