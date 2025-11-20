@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo GTM MCP Account Restriction Verification
echo ==========================================
echo.

echo 1. Checking Python syntax...
.venv\Scripts\python.exe -m py_compile src/unboundai_gtm_mcp/gtm_client.py
if %errorlevel% equ 0 (
    echo    √ gtm_client.py compiles successfully
) else (
    echo    × gtm_client.py has syntax errors
    exit /b 1
)

.venv\Scripts\python.exe -m py_compile src/unboundai_gtm_mcp/server.py
if %errorlevel% equ 0 (
    echo    √ server.py compiles successfully
) else (
    echo    × server.py has syntax errors
    exit /b 1
)

.venv\Scripts\python.exe -m py_compile src/unboundai_gtm_mcp/tools.py
if %errorlevel% equ 0 (
    echo    √ tools.py compiles successfully
) else (
    echo    × tools.py has syntax errors
    exit /b 1
)

echo.
echo 2. Checking imports...
.venv\Scripts\python.exe -c "from src.gtm_mcp.gtm_client import GTMClient; print('   √ GTMClient imports successfully')"
if %errorlevel% neq 0 (
    echo    × GTMClient import failed
    exit /b 1
)

echo.
echo 3. Running account restriction tests...
python test_account_restriction.py
if %errorlevel% neq 0 (
    echo    × Validation tests failed
    exit /b 1
)
echo    √ All validation tests passed

echo.
echo ==========================================
echo √ All verification checks passed!
echo ==========================================

exit /b 0
