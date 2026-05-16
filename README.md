# AI-Exam-Base-Python

AI-Exam-Base-Python 是一个前后端分离的 Web 应用，采用 Vue + FastAPI 技术体系实现。

## 技术栈

### 后端

| 组件 | 版本 |
|------|------|
| FastAPI | 0.115+ |
| Python | 3.10+ |
| SQLAlchemy | 2.0+ |
| 数据库 | H2 |
| 安全 | python-jose + PassLib (JWT + BCrypt) |
| 迁移 | Flyway |
| 服务器 | Uvicorn |

### 前端

| 组件 | 版本 |
|------|------|
| Vue.js | 3.4.x |
| Vite | 5.4.x |
| Ant Design Vue | 4.2.x |
| Vue Router | 4.3.x |
| Pinia | 2.1.x |
| Axios | 1.7.x |

## 项目结构

```
ai-exam-base-python/
├── backend/                # 后端工程 (FastAPI + SQLAlchemy)
│   ├── app/
│   │   ├── main.py        # FastAPI 入口
│   │   ├── config.py      # 配置管理
│   │   ├── database.py    # 数据库连接
│   │   ├── models/        # SQLAlchemy 模型
│   │   ├── schemas/       # Pydantic 模型
│   │   ├── routers/       # API 路由
│   │   ├── services/      # 业务逻辑
│   │   └── core/          # 核心模块 (JWT, 依赖注入)
│   ├── migrations/         # Flyway SQL 脚本
│   ├── tests/             # 测试
│   ├── requirements.txt
│   └── run.py
├── frontend/               # 前端工程 (Vue 3 + Node.js)
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── scripts/                # 启动脚本
└── docs/                   # 权威真源文档
    ├── current/
    └── superpowers/
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 9+

### 仅前端开发

适用于不需要后端联调的 UI 开发：

```bash
cd frontend
# 修改 .env.development，设置 VITE_SPAWN_BACKEND=false
npm install
npm run dev
```

### 全栈开发

#### 方式一：使用脚本启动（推荐）

```bash
# Windows
.\scripts\dev-win.ps1

# Mac/Linux
chmod +x ./scripts/dev-mac.sh
./scripts/dev-mac.sh
```

#### 方式二：手动启动

```bash
# 终端 1: 启动前端
cd frontend
npm install
npm run dev

# 终端 2: 启动后端
cd backend
pip install -r requirements.txt
python run.py
```

服务启动后访问：http://localhost:5173（前端）

后端 API：http://localhost:8000

### 后端单独运行

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### H2 数据库控制台

开发环境可通过 H2 控制台查看数据库（如果启用）：

- JDBC URL: `jdbc:h2:file:./data/db/sdd-dev`
- 用户名: `sa`
- 密码: (空)

## API 端点

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth | 用户登录 |
| DELETE | /api/v1/auth | 用户登出 |
| GET | /api/v1/auth/me | 获取当前用户 |

### 用户管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/users | 用户列表（分页） |
| POST | /api/v1/users | 创建用户 |
| GET | /api/v1/users/{id} | 用户详情 |
| PUT | /api/v1/users/{id} | 更新用户 |
| DELETE | /api/v1/users/{id} | 删除用户 |
| PUT | /api/v1/users/{id}/password | 修改密码 |

### 其他接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /health | 健康检查 |

## 测试

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

## 配置说明

### 后端配置

后端配置通过 `backend/.env` 文件管理：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| DATABASE_URL | 数据库连接 URL | jdbc:h2:file:./data/db/sdd-dev |
| JWT_SECRET_KEY | JWT 密钥 | (需修改) |
| JWT_ALGORITHM | JWT 算法 | HS256 |
| JWT_EXPIRE_HOURS | Token 过期时间（小时） | 24 |
| BCRYPT_ROUNDS | BCrypt 轮数 | 10 |

### 前端配置

| 环境 | 配置文件 | 说明 |
|------|----------|------|
| 开发环境 | `.env.development` | `VITE_SPAWN_BACKEND=false` 时仅前端开发 |
| 生产环境 | `.env.production` | 前后端联调或独立部署 |

## 相关文档

- [设计文档](docs/superpowers/specs/2026-05-16-backend-python-migration-design.md) — 后端迁移设计
- [实施计划](docs/superpowers/plans/2026-05-16-backend-python-migration-plan.md) — 实施计划

## 初始账户

- 用户名: admin
- 密码: admin123
