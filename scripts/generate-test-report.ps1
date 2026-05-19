# 根据测试产物生成 results/01_test_report.md (Windows)
#
# 用法:
#   .\scripts\generate-test-report.ps1

$ErrorActionPreference = "Continue"

$SCRIPT_DIR = $PSScriptRoot
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR

Write-Host ">>> 生成 Markdown 测试报告..." -ForegroundColor Green

$PyScript = Join-Path $SCRIPT_DIR "generate-test-report.py"
if (Get-Command python -ErrorAction SilentlyContinue) {
    Push-Location $PROJECT_ROOT
    try {
        python $PyScript --output results/01_test_report.md
    } catch {
        Write-Host "    报告生成失败" -ForegroundColor Red
    }
    Pop-Location
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Push-Location $PROJECT_ROOT
    try {
        py -3 $PyScript --output results/01_test_report.md
    } catch {
        Write-Host "    报告生成失败" -ForegroundColor Red
    }
    Pop-Location
} else {
    Write-Host "    未找到 Python，无法生成报告" -ForegroundColor Red
}