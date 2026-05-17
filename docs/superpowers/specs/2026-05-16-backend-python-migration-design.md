# 后端 Python 迁移设计文档

> **版本**: V1.0R26C00
> **项目**: ai-exam-base-python
> **类型**: 设计文档
> **日期**: 2026-05-16

---

## 1. 概述

### 1.1 项目背景

将 `ai-exam-base-java` 工程复刻为 `ai-exam-base-python`，其中：
- **docs/**：保持不变
- **frontend/**：保持不变
- **backend/**：从 Java Spring Boot 改为 Python FastAPI 实现

### 1.2 核心功能

- **用户认证**：登录 / 登出 / 获取当前用户
- **用户管理**：完整的用户 CRUD 操作

### 1.3 技术选型

| 层级 | Java (原) | Python (新) |
|------|-----------|-------------|
| 框架 | Spring Boot 4 + JDK 17 | **FastAPI** |
| ORM | MyBatis-Plus | **SQLAlchemy 2.0** |
| 认证 | Spring Security + JWT | **python-jose + PassLib** |
| 数据库 | H2 | H2 (复用 SQL) |
| 迁移 | Flyway | Flyway (复用 SQL) |
| 密码加密 | BCrypt | BCrypt (PassLib) |

---

## 2. 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理（对应 Java @ConfigurationProperties）
│   ├── database.py          # SQLAlchemy 连接配置
│   ├── models/              # SQLAlchemy 模型（对应 Java Entity）
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic 模型（对应 Java DTO）
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── routers/             # API 路由（对应 Java Controller）
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/            # 业务逻辑（对应 Java Service）
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── core/                # 核心模块
│   │   ├── __init__.py
│   │   ├── security.py      # JWT + BCrypt 实现
│   │   └── deps.py          # 依赖注入工具
│   └── migrations/          # Flyway SQL 脚本（复用 Java 版本）
│       └── V1.0R26C00/
│           └── V20260513120000__Create_User_Table.sql
├── requirements.txt
├── run.py                   # 启动脚本
└── alembic.ini              # Alembic 配置（Flyway 辅助）
```

---

## 3. API 设计

### 3.1 认证接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 登录 | POST | `/api/v1/auth` | 用户登录 |
| 登出 | DELETE | `/api/v1/auth` | 用户登出（客户端删除 Token） |
| 当前用户 | GET | `/api/v1/auth/me` | 获取当前登录用户信息 |

### 3.2 用户管理接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户列表 | GET | `/api/v1/users` | 分页查询用户 |
| 创建用户 | POST | `/api/v1/users` | 创建新用户 |
| 用户详情 | GET | `/api/v1/users/{id}` | 获取指定用户详情 |
| 更新用户 | PUT | `/api/v1/users/{id}` | 更新用户信息 |
| 删除用户 | DELETE | `/api/v1/users/{id}` | 删除用户 |
| 修改密码 | PUT | `/api/v1/users/{id}/password` | 修改密码 |

### 3.3 响应格式

与 Java 版本完全一致：

```json
{
  "data": { ... },
  "$page": 1,
  "$size": 10,
  "total": 100
}
```

**成功响应**：
```json
{
  "data": { "id": 1, "username": "admin", "nickname": "管理员" }
}
```

**错误响应**：
```json
{
  "error": {
    "code": "BadArgument",
    "message": "参数错误"
  }
}
```

---

## 4. 数据库设计

### 4.1 用户表 `t_user`

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password | VARCHAR(255) | NOT NULL | 密码（BCrypt加密） |
| nickname | VARCHAR(50) | NOT NULL | 昵称 |
| email | VARCHAR(100) | | 邮箱 |
| phone | VARCHAR(20) | | 手机号 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态：1正常 0禁用 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | | 更新时间 |

**索引**：`idx_username` on `username`

### 4.2 迁移脚本

直接复用 Java 版本的 Flyway SQL 脚本：
```
V20260513120000__Create_User_Table.sql
```

**初始账户**：admin / admin123

---

## 5. 核心模块设计

### 5.1 配置管理 (`config.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库
    database_url: str = "jdbc:h2:file:./data/db/sdd-dev"
    
    # JWT
    jwt_secret_key: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    
    # BCrypt
    bcrypt_rounds: int = 10
    
    class Config:
        env_file = ".env"
```

### 5.2 安全模块 (`core/security.py`)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expire_hours: int = 24) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expire_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

### 5.3 依赖注入 (`core/deps.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from core.security import decode_access_token
from services.user import UserService

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_service = UserService(db)
    user = user_service.get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
```

---

## 6. 服务层设计

### 6.1 认证服务 (`services/auth.py`)

```python
from sqlalchemy.orm import Session
from services.user import UserService
from core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def authenticate(self, username: str, password: str) -> tuple[str, User] | None:
        user = self.user_service.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        if user.status != 1:
            raise HTTPException(status_code=403, detail="User is disabled")
        
        access_token = create_access_token(data={"sub": user.username})
        return access_token, user
```

### 6.2 用户服务 (`services/user.py`)

```python
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def list_users(self, page: int = 1, size: int = 10) -> tuple[list[User], int]:
        query = self.db.query(User)
        total = query.count()
        users = query.offset((page - 1) * size).limit(size).all()
        return users, total
    
    def create(self, user_create: UserCreate) -> User:
        # ...
    
    def update(self, user_id: int, user_update: UserUpdate) -> User | None:
        # ...
    
    def delete(self, user_id: int) -> bool:
        # ...
```

---

## 7. 路由层设计

### 7.1 认证路由 (`routers/auth.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.auth import LoginRequest, LoginResponse
from schemas.user import UserResponse
from services.auth import AuthService
from core.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])

@router.post("", response_model=dict)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    result = auth_service.authenticate(login_request.username, login_request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token, user = result
    return {
        "data": {
            "token": access_token,
            "user": UserResponse.model_validate(user).model_dump()
        }
    }

@router.delete("", response_model=dict)
def logout(current_user: User = Depends(get_current_user)):
    return {"data": None}

@router.get("/me", response_model=dict)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {"data": UserResponse.model_validate(current_user).model_dump()}
```

### 7.2 用户路由 (`routers/user.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserResponse, UserCreate, UserUpdate
from services.user import UserService
from core.deps import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["用户"])

@router.get("", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_service = UserService(db)
    users, total = user_service.list_users(page, size)
    return {
        "data": [UserResponse.model_validate(u).model_dump() for u in users],
        "$page": page,
        "$size": size,
        "total": total
    }
# ... 其他 CRUD 接口
```

---

## 8. 环境配置

### 8.1 前端配置

无需修改，前端 `.env.development` 保持不变：
```
VITE_API_BASE_URL=http://localhost:8000
```

### 8.2 后端配置

`.env` 文件：
```
DATABASE_URL=jdbc:h2:file:./data/db/sdd-dev
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
BCRYPT_ROUNDS=10
```

---

## 9. 依赖列表

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
flyway-sqlserver>=11.0.0
alembic>=1.13.0
h2>=0.3.0
python-multipart>=0.0.9
```

---

## 10. 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-16 | V1.0R26C00 | 初始版本 |
