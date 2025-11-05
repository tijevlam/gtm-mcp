#!/bin/bash
# Verification script for GTM Account Restriction feature

echo "=========================================="
echo "GTM MCP Account Restriction Verification"
echo "=========================================="
echo ""

# Check Python files compile
echo "1. Checking Python syntax..."
if .venv/bin/python3 -m py_compile src/gtm_mcp/gtm_client.py; then
    echo "   ✓ gtm_client.py compiles successfully"
else
    echo "   ✗ gtm_client.py has syntax errors"
    exit 1
fi

if .venv/bin/python3 -m py_compile src/gtm_mcp/server.py; then
    echo "   ✓ server.py compiles successfully"
else
    echo "   ✗ server.py has syntax errors"
    exit 1
fi

if .venv/bin/python3 -m py_compile src/gtm_mcp/tools.py; then
    echo "   ✓ tools.py compiles successfully"
else
    echo "   ✗ tools.py has syntax errors"
    exit 1
fi

echo ""

# Check imports work
echo "2. Checking imports..."
if .venv/bin/python3 -c "from src.gtm_mcp.gtm_client import GTMClient; print('   ✓ GTMClient imports successfully')"; then
    :
else
    echo "   ✗ GTMClient import failed"
    exit 1
fi

echo ""

# Run logic tests
echo "3. Running account restriction tests..."
if python3 test_account_restriction.py | grep -q "✓ All tests completed"; then
    echo "   ✓ All validation tests passed"
else
    echo "   ✗ Validation tests failed"
    exit 1
fi

echo ""

# Check documentation exists
echo "4. Checking documentation..."
for doc in ACCOUNT_RESTRICTION.md IMPLEMENTATION_SUMMARY.md CHANGES.md; do
    if [ -f "$doc" ]; then
        echo "   ✓ $doc exists"
    else
        echo "   ✗ $doc missing"
        exit 1
    fi
done

echo ""

# Check ProSun guide exists
if [ -f "/home/etma/work/Vertisky/customers/ProSun/GTM-ACCOUNT-RESTRICTION-SETUP.md" ]; then
    echo "   ✓ ProSun setup guide exists"
else
    echo "   ✗ ProSun setup guide missing"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ All verification checks passed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update ProSun's .mcp.json with GTM_ACCOUNT_ID"
echo "2. Restart Claude Code"
echo "3. Test by listing GTM accounts"
echo ""
echo "See: /home/etma/work/Vertisky/customers/ProSun/GTM-ACCOUNT-RESTRICTION-SETUP.md"
