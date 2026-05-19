# ai-exam-base-python 本地研发启动脚本 (Windows)
# 同时启动前端和后端服务；Ctrl+C 会停止全部子进程

$ErrorActionPreference = "Continue"

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"

$script:Stopped = $false
$script:BackendProcess = $null
$script:FrontendProcess = $null

function Stop-ProcessTree {
    param([int]$ProcessId)

    if ($ProcessId -le 0) { return }
    & taskkill /T /F /PID $ProcessId 2>$null | Out-Null
}

function Stop-DevServices {
    if ($script:Stopped) { return }
    $script:Stopped = $true

    Write-Host ""
    Write-Host "正在停止所有服务..." -ForegroundColor Yellow

    foreach ($proc in @($script:BackendProcess, $script:FrontendProcess)) {
        if ($null -ne $proc -and -not $proc.HasExited) {
            Stop-ProcessTree -ProcessId $proc.Id
        }
    }

    Write-Host "所有服务已停止" -ForegroundColor Green
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ai-exam-base-python 本地研发环境启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $FRONTEND_DIR)) {
    Write-Host "[错误] 前端目录不存在: $FRONTEND_DIR" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BACKEND_DIR)) {
    Write-Host "[错误] 后端目录不存在: $BACKEND_DIR" -ForegroundColor Red
    exit 1
}

Write-Host "[1/2] 启动后端服务 (FastAPI)..." -ForegroundColor Yellow
Write-Host "       后端目录: $BACKEND_DIR" -ForegroundColor Gray
$script:BackendProcess = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "cd /d `"$BACKEND_DIR`" && python run.py" `
    -WorkingDirectory $BACKEND_DIR `
    -PassThru -NoNewWindow

Write-Host ""
Write-Host "[2/2] 启动前端服务 (Vite)..." -ForegroundColor Yellow
Write-Host "       前端目录: $FRONTEND_DIR" -ForegroundColor Gray
$script:FrontendProcess = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "cd /d `"$FRONTEND_DIR`" && npm run dev" `
    -WorkingDirectory $FRONTEND_DIR `
    -PassThru -NoNewWindow

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "服务启动中，请稍候..." -ForegroundColor Green
Write-Host "  前端: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  后端: http://localhost:8000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "后端进程 PID: $($script:BackendProcess.Id)" -ForegroundColor Gray
Write-Host "前端进程 PID: $($script:FrontendProcess.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "按 Ctrl+C 停止所有服务" -ForegroundColor Yellow

try {
    while ($true) {
        if ($script:BackendProcess.HasExited -and $script:FrontendProcess.HasExited) {
            break
        }
        Start-Sleep -Seconds 1
    }
}
finally {
    Stop-DevServices
}
