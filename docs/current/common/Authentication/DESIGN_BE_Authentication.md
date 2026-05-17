# 认证模块后端设计文档

> **版本**: V1.0R26C00
> **项目**: AI-EXAM-BASE-PYTHON
> **模块**: Authentication-BE
> **归档日期**: 2026-05-16
> **源文档**: `docs/superpowers/specs/2026-05-16-authentication-design.md`

---

## 1. 概述

认证后端模块提供用户认证及用户管理功能，采用 JWT Token 无状态认证方案。

### 1.1 核心功能

- **用户认证**: 登录/登出/获取当前用户
- **用户管理**: 完整的用户 CRUD 操作

### 1.2 技术选型

| 技术 | 说明 |
|------|------|
| Flask | Web 框架 |
| Flask-JWT-Extended | JWT Token 认证 |
| Flask-SQLAlchemy | ORM 框架 |
| SQLite Database | 开发测试数据库 |
| BCrypt | 密码加密 |

---

## 2. 系统架构

### 2.1 认证流程

```
Browser → Backend → Database
   │         │
   │         验证用户
   │         ▼
   │      返回 JWT Token
   │         ▼
   │      携带 Token 访问受保护资源
```

### 2.2 后端包结构

```
backend/app/
├── __init__.py           # Flask 应用工厂
├── api/
│   └── v1/
│       ├── __init__.py
│       └── auth.py       # 认证 API
├── models/
│   ├── __init__.py
│   └── user.py           # 用户模型
├── services/
│   ├── __init__.py
│   └── auth.py           # 认证服务
├── schemas/
│   ├── __init__.py
│   └── user.py           # 用户 Schema
└── utils/
    ├── __init__.py
    └── responses.py       # 响应工具
```

---

## 3. 数据库设计

### 3.1 用户表 `users`

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, AUTO_INCREMENT | 主键 |
| username | String(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | String(255) | NOT NULL | 密码（BCrypt加密） |
| nickname | String(50) | NOT NULL | 昵称 |
| email | String(100) | | 邮箱 |
| phone | String(20) | | 手机号 |
| status | Integer | NOT NULL, DEFAULT 1 | 状态：1正常 0禁用 |
| created_at | DateTime | NOT NULL | 创建时间 |
| updated_at | DateTime | | 更新时间 |

**索引**: `idx_username` on `username`

### 3.2 Alembic 迁移脚本

- **路径**: `backend/migrations/versions/`
- **文件**: `001_create_users_table.py`
- **初始账户**: admin / admin123

---

## 4. API 设计

### 4.1 认证接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 登录 | POST | /api/v1/auth/login | 用户登录 |
| 登出 | POST | /api/v1/auth/logout | 用户登出（客户端删除 Token） |
| 当前用户 | GET | /api/v1/auth/me | 获取当前登录用户信息 |

### 4.2 用户管理接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户列表 | GET | /api/v1/users | 分页查询用户 |
| 创建用户 | POST | /api/v1/users | 创建新用户 |
| 用户详情 | GET | /api/v1/users/{id} | 获取指定用户详情 |
| 更新用户 | PUT | /api/v1/users/{id} | 更新用户信息 |
| 删除用户 | DELETE | /api/v1/users/{id} | 删除用户 |
| 修改密码 | PUT | /api/v1/users/{id}/password | 修改密码 |

### 4.3 响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": { ... },
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 100
  }
}
```

---

## 5. 错误处理

| 场景 | HTTP状态码 | 错误码 | 说明 |
|------|-----------|--------|------|
| 用户名/密码错误 | 401 | 401 | 登录失败 |
| Token无效/过期 | 401 | 401 | 未认证 |
| 用户被禁用 | 403 | 403 | 账户已被禁用 |
| 用户不存在 | 404 | 404 | 资源未找到 |
| 参数校验失败 | 400 | 400 | 参数错误 |
| 服务器内部错误 | 500 | 500 | 系统异常 |

---

## 6. 安全措施

- **密码存储**: BCrypt 加密
- **JWT 配置**: 24小时过期
- **CORS**: 允许配置来源
- **无状态**: 禁用 Session，使用 JWT Token 认证

---

## 7. 核心代码位置

| 组件 | 文件路径 |
|------|----------|
| Flask 应用工厂 | `backend/app/__init__.py` |
| 认证 API | `backend/app/api/v1/auth.py` |
| 用户 API | `backend/app/api/v1/users.py` |
| 用户模型 | `backend/app/models/user.py` |
| 认证服务 | `backend/app/services/auth.py` |

---

## 8. 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-16 | V1.0R26C00 | 初始版本 |
