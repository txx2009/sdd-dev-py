# AGENTS.md - AI-EXAM-BASE-PYTHON 编码指南

AI-EXAM-BASE-PYTHON 是一个包含前后端工程的 Web 应用，采用 Vue + FastAPI 技术体系。

| 子工程名 | 工程路径 | 说明 |
|------|------|------|
| backend | `./backend` | 后端工程，FastAPI 0.115+ + Python 3.10+ + SQLAlchemy 2.0 + Alembic，数据库 SQLite |
| frontend | `./frontend` | 前端工程，Vue 3.4 + Vite 5.4 + Pinia + Ant Design Vue 4 + Axios |


> 详细架构设计见 [SPEC_Architecture.md](./docs/current/SPEC_Architecture.md)

## 1. 项目元信息

*   **项目名称**: AI-EXAM-BASE-PYTHON
*   **项目版本**: V1.0

## 2. Agent 行为准则 (General Guidelines)

### 2.1 文档与真源

> **思想**: 拥抱自然语言作为一种高级编程接口。通过编写高质量的设计文档，我们实际上是在用自然语言"编写"系统的核心逻辑。

#### 2.1.1 核心原则

| 原则 | 说明 |
|------|------|
| **设计先行** | 开发新模块或进行重大重构时，**必须**按两阶段完成研发设计：（1）调用 Superpowers 的 `brainstorming` 探索需求、比选方案、收敛设计要点；（2）`brainstorming` 完成后**必须**调用 [`rd-design-spec`](./.agents/skills/rd-design-spec/SKILL.md) 技能，将推敲结论整理为符合章节结构的**正式研发详细设计**（含架构、流程、数模、接口等）。以自然语言作为高级编程接口来"编写"系统核心逻辑。<br><br>*流程*：`brainstorming` → `rd-design-spec` → 审核 → 研发实现 → 自测通过 → 归档。正式设计文档先输出至 `docs/superpowers/specs/`；功能研发完成并自测通过后，**新增**或**合入** `docs/current` 下的对应模块设计文档（DESIGN_*）。 |
| **代码与文档一致性** | 代码实现必须与设计文档保持一致。若代码变更导致设计文档过时，**必须**同步更新 `docs/current` 中的文档。<br><br>*流程*：功能研发完成并自测通过后，将 Superpowers 生成的设计文档（`docs/superpowers/specs/` 或 `docs/superpowers/plans/` 中的产物）**新增**或**合入** `docs/current` 中作为最终说明。<br><br>*注*：`docs/current` 为权威真源，日常开发、评审、排障以本目录为准。 |
| **TDD 实践** | 对新功能、Bug 修复、改变对外行为的重构，**必须**遵循红—绿—重构。测试类型、目录与工具以 [`SPEC_Test.md`](./docs/current/SPEC_Test.md) 为准。<br><br>**强制要求**：<br>1. 计划阶段：实现计划中每个任务须包含「红（写测试）→ 绿（写实现）→ 重构」三步骤，缺一不可<br>2. 执行阶段：先写失败测试，再写实现代码，通过后再重构<br>3. 例外须审批：一次性原型、生成代码、纯配置等需在计划中注明并经用户同意 |
| **先读后写** | 修改复杂逻辑（认证、升级、启动、OnlineHub、构建与打包等）前，**优先读所有**最相关文档；不要通读全目录 DESIGN/SPEC。 |

#### 2.1.2 文档层级与优先级

| 目录 | 定位 | 使用场景 |
|------|------|----------|
| **`docs/current`** | 权威真源 | 日常开发、评审、排障，以本目录为唯一真源 |
| **`docs/superpowers`** | 过程与历史 | 仅在需要确认历史推敲、任务拆分或当时约定时检索，已定结论须回写至 `docs/current` |

> **优先级**: 若本文件或用户显式指令与 Superpowers 技能冲突，**以本文件与用户指令为准**。产品与设计真源始终在 `docs/current`。

#### 2.1.3 文档规范

- **命名约定**: 文档前缀 `PRD_`（需求）、`DESIGN_`（设计）、`SPEC_`（规范）。DESIGN 文档以叙述、流程与核心逻辑为主，避免大段实现级伪代码。
- **引用格式**: 引用代码或文档时，使用 Markdown 链接格式 `[filename](path)`。
- **溯源要求**:
  - 设计文档中应标注核心逻辑对应的代码文件或类名（如 `auth.py`）
  - 复杂核心代码建议添加 `@see docs/current/common/<Module>/DESIGN_XXX.md` 注释

#### 2.1.4 编码规范

- **遵循规范**: 代码实现必须遵循项目编码规范，详见 `docs/current` 目录下的 SPEC_* 文档：
 - [`SPEC_Architecture.md`](./docs/current/SPEC_Architecture.md) — 架构设计规范
 - [`SPEC_FE_Coding.md`](./docs/current/SPEC_FE_Coding.md) — 前端编码规范
 - [`SPEC_FE_Style.md`](./docs/current/SPEC_FE_Style.md) — 前端样式规范
 - [`SPEC_BE_Coding.md`](./docs/current/SPEC_BE_Coding.md) — 后端编码规范
 - [`SPEC_REST_API.md`](./docs/current/SPEC_REST_API.md) — REST API 设计规范
 - [`SPEC_Database.md`](./docs/current/SPEC_Database.md) — 数据库设计规范
 - [`SPEC_Database_Migration.md`](./docs/current/SPEC_Database_Migration.md) — 数据库迁移 Alembic 规范
 - [`SPEC_Test.md`](./docs/current/SPEC_Test.md) — 测试规范
 - [`SPEC_Logs.md`](./docs/current/SPEC_Logs.md) — 日志规范
- **规范优先**: 当编码规范与通用实践冲突时，以项目 SPEC 规范为准

#### 2.1.5 实现前检查清单

每次开始实现新功能、Bug 修复或行为变更前，Agent **必须**执行以下步骤：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 检查可用技能 | 使用 Skill 工具列出相关技能 |
| 2 | 调用 TDD 技能 | 对新功能必须调用 `test-driven-development` 技能 |
| 3 | 验证设计文档 | 确认已完成 `brainstorming` 且已用 `rd-design-spec` 产出正式研发设计；文档位于 `docs/current/DESIGN_*.md` 或 `docs/superpowers/specs/` |
| 4 | **验证实现计划含 TDD 步骤** | **逐任务检查**：每个实现任务必须包含红（写失败测试）、绿（写实现）、重构步骤；缺失则拒绝执行并要求补充 |
| 5 | 遵循实现计划 | 按 `docs/superpowers/plans/` 中的任务清单执行 |

> **强制要求**：新功能实现必须先有设计文档，再有测试（红），后有实现（绿）。跳过测试直接写代码视为违规。

---

#### 2.1.6 研发设计两阶段流程

新模块或重大重构的**研发设计**须严格按序执行，不得跳过或颠倒：

| 阶段 | 技能 | 职责 | 产出位置 |
|------|------|------|----------|
| 1. 方案推敲 | `brainstorming`（Superpowers） | 基于 PRD/需求探索边界、比选方案、收敛架构与关键决策 | `docs/superpowers/specs/` 过程稿（可与阶段 2 同文件迭代） |
| 2. 正式详细设计 | [`rd-design-spec`](./.agents/skills/rd-design-spec/SKILL.md) | 将阶段 1 结论沉淀为结构化研发设计（设计目标、架构、业务流程、核心设计、数模、接口等章节） | `docs/superpowers/specs/`（命名建议 `YYYY-MM-DD-{功能}.md` 或 `DESIGN_{功能}.md`） |

> **强制要求**：`brainstorming` 结束且方案经用户确认后，**必须**立即调用 `rd-design-spec` 输出最终研发设计；未产出符合 `rd-design-spec` 章节结构的正式设计文档前，**不得**进入 `writing-plans` 或编码实现。涉及 REST 接口时，`rd-design-spec` 内须结合 `das-rest-skill` 规范。

---

## 2.2 技能使用准则

| 场景 | 推荐技能 | 说明 |
|------|----------|------|
| 新功能设计（方案推敲） | `brainstorming` | 探索需求、比选方案、收敛设计要点；产出过程稿，非最终交付形态 |
| 新功能设计（正式详细设计） | `rd-design-spec` | **`brainstorming` 完成后必调**；按固定章节输出研发详细设计，作为后续计划与实现的真源依据 |
| 制定实现计划 | `writing-plans` | 将 **经 `rd-design-spec` 定稿** 的设计文档拆分为可执行的任务步骤 |
| 新功能/Bug修复 | `test-driven-development` | 红-绿-重构循环 |
| 代码审查 | `requesting-code-review` | 实现完成后的代码审查 |
| 问题排查 | `systematic-debugging` | 系统化调试 |
| 分支开发隔离 | `using-git-worktrees` | 创建独立工作树 |

> **重要**：技能使用不是可选的——它们是实现质量的保障。Agent 应主动检查并使用相关技能。

### 2.3 Superpowers 技能约束

| 约束项 | 说明 |
|--------|------|
| **禁止直接操作 `docs/current`** | Superpowers 技能（brainstorming、writing-plans 等）及 `rd-design-spec` **禁止**直接在 `docs/current` 目录创建或修改文档 |
| **设计文档必须先写至 superpowers** | `brainstorming` 过程稿与 `rd-design-spec` 正式研发设计均须先输出到 `docs/superpowers/specs/`（实现计划至 `docs/superpowers/plans/`） |
| **归档必须使用 finishing-work** | 执行收尾工作，研发测试完成后可以**提醒**用户使用`finishing-work` 技能，**不允许**自动调用 `finishing-work` 技能 |
| **例外** | 仅当 `docs/current` 中已存在对应模块文档需同步更新时，才允许直接修改（且必须标注变更原因） |

---

## 3. 文档索引与说明 (Documentation Index)

`docs/current` 是理解本项目业务逻辑和技术实现的关键入口。Agent 在执行任务前，应优先查阅相关设计文档。

### 3.0 索引文件（Index.md）功能定位

仓库内有两份**由技能驱动维护**的 Markdown 索引（`build` / `update` 全量或增量重建，`search` / `impact` 检索与分析），产出为**结构化目录 + 摘要 + 交叉链接**，便于 Agent 先建立模块地图再下钻正文；与 IDE 全文检索互补。

| 文件 | 功能定位 | 配套 Cursor 技能 | Agent 使用建议 |
|------|----------|------------------|----------------|
| [`docs/current/Index.md`](./docs/current/Index.md) | **当前知识库索引**：按模块罗列 `docs/current` 下与代码一致的 PRD、DESIGN、SPEC 等。 | `project-knowledge` | **日常开发、评审、排障**：需要「当前仓库承认哪些模块、各模块有哪些正式文档」时优先打开；行为与实现以索引所链到的 `docs/current` **正文**为准，索引本身为导航而非规范条文。 |
| [`docs/superpowers/Index.md`](./docs/superpowers/Index.md) | **Superpowers 工程历史索引**：按专题聚合 `specs/`、`plans/` 过程稿，标注归档路径等。 | `engineering-history` | **追溯过程与计划链**：需要查某功能的原始 spec/plan、多文档依赖、或「已定稿后合入哪篇 current 文档」时检索；**已定结论以实现与 `docs/current` 为准**，勿用未归档过程稿覆盖权威真源。 |

### 3.1 目录结构

```
docs/
├── current/                               # 与当前代码库一致的完整实现说明（权威真源）
│   ├── common/                            # 通用/核心模块设计文档
│   │   └── Authentication/                # 认证功能
│   └── SPEC_*.md                          # [规范] 研发及测试规范
└── superpowers/                           # Superpowers 过程产物（spec / plan），非日常真源
    ├── README.md
    ├── specs/
    └── plans/
```

### 3.2 命名约定 (Naming Conventions)

| 前缀 | 说明 | 提供人 | 示例 |
|------|------|--------|------|
| **PRD** | 原始需求文档 | 产品经理 | `PRD_UserManagement.md` |
| **DESIGN** | 通用设计文档（前后端共享） | 开发者/技术负责人 | `DESIGN_Authentication.md` |
| **DESIGN_FE** | 前端专属设计文档 | 前端开发 | `DESIGN_FE_Upgrade.md` |
| **DESIGN_BE** | 后端专属设计文档 | 后端开发 | `DESIGN_BE_Upgrade.md` |
| **SPEC** | 通用规范文档 | 技术负责人 | `SPEC_Architecture.md` |
| **SPEC_FE** | 前端专属规范文档 | 前端开发 | `SPEC_FE_Coding.md` |
| **SPEC_BE** | 后端专属规范文档 | 后端开发 | `SPEC_BE_Coding.md` |
| **SPEC_TEST** | 测试规范文档 | 测试工程师/开发者 | `SPEC_Test.md` |
| **TEST** | 功能模块测试文档 | 测试工程师/开发者 | `TEST_Authentication.md` |

> **原则**: 前后端文档除前缀外文件名保持一致。如 `DESIGN_FE_Upgrade.md` 与 `DESIGN_BE_Upgrade.md` 共同描述升级功能。

---

## 4. 开发工作流

1. **仅前端开发**：在 `.env.development` 中设置 `VITE_SPAWN_BACKEND=false`
2. **全栈开发**：在 `frontend` 下运行 `npm run dev`，在 `backend` 下运行 `python run.py`
3. **生产构建**：运行 README.md 中的完整构建命令

---

