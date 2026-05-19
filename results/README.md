# results 目录说明

本目录存放考试/评分用的结果 Markdown。仓库内保留带 `.tmp` 后缀的**模板**；考生填写或脚本生成的是**去掉 `.tmp` 的最终文件**（供评分脚本抓取）。

## 文件清单

| 模板（勿删，勿改文件名） | 最终交付文件 | 用途 |
| --- | --- | --- |
| `01_test_report.tmp.md` | `01_test_report.md` | 单元测试与覆盖率结果 |
| `02_run_report.tmp.md` | `02_run_report.md` | 启动与功能运行验证（截图、手工填写） |

命名约定：模板为 `*_report.tmp.md`，交付物为 `*_report.md`（仅去掉文件名中的 `.tmp`，扩展名仍为 `.md`）。

## 如何生成 / 填写

### `01_test_report.md`（可自动生成）

1. 执行单元测试（后端 JaCoCo + 前端 Vitest 覆盖率）：

   Mac / Linux:

   ```bash
   ./scripts/test-mac.sh
   ```

   Windows:

   ```powershell
   .\scripts\test-win.ps1
   ```

   全部通过后，脚本会调用 `scripts/generate-test-report.py`，根据 JaCoCo、`frontend/test-results/vitest-report.json` 等产物填充模板，写出 `results/01_test_report.md`。

2. 也可单独生成（需已跑过测试）：

   Mac / Linux:

   ```bash
   ./scripts/generate-test-report.sh
   # 或
   python3 scripts/generate-test-report.py --run-frontend-json
   ```

   Windows:

   ```powershell
   .\scripts\generate-test-report.ps1
   # 或
   .\scripts\generate-test-report.ps1 -RunFrontendJson
   ```

3. 统计范围（默认剔除脚手架自带测试，只统计考生新增功能）见 `scripts/test-report-scope.json`；需要包含全部测试时可加 `--include-scaffold`。

### `02_run_report.md`（手工）

以 `02_run_report.tmp.md` 为结构参考，在 `02_run_report.md` 中填写启动说明、功能验证表与截图链接。可将截图放在 `results/images/`，模板内已示例相对路径（如 `./images/start-success.png`）。

## 截图目录

```text
results/images/
```

由考生自行截取并放入；`01_test_report.md` 第 4 节、`02_run_report.md` 中通过 Markdown 图片语法引用。

## 提交注意

- 模板文件 `*.tmp.md` 保留在仓库中，不要改名为最终文件名。
- 最终交付的 `01_test_report.md`、`02_run_report.md` 需纳入版本控制或按考试要求提交；本地生成物勿提交无关临时文件。
