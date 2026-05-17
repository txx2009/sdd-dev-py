# SPEC_Architecture.md - 架构设计规范

> **版本**: V1.0R26C00
> **项目**: AI-EXAM-BASE-PYTHON
> **更新日期**: 2026-05-16

---

## 1. 项目概述

### 1.1 项目简介

AI-EXAM-BASE-PYTHON 是一个前后端分离的 Web 应用，采用 Vue + Flask 技术体系实现。

### 1.2 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **前端** | Vue.js + Node.js | - |
| **后端** | Flask + Python 3.11+ | - |
| **ORM** | SQLAlchemy + Flask-SQLAlchemy | - |
| **数据库** | SQLite (开发/测试) | - |
| **迁移工具** | Alembic | - |
| **构建工具** | pip / npm | - |

### 1.3 工程结构

```
ai-exam-base-python/              # 项目根目录
├── backend/              # 后端工程 (Flask + SQLAlchemy)
├── frontend/              # 前端工程 (Vue 3 + Node.js)
└── docs/                  # 权威真源文档
    ├── current/           # 权威真源文档
    │   ├── common/        # 通用/核心模块设计
    │   ├── modules/       # 业务模块设计
    │   ├── SPEC_*.md      # 研发及测试规范
    │   └── Index.md       # 文档索引
    └── superpowers/      # Superpowers 过程产物
```

---

## 2. 前端架构

### 2.1 技术选型

- **框架**: Vue.js (渐进式 JavaScript 框架)
- **包管理**: npm
- **开发服务器**: Vite

### 2.2 架构设计

详见 [common/Architecture/DESIGN_FE_Architecture.md](./common/Architecture/DESIGN_FE_Architecture.md)

### 2.3 环境配置

| 环境 | 配置文件 | 说明 |
|------|----------|------|
| 开发环境 | `.env.development` | `VITE_SPAWN_BACKEND=false` 时仅前端开发 |
| 生产环境 | `.env.production` | 前后端联调或独立部署 |

### 2.4 编码规范

详见 [SPEC_FE_Coding.md](./SPEC_FE_Coding.md) 和 [SPEC_FE_Style.md](./SPEC_FE_Style.md)

---

## 3. 后端架构

### 3.1 技术选型

- **核心框架**: Flask
- **Python 版本**: Python 3.11+
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **数据库**: SQLite (开发/测试)
- **迁移工具**: Alembic
- **构建工具**: pip

### 3.2 架构设计

详见 [common/Architecture/DESIGN_BE_Architecture.md](./common/Architecture/DESIGN_BE_Architecture.md)

### 3.3 分层架构

```
后端分层 (app/):
├── api/            # REST API 蓝图
├── models/         # 数据模型 (SQLAlchemy)
├── schemas/        # 请求/响应模式 (Pydantic/Marshmallow)
├── services/       # 业务逻辑层
└── utils/          # 工具类
```

### 3.4 REST API 设计

详见 [SPEC_REST_API.md](./SPEC_REST_API.md)

### 3.5 数据库设计

详见 [SPEC_Database.md](./SPEC_Database.md) 和 [SPEC_Database_Migration.md](./SPEC_Database_Migration.md)

### 3.6 编码规范

详见 [SPEC_BE_Coding.md](./SPEC_BE_Coding.md)

---

## 4. 数据库规范

### 4.1 SQLite 数据库

- **用途**: 开发、测试环境
- **模式**: 文件数据库
- **迁移工具**: Alembic

详见 [SPEC_Database.md](./SPEC_Database.md)

---

## 5. 开发工作流

### 5.1 仅前端开发

```bash
# 在 frontend 中设置 .env.development
VITE_SPAWN_BACKEND=false
```

### 5.2 全栈开发

```bash
# 终端 1: 启动前端
cd frontend
npm run dev

# 终端 2: 启动后端
cd backend
flask --app app run --debug
```

### 5.3 生产构建

详见各工程 README.md

---

## 6. 日志规范

详见 [SPEC_Logs.md](./SPEC_Logs.md)

---

## 7. 安全规范

（待补充具体安全设计）

---

## 8. 相关文档

| 文档 | 说明 |
|------|------|
| [SPEC_FE_Coding.md](./SPEC_FE_Coding.md) | 前端编码规范 |
| [SPEC_FE_Style.md](./SPEC_FE_Style.md) | 前端样式规范 |
| [SPEC_BE_Coding.md](./SPEC_BE_Coding.md) | 后端编码规范 |
| [SPEC_REST_API.md](./SPEC_REST_API.md) | REST API 设计规范 |
| [SPEC_Database.md](./SPEC_Database.md) | 数据库设计规范 |
| [SPEC_Database_Migration.md](./SPEC_Database_Migration.md) | 数据库迁移规范 |
| [SPEC_Test.md](./SPEC_Test.md) | 测试规范 |
| [SPEC_Logs.md](./SPEC_Logs.md) | 日志规范 |
| [Index.md](./Index.md) | 文档索引 |

---

## 9. 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-05-16 | V1.0R26C00 | 初始版本（基于 Java 版本适配） | - |
