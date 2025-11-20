#!/usr/bin/env pwsh
# Verification script for GTM Account Restriction feature

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "GTM MCP Account Restriction Verification" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python files compile
Write-Host "1. Checking Python syntax..." -ForegroundColor Yellow

$pythonExe = ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

$files = @(
    "src/unboundai_gtm_mcp/gtm_client.py",
    "src/unboundai_gtm_mcp/server.py",
    "src/unboundai_gtm_mcp/tools.py"
)

foreach ($file in $files) {
    $fileName = Split-Path $file -Leaf
    if (& $pythonExe -m py_compile $file 2>$null) {
        Write-Host "   ✓ $fileName compiles successfully" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $fileName has syntax errors" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Check imports work
Write-Host "2. Checking imports..." -ForegroundColor Yellow
$importTest = & $pythonExe -c "from src.unboundai_gtm_mcp.gtm_client import GTMClient; print('   ✓ GTMClient imports successfully')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host $importTest -ForegroundColor Green
} else {
    Write-Host "   ✗ GTMClient import failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Run logic tests
Write-Host "3. Running account restriction tests..." -ForegroundColor Yellow
$testOutput = & $pythonExe test_account_restriction.py 2>&1
if ($testOutput -match "✓ All tests completed") {
    Write-Host "   ✓ All validation tests passed" -ForegroundColor Green
} else {
    Write-Host "   ✗ Validation tests failed" -ForegroundColor Red
    Write-Host $testOutput
    exit 1
}

Write-Host ""

# Check documentation exists
Write-Host "4. Checking documentation..." -ForegroundColor Yellow
$docs = @(
    "ACCOUNT_RESTRICTION.md",
    "IMPLEMENTATION_SUMMARY.md",
    "CHANGES.md"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "   ✓ $doc exists" -ForegroundColor Green
    } else {
        Write-Host "   ✗ $doc missing" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Check ProSun guide exists (adjust path for Windows)
$proSunGuide = "C:\Users\etma\work\Vertisky\customers\ProSun\GTM-ACCOUNT-RESTRICTION-SETUP.md"
# Or use relative path if applicable
# $proSunGuide = "..\..\..\ProSun\GTM-ACCOUNT-RESTRICTION-SETUP.md"

if (Test-Path $proSunGuide) {
    Write-Host "   ✓ ProSun setup guide exists" -ForegroundColor Green
} else {
    Write-Host "   ✗ ProSun setup guide missing (checked: $proSunGuide)" -ForegroundColor Yellow
    # Don't exit - this might be expected on different machines
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ All verification checks passed!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update ProSun's .mcp.json with GTM_ACCOUNT_ID"
Write-Host "2. Restart Claude Code"
Write-Host "3. Test by listing GTM accounts"
Write-Host ""
if (Test-Path $proSunGuide) {
    Write-Host "See: $proSunGuide" -ForegroundColor Cyan
}
