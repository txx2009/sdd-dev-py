# ai-exam-base-python 本地研发启动脚本 (Windows)
# 同时启动前端和后端服务

$ErrorActionPreference = "Continue"

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ai-exam-base-python 本地研发环境启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查前端目录
if (-not (Test-Path $FRONTEND_DIR)) {
    Write-Host "[错误] 前端目录不存在: $FRONTEND_DIR" -ForegroundColor Red
    exit 1
}

# 检查后端目录
if (-not (Test-Path $BACKEND_DIR)) {
    Write-Host "[错误] 后端目录不存在: $BACKEND_DIR" -ForegroundColor Red
    exit 1
}

Write-Host "[1/2] 启动后端服务 (FastAPI)..." -ForegroundColor Yellow
Write-Host "       后端目录: $BACKEND_DIR" -ForegroundColor Gray
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $BACKEND_DIR && python run.py" -WindowStyle Minimized

Write-Host ""
Write-Host "[2/2] 启动前端服务 (Vite)..." -ForegroundColor Yellow
Write-Host "       前端目录: $FRONTEND_DIR" -ForegroundColor Gray
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $FRONTEND_DIR && npm run dev" -WindowStyle Minimized

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "服务启动中，请稍候..." -ForegroundColor Green
Write-Host "  前端: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  后端: http://localhost:8000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
