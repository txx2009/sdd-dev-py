# SPEC_BE_Coding - 后端编码规范

本文档定义了 AI-EXAM-BASE-PYTHON 项目后端（Flask）的编码规范。

## 1. 技术栈

- **语言**: Python 3.11+
- **框架**: Flask 3.0+
- **ORM**: SQLAlchemy 2.0+ / Flask-SQLAlchemy 3.1+
- **数据库**: SQLite (开发/测试)
- **迁移**: Alembic / Flask-Migrate
- **认证**: PyJWT + BCrypt
- **验证**: Pydantic 2.0+
- **日志**: Python logging
- **测试**: pytest

## 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `auth_service`, `user_model` |
| 类 | PascalCase | `UserService`, `AuthController` |
| 函数/方法 | snake_case | `get_user_by_id`, `create_user` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 变量 | snake_case | `user_id`, `access_token` |

## 3. 包结构

根目录：`backend/app/`。

```
backend/app/
├── __init__.py           # Flask 应用工厂
├── api/                  # API 蓝图
│   └── v1/              # API v1 版本
├── models/              # SQLAlchemy 模型
├── schemas/             # Pydantic 模式
├── services/            # 业务逻辑层
├── utils/               # 工具类
└── config.py            # 配置（可选）
```

## 4. Flask 规范

### 4.1 蓝图（Blueprints）

- 使用蓝图组织 API 路由
- 按版本划分：`api/v1/`
- 蓝图命名：`auth_bp`, `user_bp`

### 4.2 路由

- 使用装饰器定义路由
- RESTful URL 设计
- 返回统一响应格式

### 4.3 模型（Models）

- 使用 SQLAlchemy ORM
- 模型继承 `db.Model`
- 使用 Pydantic 进行数据验证

### 4.4 业务逻辑层（Services）

- 业务逻辑封装在 Service 层
- Service 由 API 层调用
- 返回原始数据或 Pydantic 模型

### 4.5 日志

- 使用 Python `logging` 模块
- 日志级别：`logging.info()`、`logging.error()`、`logging.warning()`

## 5. 错误处理

- 使用 `@app.errorhandler` 进行全局错误处理
- 返回一致的 API 响应格式：`{ "code": ..., "message": ..., "data": ... }`
- 使用适当的日志级别

## 6. 测试规范

- 框架：pytest
- 测试位置：`backend/tests/`
- 命名：`test_*.py`
- 使用 pytest fixtures

## 7. 配置说明

- **配置文件**: `config.py` 或 `backend/config.py`
- **环境变量**: 使用 `.env` 文件
- **默认端口**: 5000 (Flask 开发服务器)

## 8. 数据库规范

详见 [SPEC_Database.md](./SPEC_Database.md)

### 8.1 ORM 使用原则

- 优先使用 SQLAlchemy 提供的查询构建器
- 使用 `Query` 对象进行数据库操作
- 避免直接写 SQL（复杂查询除外）

### 8.2 命名规范

| 对象类型 | 前缀 | 示例 |
|----------|------|------|
| 表 | 无前缀（SQLite 通常用单数） | `user`, `task` |
| 索引 | `idx_` | `idx_task_state` |
| 唯一索引 | `uk_` | `uk_user_email` |
| 主键 | `id` | `id` |

## 9. API 响应格式

### 9.1 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

### 9.2 错误响应

```json
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

### 9.3 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 100
  }
}
```
