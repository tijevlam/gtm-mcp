# PyPI Deployment Guide for gtm-mcp

This guide explains how to build and deploy the `gtm-mcp` package to PyPI.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10 or higher** installed
2. **Poetry** installed (`pip install poetry`)
3. **PyPI Account**: Register at [https://pypi.org/account/register/](https://pypi.org/account/register/)
4. **TestPyPI Account** (optional, for testing): Register at [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)

## Step 1: Configure PyPI API Token

For security, PyPI recommends using API tokens instead of passwords.

### Create a PyPI API Token

1. Log in to [PyPI](https://pypi.org/)
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Give it a name (e.g., "gtm-mcp-upload")
5. Select scope:
   - **First upload**: "Entire account"
   - **After first upload**: Limit to the "gtm-mcp" project
6. Copy the token (starts with `pypi-`)
7. **IMPORTANT**: Save it securely - you can't view it again!

### Configure Poetry with Your Token

```bash
poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcC...your-token-here
```

### (Optional) Configure TestPyPI Token

For testing before production:

1. Create a token at [TestPyPI](https://test.pypi.org/)
2. Configure it:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-AgEIcHlwaS5vcmcC...your-test-token-here
```

## Step 2: Update Version Number

Before each release, update the version in `pyproject.toml`:

```toml
[tool.poetry]
version = "0.1.0"  # Update this
```

Or use Poetry's version command:

```bash
# Bump patch version (0.0.1 → 0.0.2)
poetry version patch

# Bump minor version (0.0.1 → 0.1.0)
poetry version minor

# Bump major version (0.0.1 → 1.0.0)
poetry version major

# Set specific version
poetry version 1.2.3
```

## Step 3: Build the Package

Clean any previous builds and create fresh distribution files:

```bash
# Clean previous builds
rm -rf dist/

# Build the package
poetry build
```

This creates two files in the `dist/` directory:
- `gtm_mcp-X.Y.Z-py3-none-any.whl` (wheel format)
- `gtm_mcp-X.Y.Z.tar.gz` (source distribution)

## Step 4: (Optional) Test on TestPyPI

Before publishing to the real PyPI, test your package:

```bash
# Upload to TestPyPI
poetry publish -r testpypi

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gtm-mcp
```

Note: `--extra-index-url https://pypi.org/simple/` allows pip to fetch dependencies from the real PyPI.

## Step 5: Publish to PyPI

When you're ready to publish to the production PyPI:

```bash
poetry publish
```

You'll see output like:

```
Publishing gtm-mcp (0.1.0) to PyPI
 - Uploading gtm_mcp-0.1.0-py3-none-any.whl 100%
 - Uploading gtm_mcp-0.1.0.tar.gz 100%
```

## Step 6: Verify Installation

After publishing, test that your package can be installed:

```bash
# Install from PyPI
pip install gtm-mcp

# Verify the command works
gtm-mcp --help

# Check installed version
pip show gtm-mcp
```

## Step 7: Create a GitHub Release (Recommended)

After publishing to PyPI, create a corresponding GitHub release:

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v0.1.0` (must match PyPI version)
4. Release title: `v0.1.0` or descriptive name
5. Describe the changes in this release
6. Click "Publish release"

## Troubleshooting

### Error: "File already exists"

PyPI doesn't allow re-uploading the same version. You must:
1. Bump the version number
2. Rebuild with `poetry build`
3. Publish again

### Error: "Invalid credentials"

- Check your API token is correct
- Verify the token hasn't expired
- Make sure you ran: `poetry config pypi-token.pypi your-token`

### Error: "403 Forbidden"

- First upload: Use a token with "Entire account" scope
- Subsequent uploads: Token must have access to the project

### Package Not Found After Upload

- Wait a few minutes - PyPI indexing takes time
- Check [https://pypi.org/project/gtm-mcp/](https://pypi.org/project/gtm-mcp/)
- Clear pip cache: `pip cache purge`

### Import Errors After Installation

Verify your package structure:
- Source code should be in `src/gtm_mcp/`
- `__init__.py` must exist in `src/gtm_mcp/`
- Check `packages` in `pyproject.toml`

## Automation (Optional)

### GitHub Actions

The repository includes two GitHub Actions workflows:

#### 1. Automatic Build and Test (`.github/workflows/build-test.yml`)

Automatically tests the package build on multiple Python versions (3.10, 3.11, 3.12, 3.13) for every push and pull request.

#### 2. Publish to PyPI (`.github/workflows/publish-to-pypi.yml`)

Automatically publishes to PyPI when you create a GitHub release, or manually via workflow dispatch.

**Setup GitHub Secrets:**

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following secrets:

   - **PYPI_TOKEN**: Your PyPI API token (required for production publishing)
     - Token from https://pypi.org/manage/account/token/
   
   - **TESTPYPI_TOKEN**: Your TestPyPI API token (optional, for testing)
     - Token from https://test.pypi.org/manage/account/token/

**Usage:**

- **Automatic publish**: Create a GitHub release (tag format: `v0.1.0`), and the workflow will automatically build and publish to PyPI
- **Manual publish**: Go to Actions → "Publish to PyPI" → "Run workflow" and choose target (pypi or testpypi)

**Creating a GitHub Release:**

1. Go to your repository → Releases → "Draft a new release"
2. Click "Choose a tag" and create a new tag (e.g., `v0.1.0`)
3. Fill in release title and description
4. Click "Publish release"
5. The workflow will automatically trigger and publish to PyPI

## Best Practices

1. **Version Control**: Always commit version changes before publishing
2. **Changelog**: Maintain a CHANGELOG.md documenting all changes
3. **Testing**: Test on TestPyPI first for major releases
4. **Semantic Versioning**: Follow [semver](https://semver.org/)
   - MAJOR: Incompatible API changes
   - MINOR: New backwards-compatible functionality
   - PATCH: Backwards-compatible bug fixes
5. **Git Tags**: Tag releases in Git to match PyPI versions
6. **Documentation**: Update README.md with installation instructions

## Quick Reference Commands

```bash
# Check current version
poetry version

# Bump version (patch/minor/major)
poetry version patch

# Build
rm -rf dist/ && poetry build

# Test on TestPyPI
poetry publish -r testpypi

# Publish to PyPI
poetry publish

# Verify installation
pip install gtm-mcp --upgrade
gtm-mcp --help
```

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

## Support

If you encounter issues:
1. Check [Poetry Troubleshooting](https://python-poetry.org/docs/faq/)
2. Verify [PyPI Status](https://status.python.org/)
3. Open an issue in the GitHub repository
