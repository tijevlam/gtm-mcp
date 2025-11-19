# PyPI Publishing Checklist

Use this checklist when you're ready to publish gtm-mcp to PyPI.

## Pre-Publishing Checklist

### Code & Quality
- [ ] All code changes are committed to git
- [ ] All tests pass (if applicable)
- [ ] Code has been reviewed
- [ ] No security vulnerabilities present
- [ ] Documentation is up to date

### Version & Metadata
- [ ] Version number updated in `pyproject.toml`
- [ ] Version follows semantic versioning (MAJOR.MINOR.PATCH)
- [ ] `CHANGES.md` updated with release notes for this version
- [ ] README.md reflects current functionality
- [ ] All metadata in `pyproject.toml` is accurate

### Build & Test
- [ ] Clean build completes successfully: `rm -rf dist/ && poetry build`
- [ ] Both artifacts exist in `dist/`:
  - [ ] `gtm_mcp-X.Y.Z-py3-none-any.whl`
  - [ ] `gtm_mcp-X.Y.Z.tar.gz`
- [ ] Package installs in clean environment
- [ ] `gtm-mcp` command works after installation
- [ ] No import errors

### PyPI Account Setup (First Time Only)
- [ ] Registered at https://pypi.org/account/register/
- [ ] Email verified
- [ ] 2FA enabled (recommended)
- [ ] API token created at https://pypi.org/manage/account/token/
- [ ] Token configured in Poetry: `poetry config pypi-token.pypi pypi-YOUR-TOKEN`

### Optional: TestPyPI (Recommended for First Release)
- [ ] Registered at https://test.pypi.org/account/register/
- [ ] TestPyPI token created
- [ ] Token configured: `poetry config pypi-token.testpypi pypi-YOUR-TOKEN`
- [ ] TestPyPI repository configured: `poetry config repositories.testpypi https://test.pypi.org/legacy/`
- [ ] Published to TestPyPI: `poetry publish -r testpypi`
- [ ] Tested installation from TestPyPI: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gtm-mcp`

## Publishing Steps

### Step 1: Final Verification
```bash
# Clean and rebuild
rm -rf dist/
poetry build

# Test locally
python -m venv /tmp/test_env
source /tmp/test_env/bin/activate
pip install dist/*.whl
gtm-mcp --help  # Should work
pip show gtm-mcp  # Check version
deactivate
```

- [ ] Executed and verified

### Step 2: Publish to PyPI
```bash
poetry publish
```

- [ ] Command executed successfully
- [ ] No errors occurred
- [ ] Confirmation message received

### Step 3: Verify on PyPI
- [ ] Package appears at https://pypi.org/project/gtm-mcp/
- [ ] Version number is correct
- [ ] Description renders correctly
- [ ] Links work (homepage, repository)
- [ ] Classifiers are correct

### Step 4: Test Installation from PyPI
```bash
# In a new environment
pip install gtm-mcp
gtm-mcp --help
pip show gtm-mcp
```

- [ ] Installation successful
- [ ] Version is correct
- [ ] Command works

### Step 5: Git Tag and Release
```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

- [ ] Git tag created
- [ ] Tag pushed to GitHub
- [ ] GitHub release created (optional but recommended)

### Step 6: Update Documentation
- [ ] Update any version references in documentation
- [ ] Announce the release (if applicable)
- [ ] Update project board/issues (if applicable)

## Post-Publishing Checklist

### Immediate Verification (Within 5 minutes)
- [ ] Package searchable on PyPI
- [ ] Can install with: `pip install gtm-mcp`
- [ ] PyPI page displays correctly
- [ ] All links functional

### Monitor (Next 24 hours)
- [ ] Check for installation issues
- [ ] Monitor GitHub issues
- [ ] Check download stats on PyPI

### Documentation Updates
- [ ] Update project README if it references "upcoming" features
- [ ] Update any installation documentation
- [ ] Announce on relevant channels if applicable

## If Something Goes Wrong

### Package won't upload
- Check token is valid and has correct permissions
- Verify version number hasn't been used before
- Check network connectivity
- Review Poetry logs for specific errors

### Package uploads but can't install
- Check package metadata in `pyproject.toml`
- Verify all dependencies are available on PyPI
- Check Python version constraints
- Review package structure with: `tar -tzf dist/*.tar.gz`

### Need to fix immediately
- **You cannot delete or replace a version on PyPI**
- Increment the version (e.g., 0.1.0 → 0.1.1)
- Fix the issue
- Rebuild and republish with new version
- Consider yanking the broken version if critical

## Version Numbering Guide

Use semantic versioning: MAJOR.MINOR.PATCH

- **PATCH** (0.0.X): Bug fixes, no API changes
  ```bash
  poetry version patch
  ```

- **MINOR** (0.X.0): New features, backward compatible
  ```bash
  poetry version minor
  ```

- **MAJOR** (X.0.0): Breaking changes
  ```bash
  poetry version major
  ```

## Quick Commands Reference

```bash
# Check version
poetry version

# Bump version
poetry version patch  # or minor, major

# Build
rm -rf dist/ && poetry build

# Test on TestPyPI
poetry publish -r testpypi

# Publish to PyPI
poetry publish

# Create git tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Resources

- [Poetry Publishing Docs](https://python-poetry.org/docs/cli/#publish)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Note**: Save this checklist and use it for every release to ensure consistency and avoid mistakes.
