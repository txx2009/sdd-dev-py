# SPEC_Database - 数据库设计规范

## 1. 概述

本文档详细描述了 AI-EXAM-BASE-PYTHON 系统的数据库设计、存储机制和数据管理策略。系统采用 SQLite 嵌入式数据库作为持久化存储，使用 SQLAlchemy 作为 ORM 框架，并通过 Alembic 实现数据库版本控制。

## 2. 数据库选型

### 2.1 选型原因

- **SQLite 嵌入式数据库**: 适用于桌面应用和轻量级 Web 应用，无需独立数据库服务
- **轻量级**: 数据库引擎嵌入到应用中，减少部署复杂度
- **跨平台**: 支持 Windows、macOS、Linux 等操作系统
- **文件存储**: 数据以文件形式存储，便于备份和迁移
- **零配置**: 无需安装和配置数据库服务器

## 3. 数据库配置

### 3.1 配置文件

数据库配置位于 `backend/config.py`:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3.2 连接参数说明

- `sqlite:///`: 指定使用 SQLite 文件模式存储
- `data/app.db`: 数据库文件路径（相对于 backend 目录）

## 4. 数据库存储位置

### 4.1 默认存储路径

数据库文件存储在项目根目录下的：
```
backend/data/app.db
```

> **注意**: 数据库路径为 `backend/data/app.db`，位于后端工程 `backend/` 目录下。

## 5. ORM 框架配置

### 5.1 SQLAlchemy 使用规范

#### 5.1.1 模型定义规范

- **使用 SQLAlchemy ORM**：通过 `db.Model` 定义模型类
- **表名**：使用 `__tablename__` 属性指定，明确的复数形式
- **主键**：使用 `id` 字段，`Integer` 类型，`primary_key=True`
- **时间戳**：使用 `created_at` 和 `updated_at` 字段

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=1)  # 1: 正常, 0: 禁用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 5.1.2 关系定义

使用 `db.relationship` 定义模型间关系：

```python
class User(db.Model):
    # ... 其他字段
    tasks = db.relationship('Task', backref='creator', lazy='dynamic')
```

### 5.2 查询规范

- **优先使用查询构建器**：`Model.query.filter()`, `Model.query.filter_by()`
- **使用 ORM 而非原始 SQL**：除非是复杂查询
- **避免直接写 SQL**：复杂查询可使用 `db.session.execute()`

## 6. 数据库连接池配置

SQLite 使用文件锁，不涉及连接池配置。如需更高并发，可考虑迁移到 PostgreSQL。

## 7. 数据库对象命名规范

### 7.1 命名原则

- **简洁明了**: 名称应清晰表达对象用途
- **统一前缀**: 使用前缀区分对象类型（如有需要）
- **小写字母**: 全部使用小写字母，单词间用下划线分隔
- **避免保留字**: 不使用数据库保留字作为对象名

### 7.2 对象前缀规范

| 对象类型 | 前缀/格式 | 示例 | 说明 |
|----------|------|------|------|
| **表** | 复数形式 | `users`, `tasks` | 数据表 |
| **索引** | `idx_` | `idx_task_state` | 普通索引 |
| **唯一索引** | `uk_` | `uk_user_email` | 唯一索引 |

### 7.3 表命名详细规则

**格式**: 复数形式的实体名，如 `users`、`tasks`。

### 7.4 字段命名规范

| 规则 | 说明 | 示例 |
|------|------|------|
| 主键 | `id` | `id` |
| 外键 | `{关联表}_id` | `user_id`, `parent_task_id` |
| 状态 | `{实体}_status` 或 `state` | `task_status`, `state` |
| 时间戳 | `created_at`, `updated_at` | `created_at` |
| 布尔值 | `is_{描述}` 或 `{描述}_flag` | `is_deleted`, `active_flag` |
| 创建人 | `created_by` | - |
| 更新人 | `updated_by` | - |

### 7.5 索引命名规范

**格式**: `{前缀}_{表名}_{字段名}`，如 `idx_task_state`、`uk_user_email`。

## 8. 数据库迁移规范

详见 [SPEC_Database_Migration.md](./SPEC_Database_Migration.md)

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
