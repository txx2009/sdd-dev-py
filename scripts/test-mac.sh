#!/bin/bash
# ai-exam-base-python 一键单元测试 (Mac/Linux)
# 依次执行后端 pytest 测试（含 coverage）与前端测试
#
# 用法:
#   ./scripts/test-mac.sh          # 含覆盖率检查（默认）
#   ./scripts/test-mac.sh --quick  # 仅跑测试，跳过覆盖率门禁

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

WITH_COVERAGE=1
if [ "${1:-}" = "--quick" ]; then
    WITH_COVERAGE=0
fi

echo "=========================================="
echo " ai-exam-base-python 单元测试"
echo " 项目目录: $PROJECT_ROOT"
echo "=========================================="
echo ""

FAILED=0

echo ">>> [后端] 运行单元测试..."
if [ "$WITH_COVERAGE" -eq 1 ]; then
    (cd "$BACKEND_DIR" && python -m pytest -q --cov=app --cov-report=term-missing --cov-report=html)
else
    (cd "$BACKEND_DIR" && python -m pytest -q)
fi
if [ $? -ne 0 ]; then
    echo ">>> [后端] 失败"
    FAILED=1
else
    echo ">>> [后端] 通过"
    if [ "$WITH_COVERAGE" -eq 1 ]; then
        echo "    覆盖率报告: backend/htmlcov/index.html"
    fi
fi
echo ""

echo ">>> [前端] 运行单元测试..."
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "    未检测到 node_modules，正在执行 npm install..."
    (cd "$FRONTEND_DIR" && npm install)
fi

# 检查是否配置了测试框架
TEST_SCRIPT=$(cd "$FRONTEND_DIR" && npm pkg get scripts.test 2>/dev/null | tr -d '"')
if [ -z "$TEST_SCRIPT" ] || [ "$TEST_SCRIPT" = "null" ]; then
    echo "    前端未配置测试框架，跳过前端测试"
else
    if [ "$WITH_COVERAGE" -eq 1 ]; then
        (cd "$FRONTEND_DIR" && npm run test:coverage)
    else
        (cd "$FRONTEND_DIR" && npm test)
    fi
    if [ $? -ne 0 ]; then
        echo ">>> [前端] 失败"
        FAILED=1
    else
        echo ">>> [前端] 通过"
        if [ "$WITH_COVERAGE" -eq 1 ]; then
            echo "    覆盖率报告: frontend/coverage/index.html"
        fi
    fi
fi
echo ""

echo "=========================================="
if [ "$FAILED" -eq 0 ]; then
    echo " 全部单元测试通过"
    echo ""
    echo ">>> 生成 Markdown 测试报告..."
    if [ ! -f "$BACKEND_DIR/test-results/pytest-report.json" ]; then
        (cd "$BACKEND_DIR" && python -m pytest --json-report --json-report-file=test-results/pytest-report.json) >/dev/null 2>&1 || true
    fi
    python3 "$SCRIPT_DIR/generate-test-report.py" || true
    echo "    报告: results/01_test_report.md"
    exit 0
else
    echo " 存在失败的测试，请查看上方日志"
    exit 1
fi