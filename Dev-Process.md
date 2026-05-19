# SDD-DEV 研发工作流程

## 1. write-prd — 编写需求文档

**Skill**: `write-prd`

**产出物**: `PRD 需求文档`

**产出**: `docs/current/modules/{模块}/PRD_{功能}.md`

---

## 2. brainstorming — 编写研发设计

> 第1步完成后默认会有brainstorming执行提示，可以直接选择继续执行。

**Skill**: `brainstorming`

**产出物**: `研发设计文档`

**产出**: `docs/superpowers/specs/YYYY-MM-DD-{功能}.md`

---

## 3. writing-plans — 编写研发计划

> 第2步完成后默认会有writing-plans执行提示，可以直接选择继续执行。

**Skill**: `writing-plans`

**产出物**: `实施计划`

**产出**: `docs/superpowers/plans/YYYY-MM-DD-{功能}.md`

---

## 4. subagent-driven-development / executing-plans — 编码执行

> 第3步完成后默认会有Subagent-Driven or  Inline Execution执行提示，可以直接选择继续执行。

**Skill**: `subagent-driven-development`（推荐）或 `executing-plans`

**产出物**: `实现代码`

**产出**: `frontend/` / `backend/` 实现代码

---

## 5. test-driven-development — 单元测试

> 第4步编码阶段内部默认会使用TDD方式，先编写单元测试再实现代码，不需要显示调用。

**Skill**: `stest-driven-development`

**产出物**: `单元测试代码`

**产出**: `frontend/` / `backend/` 实现单元代码

## 6. finishing-work — 工作收尾

**Skill**: `finishing-work`

**产出物**: `归档文档`

内部依次执行：
1. `releasing-design-docs` — 设计文档归档
2. `engineering-history` update — 工程历史索引更新
3. `project-knowledge` update — 项目知识库索引更新
4. `reorganize-commits` — Commit 规范化整理

**产出**: 归档后的 DESIGN_ 设计文档（`docs/current/modules/{模块}/DESIGN_{功能}.md`）

---

## 项目启动

**Windows 环境**：
```powershell
./scripts/dev-win.ps1
```

**macOS 环境**：
```bash
./scripts/dev-mac.sh
```

启动后访问 http://localhost:5173 ，使用 `admin/admin123` 登录。