#!/usr/bin/env python3
"""
根据测试产物生成 results/01_test_report.md。

依赖：先执行单元测试（./scripts/test-mac.sh 或分别跑后端/前端测试）。
可选：--run-pytest-json 在无 Pytest JSON 时自动跑一次并写入 backend/test-results/pytest-report.json

用法:
  python3 scripts/generate-test-report.py
  python3 scripts/generate-test-report.py --output results/01_test_report.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ReportScope:
    """报告统计范围：默认剔除脚手架测试，仅保留考生新增功能。"""

    enabled: bool = True
    backend_exclude_path_prefixes: list[str] = field(default_factory=list)
    backend_exclude_paths: list[str] = field(default_factory=list)
    backend_coverage_path_prefixes: list[str] = field(default_factory=list)
    frontend_exclude_path_contains: list[str] = field(default_factory=list)
    frontend_coverage_path_contains: list[str] = field(default_factory=list)


def load_report_scope(path: Path) -> ReportScope:
    if not path.is_file():
        return ReportScope(enabled=False)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ReportScope(
        enabled=True,
        backend_exclude_path_prefixes=list(
            data.get("backend_exclude_path_prefixes", [])
        ),
        backend_exclude_paths=list(data.get("backend_exclude_paths", [])),
        backend_coverage_path_prefixes=list(
            data.get("backend_coverage_path_prefixes", [])
        ),
        frontend_exclude_path_contains=list(
            data.get("frontend_exclude_path_contains", [])
        ),
        frontend_coverage_path_contains=list(
            data.get("frontend_coverage_path_contains", [])
        ),
    )


def is_backend_scaffold(file_path: str, scope: ReportScope) -> bool:
    if not scope.enabled:
        return False
    normalized = file_path.replace("\\", "/")
    if normalized in scope.backend_exclude_paths:
        return True
    return any(normalized.startswith(p) for p in scope.backend_exclude_path_prefixes)


def is_backend_coverage(file_path: str, scope: ReportScope) -> bool:
    if not scope.enabled:
        return True
    if not scope.backend_coverage_path_prefixes:
        return True
    normalized = file_path.replace("\\", "/")
    return any(normalized.startswith(p) for p in scope.backend_coverage_path_prefixes)


def is_frontend_scaffold(file_path: str, scope: ReportScope) -> bool:
    if not scope.enabled:
        return False
    normalized = file_path.replace("\\", "/")
    return any(part in normalized for part in scope.frontend_exclude_path_contains)


def _sum_counters(elements: list[ET.Element]) -> dict[str, tuple[int, int]]:
    totals: dict[str, tuple[int, int]] = {}
    for el in elements:
        for counter in el.findall("counter"):
            ctype = counter.get("type", "")
            missed = int(counter.get("missed", 0))
            covered = int(counter.get("covered", 0))
            pm, pc = totals.get(ctype, (0, 0))
            totals[ctype] = (pm + missed, pc + covered)
    return totals


def _coverage_from_totals(totals: dict[str, tuple[int, int]]) -> CoverageMetrics:
    def pct_for(ctype: str) -> Optional[float]:
        if ctype not in totals:
            return None
        missed, covered = totals[ctype]
        return ratio(covered, missed + covered)

    line_missed, line_covered = totals.get("LINE", (0, 0))
    return CoverageMetrics(
        line=pct_for("LINE"),
        branch=pct_for("BRANCH"),
        method=pct_for("METHOD"),
        instruction=pct_for("INSTRUCTION"),
        lines_covered=line_covered,
        lines_total=line_missed + line_covered,
    )


@dataclass
class CoverageMetrics:
    line: Optional[float] = None
    branch: Optional[float] = None
    method: Optional[float] = None
    instruction: Optional[float] = None
    lines_covered: int = 0
    lines_total: int = 0

    def line_pct_str(self) -> str:
        return pct(self.line)

    def branch_pct_str(self) -> str:
        return pct(self.branch)

    def method_pct_str(self) -> str:
        return pct(self.method)


@dataclass
class TestCaseRow:
    name: str
    goal: str
    input_data: str
    expected: str
    actual: str
    passed: bool
    source: str = ""


@dataclass
class ModuleRow:
    module: str
    content: str
    case_count: int
    passed: bool


@dataclass
class TestStats:
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0

    @property
    def pass_rate(self) -> Optional[float]:
        if self.total == 0:
            return None
        return self.passed / self.total * 100


def pct(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def ratio(covered: int, total: int) -> Optional[float]:
    if total <= 0:
        return None
    return covered / total * 100


def merge_coverage(a: CoverageMetrics, b: CoverageMetrics) -> CoverageMetrics:
    lines_total = a.lines_total + b.lines_total
    lines_covered = a.lines_covered + b.lines_covered
    out = CoverageMetrics(
        line=ratio(lines_covered, lines_total),
        lines_covered=lines_covered,
        lines_total=lines_total,
    )
    branches = [x for x in (a.branch, b.branch) if x is not None]
    methods = [x for x in (a.method, b.method) if x is not None]
    instructions = [x for x in (a.instruction, b.instruction) if x is not None]
    if branches:
        out.branch = sum(branches) / len(branches)
    if methods:
        out.method = sum(methods) / len(methods)
    if instructions:
        out.instruction = sum(instructions) / len(instructions)
    return out


def parse_pytest_json(
    path: Path,
    scope: Optional[ReportScope] = None,
) -> tuple[TestStats, list[ModuleRow], list[TestCaseRow]]:
    stats = TestStats()
    modules: list[ModuleRow] = []
    cases: list[TestCaseRow] = []

    if not path.is_file():
        return stats, modules, cases

    data = json.loads(path.read_text(encoding="utf-8"))

    # pytest-json-report 格式
    for suite in data.get("test_results", []):
        file_path = suite.get("nodeid", "")
        if scope and is_backend_scaffold(file_path, scope):
            continue

        # 提取模块名
        rel = Path(file_path).name if file_path else "unknown"
        suite_title = Path(file_path).stem if file_path else rel
        outcomes = suite.get("outcome", "passed")
        setup = suite.get("setup", {})
        call = suite.get("call", {})
        teardown = suite.get("teardown", {})

        # 计算各状态数量
        setup_ok = setup.get("outcome") == "passed" if setup else True
        call_outcome = call.get("outcome", "passed") if call else outcomes
        teardown_ok = teardown.get("outcome") == "passed" if teardown else True

        if call_outcome == "skipped":
            stats.skipped += 1
        elif call_outcome == "failed":
            stats.failed += 1
        else:
            stats.passed += 1
        stats.total += 1

        suite_passed = call_outcome == "passed" and teardown_ok

        modules.append(
            ModuleRow(
                module=f"后端 / {rel}",
                content=call.get("longrepr", "") or suite_title,
                case_count=1,
                passed=suite_passed,
            )
        )

        # 从 call 中提取用例信息
        if call:
            for action in call.get("keywords", []):
                if isinstance(action, dict) and action.get("name"):
                    cases.append(
                        TestCaseRow(
                            name=action.get("name", ""),
                            goal=action.get("name", ""),
                            input_data="见测试代码",
                            expected="断言通过",
                            actual="与预期一致" if suite_passed else "失败",
                            passed=suite_passed,
                            source="backend",
                        )
                    )

    return stats, modules, cases


def parse_pytest_xml(
    path: Path,
    scope: Optional[ReportScope] = None,
) -> tuple[TestStats, list[ModuleRow], list[TestCaseRow]]:
    stats = TestStats()
    modules: list[ModuleRow] = []
    cases: list[TestCaseRow] = []

    if not path.is_dir():
        return stats, modules, cases

    for xml_file in sorted(path.glob("test-*.xml")):
        try:
            root = ET.parse(xml_file).getroot()
        except ET.ParseError:
            continue

        class_name = root.get("name", xml_file.stem.replace("test-", ""))
        if scope and is_backend_scaffold(class_name, scope):
            continue

        t = int(root.get("tests", 0))
        f = int(root.get("failures", 0))
        e = int(root.get("errors", 0))
        s = int(root.get("skipped", 0))
        passed_count = t - f - e - s

        stats.total += t
        stats.failed += f + e
        stats.skipped += s
        stats.passed += passed_count

        short_name = class_name.rsplit(".", 1)[-1] if "." in class_name else class_name
        suite_passed = (f + e) == 0

        modules.append(
            ModuleRow(
                module=f"后端 / {short_name}",
                content=class_name,
                case_count=t,
                passed=suite_passed,
            )
        )

        for tc in root.findall("testcase"):
            method = tc.get("name", "")
            failure = tc.find("failure") is not None or tc.find("error") is not None
            skipped = tc.get("skipped") is not None or tc.find("skipped") is not None
            ok = not failure and not skipped

            cases.append(
                TestCaseRow(
                    name=method,
                    goal=class_name,
                    input_data="见测试代码构造的参数",
                    expected="断言通过",
                    actual="与预期一致" if ok else "失败，见 Pytest 报告",
                    passed=ok,
                    source="backend",
                )
            )

    return stats, modules, cases


def parse_coverage_xml(
    path: Path,
    scope: Optional[ReportScope] = None,
) -> CoverageMetrics:
    if not path.is_file():
        return CoverageMetrics()
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return CoverageMetrics()

    if scope and scope.enabled and scope.backend_coverage_path_prefixes:
        packages = [
            pkg
            for pkg in root.findall(".//package")
            if any(
                (pkg.get("name") or "").replace(".", "/").startswith(p.replace(".", "/"))
                for p in scope.backend_coverage_path_prefixes
            )
        ]
        if not packages:
            return CoverageMetrics()
        return _coverage_from_totals(_sum_counters(packages))

    return _coverage_from_totals(_sum_counters([root]))


def parse_vitest_json(
    path: Path,
    scope: Optional[ReportScope] = None,
) -> tuple[TestStats, list[ModuleRow], list[TestCaseRow]]:
    stats = TestStats()
    modules: list[ModuleRow] = []
    cases: list[TestCaseRow] = []

    if not path.is_file():
        return stats, modules, cases

    data = json.loads(path.read_text(encoding="utf-8"))

    for suite in data.get("testResults", []):
        file_path = suite.get("name", "")
        if scope and is_frontend_scaffold(file_path, scope):
            continue

        rel = Path(file_path).name if file_path else "unknown"
        suite_title = Path(file_path).stem if file_path else rel
        assertions = suite.get("assertionResults", [])
        suite_passed = suite.get("status") == "passed"
        suite_failed = sum(1 for a in assertions if a.get("status") == "failed")
        suite_skipped = sum(1 for a in assertions if a.get("status") in ("skipped", "pending"))

        stats.total += len(assertions)
        stats.passed += sum(1 for a in assertions if a.get("status") == "passed")
        stats.failed += suite_failed
        stats.skipped += suite_skipped

        describe = ""
        if assertions:
            ancestors = assertions[0].get("ancestorTitles") or []
            describe = " / ".join(ancestors) if ancestors else suite_title

        modules.append(
            ModuleRow(
                module=f"前端 / {rel}",
                content=describe or suite_title,
                case_count=len(assertions),
                passed=suite_passed,
            )
        )

        for a in assertions:
            title = a.get("title", "")
            ancestors = a.get("ancestorTitles") or []
            full_name = a.get("fullName") or title
            status = a.get("status", "failed")
            ok = status == "passed"
            cases.append(
                TestCaseRow(
                    name=full_name,
                    goal=title,
                    input_data="见测试代码中的 mock / 组件 props",
                    expected="Vitest 断言期望",
                    actual="与预期一致" if ok else "; ".join(a.get("failureMessages") or [])[:200] or "失败",
                    passed=ok,
                    source="frontend",
                )
            )

    return stats, modules, cases


def run_pytest_json(backend_dir: Path, out_file: Path) -> bool:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "pytest",
        "--json-report", f"--json-report-file={out_file}",
    ]
    try:
        subprocess.run(cmd, cwd=backend_dir, check=True, capture_output=True, text=True)
        return out_file.is_file()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_overview_table(
    stats: TestStats,
    coverage: CoverageMetrics,
) -> str:
    pass_rate = pct(stats.pass_rate)
    code_cov = coverage.line_pct_str()
    if code_cov == "N/A" and coverage.instruction is not None:
        code_cov = pct(coverage.instruction)

    rows = [
        ("单元测试用例总数", str(stats.total)),
        ("通过用例数", str(stats.passed)),
        ("失败用例数", str(stats.failed)),
        ("跳过用例数", str(stats.skipped)),
        ("测试通过率", pass_rate),
        ("代码覆盖率", code_cov),
        ("行覆盖率", coverage.line_pct_str()),
        ("分支覆盖率", coverage.branch_pct_str()),
        ("方法 / 函数覆盖率", coverage.method_pct_str()),
    ]
    lines = ["| 指标 | 结果 |", "| ---- | ---- |"]
    for k, v in rows:
        lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


def build_module_table(modules: list[ModuleRow]) -> str:
    lines = [
        "| 模块 / 类 / 文件 | 测试内容 | 对应用例数量 | 是否通过 |",
        "| ---- | ---- | ---- | ---- |",
    ]
    for m in modules:
        status = "是" if m.passed else "否"
        lines.append(f"| {m.module} | {m.content} | {m.case_count} | {status} |")
    if len(modules) == 0:
        lines.append(
            "| （无新增功能测试数据，请为业务模块补充测试并执行 pytest / npm test） |  |  | 否 |"
        )
    return "\n".join(lines)


def build_case_table(cases: list[TestCaseRow], limit: int = 30) -> str:
    lines = [
        "| 用例名称 | 测试目标 | 输入数据 | 预期结果 | 实际结果 | 是否通过 |",
        "| ---- | ---- | ---- | ---- | ---- | ---- |",
    ]
    shown = cases[:limit]
    for c in shown:
        status = "是" if c.passed else "否"
        actual = c.actual.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {c.name} | {c.goal} | {c.input_data} | {c.expected} | {actual} | {status} |"
        )
    if len(cases) > limit:
        lines.append(f"| … | 另有 {len(cases) - limit} 条用例未列出 |  |  |  |  |")
    if not cases:
        lines.append("| （无数据） |  |  |  |  | 否 |")
    return "\n".join(lines)


def build_screenshot_section(project_root: Path, backend_ok: bool, frontend_ok: bool) -> str:
    lines = [
        "> 粘贴项目运行单元测试的核心结果",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if backend_ok:
        lines.append("- 后端 coverage HTML：`backend/htmlcov/index.html`")
    if frontend_ok:
        lines.append("- 前端覆盖率 HTML：`frontend/coverage/index.html`")
    img_dir = project_root / "results" / "images"
    if img_dir.is_dir():
        images = sorted(img_dir.glob("*.png")) + sorted(img_dir.glob("*.jpg"))
        if images:
            lines.append("")
            lines.append("截图：")
            for img in images:
                rel = img.relative_to(project_root)
                lines.append(f"![{img.name}]({rel.as_posix()})")
    else:
        lines.append("")
        lines.append("（可将终端截图保存至 `results/images/` 后重新运行本脚本以自动嵌入）")
    return "\n".join(lines)


def build_scope_note(scope: ReportScope, scope_path: Path, project_root: Path) -> str:
    if not scope.enabled:
        return ""
    try:
        rel = scope_path.relative_to(project_root).as_posix()
    except ValueError:
        rel = scope_path.as_posix()
    return (
        f"> 统计范围：已剔除脚手架默认测试，仅包含考生新增功能。配置见 `{rel}`。\n\n"
    )


def generate_report(
    project_root: Path,
    template_path: Path,
    output_path: Path,
    run_pytest_json: bool,
    include_scaffold: bool = False,
    scope_path: Optional[Path] = None,
) -> int:
    backend_surefire = project_root / "backend" / "test-results"
    backend_pytest_json = project_root / "backend" / "test-results" / "pytest-report.json"
    backend_coverage = project_root / "backend" / "coverage.xml"
    frontend_vitest = project_root / "frontend" / "test-results" / "vitest-report.json"
    frontend_coverage = project_root / "frontend" / "coverage" / "clover.xml"
    backend_dir = project_root / "backend"

    scope_file = scope_path or (project_root / "scripts" / "test-report-scope.json")
    scope = load_report_scope(scope_file)
    if include_scaffold:
        scope = ReportScope(enabled=False)

    # 解析后端测试结果（优先 JSON，其次 XML）
    be_stats = TestStats()
    be_modules: list[ModuleRow] = []
    be_cases: list[TestCaseRow] = []

    if backend_pytest_json.is_file():
        be_stats, be_modules, be_cases = parse_pytest_json(backend_pytest_json, scope)
    elif backend_surefire.is_dir():
        be_stats, be_modules, be_cases = parse_pytest_xml(backend_surefire, scope)

    be_cov = parse_coverage_xml(backend_coverage, scope)

    # 解析前端测试结果
    fe_stats, fe_modules, fe_cases = parse_vitest_json(frontend_vitest, scope)
    fe_cov = CoverageMetrics()  # TODO: 解析前端 coverage

    total_stats = TestStats(
        total=be_stats.total + fe_stats.total,
        passed=be_stats.passed + fe_stats.passed,
        failed=be_stats.failed + fe_stats.failed,
        skipped=be_stats.skipped + fe_stats.skipped,
    )
    combined_cov = merge_coverage(be_cov, fe_cov)
    all_modules = be_modules + fe_modules
    all_cases = be_cases + fe_cases

    if not template_path.is_file():
        # 创建默认模板
        template_content = """# 单元测试报告

## 1. 单元测试概览
| 指标 | 结果 |
| ---- | ---- |

## 2. 单元测试覆盖范围
| 模块 / 类 / 文件 | 测试内容 | 对应用例数量 | 是否通过 |
| ---- | ---- | ---- | ---- |

## 3. 关键测试用例说明
| 用例名称 | 测试目标 | 输入数据 | 预期结果 | 实际结果 | 是否通过 |
| ---- | ---- | ---- | ---- | ---- | ---- |

## 4. 单元测试截图
> 粘贴项目运行单元测试的核心结果

"""
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text(template_content, encoding="utf-8")

    template = load_template(template_path)
    scope_note = build_scope_note(scope, scope_file, project_root)
    overview = build_overview_table(total_stats, combined_cov)
    module_table = build_module_table(all_modules)
    case_table = build_case_table(all_cases)
    screenshot = build_screenshot_section(
        project_root,
        backend_coverage.is_file(),
        frontend_coverage.is_file(),
    )

    report = template
    if scope_note and report.startswith("# "):
        first_nl = report.find("\n")
        report = report[: first_nl + 1] + "\n" + scope_note + report[first_nl + 1 :]
    report = re.sub(
        r"(## 1\. 单元测试概览\n)\| 指标 \| 结果 \|\n\| ---- \| ---- \|\n(?:\| [^\n]+ \|\n)+",
        r"\1" + overview + "\n",
        report,
        count=1,
    )
    report = re.sub(
        r"(## 2\. 单元测试覆盖范围\n\n)\| 模块 / 类 / 文件 \|.*?(?=\n---)",
        r"\1" + module_table + "\n",
        report,
        count=1,
        flags=re.DOTALL,
    )
    report = re.sub(
        r"(## 3\. 关键测试用例说明\n)\| 用例名称 \|.*?(?=\n---)",
        r"\1" + case_table + "\n",
        report,
        count=1,
        flags=re.DOTALL,
    )
    report = re.sub(
        r"(## 4\. 单元测试截图\n).*",
        r"\1\n" + screenshot + "\n",
        report,
        count=1,
        flags=re.DOTALL,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"已生成: {output_path}")
    print(
        f"  用例: 总计 {total_stats.total}, 通过 {total_stats.passed}, "
        f"失败 {total_stats.failed}, 跳过 {total_stats.skipped}"
    )
    print(f"  覆盖率(业务代码行): {combined_cov.line_pct_str()}")
    if scope.enabled:
        print(f"  已剔除脚手架测试（配置: {scope_file.name}）")
    return 0


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    parser = argparse.ArgumentParser(description="根据测试产物生成单元测试 Markdown 报告")
    parser.add_argument(
        "--template",
        type=Path,
        default=project_root / "results" / "01_test_report.tmp.md",
        help="报告模板路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "results" / "01_test_report.md",
        help="输出报告路径",
    )
    parser.add_argument(
        "--run-pytest-json",
        action="store_true",
        help="若缺少 Pytest JSON，自动执行 pytest --json-report",
    )
    parser.add_argument(
        "--include-scaffold",
        action="store_true",
        help="包含脚手架默认测试（不过滤）",
    )
    parser.add_argument(
        "--scope",
        type=Path,
        default=project_root / "scripts" / "test-report-scope.json",
        help="统计范围配置文件",
    )
    args = parser.parse_args()

    return generate_report(
        project_root,
        args.template,
        args.output,
        args.run_pytest_json,
        include_scaffold=args.include_scaffold,
        scope_path=args.scope,
    )


if __name__ == "__main__":
    sys.exit(main())