# DESIGN_BE_Architecture - 后端工程架构设计

> **版本**: V1.0
> **日期**: 2026-05-16
> **项目**: AI-EXAM-BASE-PYTHON

---

## 1. 概述

后端工程采用 Flask + Python 3.11+ 技术体系，建立符合项目规范的企业级 Flask 工程骨架。

## 2. 技术选型

| 组件 | 版本 | 说明 |
|------|------|------|
| Flask | 3.0+ | Web 框架 |
| Python | 3.11+ | LTS 版本 |
| Flask-SQLAlchemy | 3.1+ | ORM 扩展 |
| SQLAlchemy | 2.0+ | ORM 框架 |
| Alembic | 1.13+ | 数据库迁移 |
| Flask-Migrate | 4.0+ | 迁移管理 |
| Flask-CORS | 4.0+ | 跨域支持 |
| PyJWT | 2.8+ | Token 认证 |
| BCrypt | 4.1+ | 密码加密 |
| Pydantic | 2.0+ | 数据验证 |

## 3. 包结构设计

```
backend/
├── app/                    # 应用主包
│   ├── __init__.py        # Flask 应用工厂
│   ├── api/               # API 蓝图
│   │   ├── __init__.py
│   │   └── v1/            # API v1 版本
│   │       ├── __init__.py
│   │       └── auth.py    # 认证 API
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   └── user.py        # 用户模型
│   ├── schemas/           # 请求/响应模式
│   │   ├── __init__.py
│   │   └── user.py        # 用户模式
│   ├── services/          # 业务逻辑
│   │   ├── __init__.py
│   │   └── auth.py        # 认证服务
│   └── utils/             # 工具类
│       ├── __init__.py
│       └── responses.py   # 响应工具
├── migrations/            # Alembic 迁移
│   └── versions/          # 迁移版本
├── tests/                 # 测试目录
├── config.py              # 配置
└── requirements.txt      # 依赖
```

> **说明**: 采用 Flask 应用工厂模式，便于测试和扩展。

## 4. 核心配置文件

### 4.1 requirements.txt

**关键依赖**:
- `flask>=3.0.0`
- `flask-sqlalchemy>=3.1.0`
- `flask-migrate>=4.0.0`
- `flask-cors>=4.0.0`
- `sqlalchemy>=2.0.0`
- `alembic>=1.13.0`
- `pyjwt>=2.8.0`
- `bcrypt>=4.1.0`
- `pydantic>=2.0.0`

### 4.2 config.py

| 配置项 | 值 |
|--------|-----|
| SECRET_KEY | 环境变量或默认密钥 |
| SQLALCHEMY_DATABASE_URI | SQLite 文件路径 |
| SQLALCHEMY_TRACK_MODIFICATIONS | False |
| JSON_AS_ASCII | False |

## 5. 数据库配置

- **类型**: SQLite 文件数据库
- **路径**: `backend/data/app.db`
- **迁移**: Alembic

## 6. 安全配置

安全实现预留：
- BCrypt 密码加密
- JWT Token 认证
- CORS 配置

## 7. 工程结构

```
backend/                         # 后端工程目录
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── app/
│   ├── __init__.py
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── migrations/
│   └── versions/
├── data/                       # 数据库文件目录
│   └── app.db
└── tests/
    └── ...
```

## 8. 核心代码位置

| 文件 | 说明 |
|------|------|
| `app/__init__.py` | Flask 应用工厂 |
| `config.py` | 应用配置 |
| `requirements.txt` | 依赖配置 |

## 9. 待迭代项

- [ ] 安全核心实现（JWT）
- [ ] 业务模块开发
- [ ] API 文档（按需）

---

## 关联文档

- [SPEC_Architecture.md](../SPEC_Architecture.md) - 架构设计规范
- [SPEC_BE_Coding.md](../SPEC_BE_Coding.md) - 后端编码规范
