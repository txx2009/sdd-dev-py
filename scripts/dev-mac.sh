#!/bin/bash
# ai-exam-base-python 本地研发启动脚本 (Mac/Linux)
# 同时启动前端和后端服务；Ctrl+C 会停止全部子进程

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

BACKEND_PID=""
FRONTEND_PID=""
CLEANED_UP=0

kill_tree() {
    local pid=$1
    [ -z "$pid" ] && return 0
    kill -0 "$pid" 2>/dev/null || return 0

    local child
    for child in $(pgrep -P "$pid" 2>/dev/null); do
        kill_tree "$child"
    done
    kill -TERM "$pid" 2>/dev/null || true
}

cleanup() {
    [ "$CLEANED_UP" -eq 1 ] && return 0
    CLEANED_UP=1

    trap - INT TERM EXIT

    echo ""
    echo "正在停止所有服务..."

    kill_tree "$BACKEND_PID"
    kill_tree "$FRONTEND_PID"

    sleep 1

    for pid in "$BACKEND_PID" "$FRONTEND_PID"; do
        kill -KILL "$pid" 2>/dev/null || true
        pkill -KILL -P "$pid" 2>/dev/null || true
    done

    wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    echo "所有服务已停止"
}

trap cleanup INT TERM EXIT

echo "========================================"
echo "ai-exam-base-python 本地研发环境启动"
echo "========================================"
echo ""

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "[错误] 前端目录不存在: $FRONTEND_DIR"
    exit 1
fi

if [ ! -d "$BACKEND_DIR" ]; then
    echo "[错误] 后端目录不存在: $BACKEND_DIR"
    exit 1
fi

echo "[1/2] 启动后端服务 (FastAPI)..."
echo "       后端目录: $BACKEND_DIR"
(
    cd "$BACKEND_DIR" && exec python run.py
) &
BACKEND_PID=$!

echo ""
echo "[2/2] 启动前端服务 (Vite)..."
echo "       前端目录: $FRONTEND_DIR"
(
    cd "$FRONTEND_DIR" && exec npm run dev
) &
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

wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
cleanup
