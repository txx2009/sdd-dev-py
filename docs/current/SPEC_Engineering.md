# AI-EXAM-BASE-PYTHON 工程规范

> 本文件是项目所有技术规范的索引与执行指引。
> Agent 在设计、审核、实现阶段应**按需读取**对应子规范，不要一次性通读全部。

## 1. 规范清单与按需读取指引

> **重要原则**：不要一次性读取所有规范。根据当前任务涉及的技术领域，仅读取相关子规范。

### 1.1 按需读取映射表

| 你正在做 | 需读取的规范 | 跳过无关规范 |
|----------|-------------|-------------|
| 新增/修改数据表 | `SPEC_Database.md` | API、前端、测试 |
| 编写 Alembic 迁移脚本 | `SPEC_Database_Migration.md` | 前端、测试 |
| 设计/审核 REST API | `SPEC_REST_API.md` | 数据库、前端 |
| 前端组件开发 | `SPEC_FE_Coding.md` + `SPEC_FE_Style.md` | 数据库、后端 |
| 后端代码开发 | `SPEC_BE_Coding.md` | 前端 |
| 异常处理与日志 | `SPEC_Logs.md` | 前端、测试 |
| 编写/审核测试 | `SPEC_Test.md` | 前端样式、日志 |
| 整体架构评审 | `SPEC_Architecture.md` | 编码细节 |

### 1.2 规范文件清单

| 序号 | 文件 | 定位 | 核心关注点 |
|------|------|------|-----------|
| 1 | `docs/current/SPEC_Architecture.md` | 架构分层、模块通信、技术选型 | 系统级设计约束 |
| 2 | `docs/current/SPEC_Database.md` | 数据库选型、ORM 规范、命名规范 | SQLite 配置、SQLAlchemy 使用规范 |
| 3 | `docs/current/SPEC_Database_Migration.md` | Alembic 版本控制 | 迁移脚本命名规范、单一职责、幂等性 |
| 4 | `docs/current/SPEC_REST_API.md` | REST 接口设计 | URL 纯名词/复数/kebab-case、HTTP 方法语义、统一响应格式 |
| 5 | `docs/current/SPEC_FE_Coding.md` | 前端编码规范 | Vue 3 Composition API、Pinia、组件/组合式函数组织 |
| 6 | `docs/current/SPEC_FE_Style.md` | 前端样式规范 | CSS 变量、命名、响应式 |
| 7 | `docs/current/SPEC_BE_Coding.md` | 后端编码规范 | Python 编码风格、分层架构、日志处理 |
| 8 | `docs/current/SPEC_Test.md` | 测试规范 | 测试框架选型、测试目录、pytest 使用 |
| 9 | `docs/current/SPEC_Logs.md` | 日志规范 | 日志级别、格式、敏感信息 |

## 2. 核心规范速查（高频违反项）

> 以下是最常被违反的核心规范，开发/审核时应重点检查。

### 2.1 数据库命名（SPEC_Database.md 第 7 节）

| 对象 | 前缀/格式 | 正确示例 | 常见错误 |
|------|----------|---------|---------|
| 表 | 复数形式 | `users`, `tasks` | `user`, `task` |
| 索引 | `idx_{表}_{字段}` | `idx_task_state` | `task_state_idx` |
| 唯一索引 | `uk_{表}_{字段}` | `uk_user_email` | `ux_email` |
| 主键字段 | `id` | `id` | `user_id` |
| 外键字段 | `{关联表}_id` | `creator_id` | `createdBy` |
| 时间戳 | `created_at`, `updated_at` | `created_at` | `createTime` |
| 布尔值 | `is_{描述}` | `is_deleted` | `deletedFlag` |

### 2.2 ORM 规范（SPEC_Database.md 第 5 节）

- **优先使用 SQLAlchemy 查询构建器**（`Model.query.filter()`, `Query` 对象）
- 避免直接写 SQL（复杂查询除外）
- Service 层返回模型或 Pydantic Schema

### 2.3 REST API（SPEC_REST_API.md）

- URL **仅包含名词**，禁止动词（`/api/v1/getUsers` 错误）
- 资源名称**统一复数**（`/api/v1/users`）
- 多单词用**连字符** kebab-case（`/api/v1/user-preferences`）
- 响应统一格式：`{"code": 200, "message": "success", "data": ...}`
- 使用 Pydantic 进行请求验证

### 2.4 Alembic 迁移（SPEC_Database_Migration.md）

- 使用 `flask db revision -m "description"` 生成迁移脚本
- 每个迁移只做一件事（单一职责）
- 一旦应用（Upgraded），绝对禁止修改内容
- 保留 `upgrade()` 和 `downgrade()` 方法

### 2.5 测试（SPEC_Test.md）

- 后端：pytest + Flask testing client
- 使用 fixtures 管理测试依赖
- TDD 流程：红 → 绿 → 重构

## 3. 设计文档审核执行流程

> 当审核 `docs/superpowers/specs/` 或 `docs/superpowers/plans/` 中的设计文档时执行。

### 3.1 第一步：识别技术领域并映射 SPEC

根据设计文档涉及的内容，从 1.1 映射表中找出需要读取的规范文件。

### 3.2 第二步：逐条对照审查

对每条映射到的规范，逐条对照设计文档内容，输出对比表：

```
| 规范条款 | 设计文档内容 | 结果(✅/❌/⚠️) | 问题说明 |
|----------|-------------|---------------|----------|
```

### 3.3 第三步：输出审核结论

问题按严重性分级：

| 级别 | 含义 | 处理要求 |
|------|------|---------|
| **阻塞** | 违反明确规范（如 REST API 路径含动词、表命名不符） | **必须在实现前修正** |
| **中等** | 规范建议未采纳（如迁移脚本未拆分为单一职责） | 强烈建议实现前修正 |
| **建议** | 非强制优化项（如补充响应样例） | 可后续迭代 |

### 3.4 强制约束

- 审核结论必须有对应的规范条款作为依据，不得仅凭主观判断
- **不得跳读或只审查部分规范**——识别到的领域必须全部覆盖
- 但**也**不要读取无关规范（如纯前端组件设计无需读数据库规范）
