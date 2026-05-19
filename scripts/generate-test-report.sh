#!/bin/bash
# 根据测试产物生成 results/01_test_report.md
#
# 用法:
#   ./scripts/generate-test-report.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

exec python3 "$SCRIPT_DIR/generate-test-report.py" "$@"