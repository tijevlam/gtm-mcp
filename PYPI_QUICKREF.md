# PyPI Quick Reference for gtm-mcp

## 🚀 Quick Commands

### Initial Setup (One-time)
```bash
# Install Poetry
pip install poetry

# Configure PyPI token
poetry config pypi-token.pypi pypi-YOUR-TOKEN-HERE

# (Optional) Configure TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-YOUR-TESTPYPI-TOKEN-HERE
```

### Release Workflow

#### 1. Update Version
```bash
# Option A: Use Poetry (recommended)
poetry version patch    # 0.0.1 → 0.0.2
poetry version minor    # 0.0.1 → 0.1.0
poetry version major    # 0.0.1 → 1.0.0

# Option B: Edit pyproject.toml manually
# Update: version = "0.1.0"
```

#### 2. Build Package
```bash
# Clean and build
rm -rf dist/
poetry build

# Verify build artifacts
ls -lh dist/
```

#### 3. Test Locally (Optional but recommended)
```bash
# Test in clean environment
python -m venv /tmp/test_env
source /tmp/test_env/bin/activate
pip install dist/*.whl
gtm-mcp --help  # Should work
pip show gtm-mcp  # Check version
deactivate
```

#### 4. Publish
```bash
# Option A: TestPyPI first (recommended for testing)
poetry publish -r testpypi

# Test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gtm-mcp

# Option B: Direct to PyPI (production)
poetry publish

# Verify
pip install gtm-mcp --upgrade
```

#### 5. Tag Release in Git
```bash
# After successful PyPI publish
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## 📋 Pre-Release Checklist

- [ ] All tests pass
- [ ] Version bumped in pyproject.toml
- [ ] CHANGES.md updated with release notes
- [ ] README.md updated if needed
- [ ] All changes committed to git
- [ ] Built successfully (`poetry build`)
- [ ] Tested locally
- [ ] (Optional) Tested on TestPyPI

## 🛠️ Using dev-helper.sh

For a guided experience:
```bash
./dev-helper.sh
```

This interactive script provides menu options for all common tasks.

## 🔍 Troubleshooting

### "File already exists" error
PyPI doesn't allow re-uploading the same version. Bump version and rebuild.

### Test installation from TestPyPI
```bash
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  gtm-mcp
```

### Clear pip cache
```bash
pip cache purge
```

### View package on PyPI
- Production: https://pypi.org/project/gtm-mcp/
- Test: https://test.pypi.org/project/gtm-mcp/

## 📦 Package Structure

```
gtm-mcp/
├── src/
│   └── gtm_mcp/          # Source code
│       ├── __init__.py   # Package entry point
│       └── server.py     # Contains run() function
├── pyproject.toml        # Package metadata
├── README.md             # Package description for PyPI
├── LICENSE               # Package license
└── dist/                 # Build artifacts (not in git)
    ├── *.whl            # Wheel distribution
    └── *.tar.gz         # Source distribution
```

## 🔐 Security

### API Token Permissions
- **First upload**: Token needs "Entire account" scope
- **Subsequent uploads**: Can limit to "gtm-mcp" project

### Token Storage
Tokens are stored in Poetry config:
```bash
# View config location
poetry config --list

# Stored in: ~/.config/pypoetry/auth.toml
```

### Never commit:
- API tokens
- .pypirc files
- Personal credentials

## 📚 Resources

- [Poetry Docs](https://python-poetry.org/docs/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)

## 💡 Tips

1. **Always test on TestPyPI first** for major releases
2. **Keep versions consistent** between git tags and PyPI
3. **Document changes** in CHANGES.md before releasing
4. **Use semantic versioning** (MAJOR.MINOR.PATCH)
5. **Test installation** in clean environment before publishing
