#!/bin/bash

# Quick Start Script for gtm-mcp Package Development
# This script helps with common development tasks

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}GTM-MCP Development Helper${NC}\n"

# Function to display menu
show_menu() {
    echo "Select an option:"
    echo "1. Install dependencies"
    echo "2. Run tests"
    echo "3. Build package"
    echo "4. Test local installation"
    echo "5. Clean build artifacts"
    echo "6. Bump version (patch)"
    echo "7. Bump version (minor)"
    echo "8. Bump version (major)"
    echo "9. Publish to TestPyPI"
    echo "10. Publish to PyPI"
    echo "0. Exit"
}

# Install dependencies
install_deps() {
    echo -e "${GREEN}Installing dependencies...${NC}"
    pip install poetry
    poetry install
}

# Run tests
run_tests() {
    echo -e "${GREEN}Running tests...${NC}"
    poetry run pytest
}

# Build package
build_package() {
    echo -e "${GREEN}Building package...${NC}"
    rm -rf dist/
    poetry build
    echo -e "${GREEN}Build complete! Artifacts in dist/${NC}"
    ls -lh dist/
}

# Test local installation
test_install() {
    echo -e "${GREEN}Testing local installation...${NC}"
    if [ -d "/tmp/test_gtm_env" ]; then
        rm -rf /tmp/test_gtm_env
    fi
    python -m venv /tmp/test_gtm_env
    source /tmp/test_gtm_env/bin/activate
    pip install dist/*.whl
    echo -e "${GREEN}Testing gtm-mcp command...${NC}"
    which gtm-mcp
    pip show gtm-mcp
    deactivate
    echo -e "${GREEN}Test complete!${NC}"
}

# Clean build artifacts
clean() {
    echo -e "${GREEN}Cleaning build artifacts...${NC}"
    rm -rf dist/ build/ *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    echo -e "${GREEN}Clean complete!${NC}"
}

# Bump version
bump_version() {
    VERSION_TYPE=$1
    echo -e "${GREEN}Bumping ${VERSION_TYPE} version...${NC}"
    poetry version $VERSION_TYPE
    NEW_VERSION=$(poetry version -s)
    echo -e "${GREEN}New version: ${NEW_VERSION}${NC}"
}

# Publish to TestPyPI
publish_testpypi() {
    echo -e "${GREEN}Publishing to TestPyPI...${NC}"
    poetry publish -r testpypi
}

# Publish to PyPI
publish_pypi() {
    echo -e "${GREEN}⚠️  Publishing to PyPI (production)...${NC}"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        poetry publish
        echo -e "${GREEN}Published to PyPI!${NC}"
    else
        echo "Cancelled."
    fi
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice: " choice
    echo ""
    
    case $choice in
        1) install_deps ;;
        2) run_tests ;;
        3) build_package ;;
        4) test_install ;;
        5) clean ;;
        6) bump_version "patch" ;;
        7) bump_version "minor" ;;
        8) bump_version "major" ;;
        9) publish_testpypi ;;
        10) publish_pypi ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid option. Please try again." ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    echo ""
done
