#!/bin/bash
# ai-exam-base-python 本地研发启动脚本 (Mac/Linux)
# 同时启动前端和后端服务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "========================================"
echo "ai-exam-base-python 本地研发环境启动"
echo "========================================"
echo ""

# 检查前端目录
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "[错误] 前端目录不存在: $FRONTEND_DIR"
    exit 1
fi

# 检查后端目录
if [ ! -d "$BACKEND_DIR" ]; then
    echo "[错误] 后端目录不存在: $BACKEND_DIR"
    exit 1
fi

echo "[1/2] 启动后端服务 (FastAPI)..."
echo "       后端目录: $BACKEND_DIR"
cd "$BACKEND_DIR" && python run.py &
BACKEND_PID=$!

echo ""
echo "[2/2] 启动前端服务 (Vite)..."
echo "       前端目录: $FRONTEND_DIR"
cd "$FRONTEND_DIR" && npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "服务启动中，请稍候..."
echo "  前端: http://localhost:5173"
echo "  后端: http://localhost:8000"
echo "========================================"
echo ""
echo "后端进程 PID: $BACKEND_PID"
echo "前端进程 PID: $FRONTEND_PID"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待任意一个进程退出
wait
