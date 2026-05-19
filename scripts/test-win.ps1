# ai-exam-base-python 一键单元测试 (Windows)
# 依次执行后端 pytest 测试（含 coverage）与前端测试
#
# 用法:
#   .\scripts\test-win.ps1          # 含覆盖率检查（默认）
#   .\scripts\test-win.ps1 -Quick   # 仅跑测试，跳过覆盖率门禁

param(
    [switch]$Quick
)

$ErrorActionPreference = "Continue"

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"

$Failed = $false

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " ai-exam-base-python 单元测试" -ForegroundColor Cyan
Write-Host " 项目目录: $PROJECT_ROOT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host ">>> [后端] 运行单元测试..." -ForegroundColor Green
Push-Location $BACKEND_DIR
try {
    if ($Quick) {
        python -m pytest -q
    } else {
        python -m pytest -q --cov=app --cov-report=term-missing --cov-report=html
    }
    if ($LASTEXITCODE -ne 0) {
        throw "pytest 退出码 $LASTEXITCODE"
    }
    Write-Host ">>> [后端] 通过" -ForegroundColor Green
    if (-not $Quick) {
        Write-Host "    覆盖率报告: backend/htmlcov/index.html"
    }
} catch {
    $Failed = $true
    Write-Host ">>> [后端] 失败" -ForegroundColor Red
}
Pop-Location
Write-Host ""

Write-Host ">>> [前端] 运行单元测试..." -ForegroundColor Green
Push-Location $FRONTEND_DIR
try {
    if (-not (Test-Path "node_modules")) {
        Write-Host "    未检测到 node_modules，正在执行 npm install..."
        npm install
        if ($LASTEXITCODE -ne 0) { throw "npm install 失败" }
    }
    # 检查是否配置了测试框架
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    $testScript = $packageJson.scripts.test
    if ($null -eq $testScript) {
        Write-Host "    前端未配置测试框架，跳过前端测试" -ForegroundColor Yellow
    } else {
        if ($Quick) {
            npm test
        } else {
            npm run test:coverage
        }
        if ($LASTEXITCODE -ne 0) {
            throw "前端测试退出码 $LASTEXITCODE"
        }
        Write-Host ">>> [前端] 通过" -ForegroundColor Green
        if (-not $Quick) {
            Write-Host "    覆盖率报告: frontend/coverage/index.html"
        }
    }
} catch {
    $Failed = $true
    Write-Host ">>> [前端] 失败" -ForegroundColor Red
}
Pop-Location
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
if (-not $Failed) {
    Write-Host " 全部单元测试通过" -ForegroundColor Green
    Write-Host ""
    Write-Host ">>> 生成 Markdown 测试报告..." -ForegroundColor Green

    $PytestJson = Join-Path $BACKEND_DIR "test-results\pytest-report.json"
    if (-not (Test-Path $PytestJson)) {
        Push-Location $BACKEND_DIR
        try {
            python -m pytest --json-report --json-report-file=test-results/pytest-report.json 2>$null | Out-Null
        } catch {
            # 忽略 pytest JSON 生成失败，报告脚本会提示
        }
        Pop-Location
    }

    $ReportScript = Join-Path $PSScriptRoot "generate-test-report.ps1"
    if (Test-Path $ReportScript) {
        & $ReportScript
    } else {
        $PyScript = Join-Path $PSScriptRoot "generate-test-report.py"
        if (Get-Command python -ErrorAction SilentlyContinue) {
            Push-Location $PROJECT_ROOT
            try { python $PyScript } catch { }
            Pop-Location
        } elseif (Get-Command py -ErrorAction SilentlyContinue) {
            Push-Location $PROJECT_ROOT
            try { py -3 $PyScript } catch { }
            Pop-Location
        }
    }
    Write-Host "    报告: results/01_test_report.md"
    exit 0
} else {
    Write-Host " 存在失败的测试，请查看上方日志" -ForegroundColor Red
    exit 1
}