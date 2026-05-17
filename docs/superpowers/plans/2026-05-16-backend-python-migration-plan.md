# Backend Python Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 ai-exam-base-java 的 Spring Boot 后端迁移为 FastAPI Python 实现，保持 API 兼容

**Architecture:** FastAPI 最佳实践结构，分层设计（routers/services/models/schemas），复用 Java 版本的 Flyway SQL 迁移脚本，JWT + BCrypt 认证方案

**Tech Stack:** FastAPI, SQLAlchemy 2.0, python-jose, PassLib, Flyway, H2

---

## 文件结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口，依赖注入
│   ├── config.py            # Pydantic Settings 配置
│   ├── database.py          # SQLAlchemy Engine/Session
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # SQLAlchemy User 模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # LoginRequest, LoginResponse
│   │   └── user.py          # UserCreate, UserUpdate, UserResponse
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证接口
│   │   └── user.py          # 用户 CRUD 接口
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证业务逻辑
│   │   └── user.py          # 用户业务逻辑
│   └── core/
│       ├── __init__.py
│       ├── security.py      # JWT + BCrypt 实现
│       └── deps.py          # 依赖注入（get_current_user）
├── migrations/
│   └── V1.0R26C00/
│       └── V20260513120000__Create_User_Table.sql  # 复用 Java 版
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── test_security.py
│   ├── test_auth.py
│   └── test_user.py
├── requirements.txt
├── run.py
└── .env
```

---

## Task 1: 项目基础设置

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env`
- Create: `backend/run.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

- [ ] **Step 2: 创建 .env 配置文件**

```env
DATABASE_URL=jdbc:h2:file:./data/db/sdd-dev
JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
BCRYPT_ROUNDS=10
```

- [ ] **Step 3: 创建 run.py 启动脚本**

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

- [ ] **Step 4: Commit**

```bash
git add backend/requirements.txt backend/.env backend/run.py
git commit -m "chore: add backend project foundation files"
```

---

## Task 2: 配置与数据库模块

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/config.py`
- Create: `backend/app/database.py`

- [ ] **Step 1: 创建 config.py**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # 数据库
    database_url: str = "jdbc:h2:file:./data/db/sdd-dev"

    # JWT
    jwt_secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    # BCrypt
    bcrypt_rounds: int = 10


settings = Settings()
```

- [ ] **Step 2: 创建 database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclaritiveBase

from app.config import settings

# 转换 JDBC URL 为 SQLAlchemy 支持的 H2 URL
# jdbc:h2:file:./data/db/sdd-dev -> h2:./data/db/sdd-dev
database_url = settings.database_url.replace("jdbc:", "")

engine = create_engine(
    database_url,
    connect_args={"mode": "MYSQL", "scale": 2},
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclaritiveBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/__init__.py backend/app/config.py backend/app/database.py
git commit -m "feat: add config and database modules"
```

---

## Task 3: User 模型

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/user.py`

- [ ] **Step 1: 创建 User 模型 (app/models/user.py)**

```python
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "t_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

- [ ] **Step 2: 更新 models/__init__.py**

```python
from app.models.user import User

__all__ = ["User"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/models/__init__.py backend/app/models/user.py
git commit -m "feat: add User SQLAlchemy model"
```

---

## Task 4: 安全模块（JWT + BCrypt）

**Files:**
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/security.py`

- [ ] **Step 1: 创建 security.py**

```python
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expire_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/core/__init__.py backend/app/core/security.py
git commit -m "feat: add JWT and BCrypt security module"
```

---

## Task 5: 依赖注入模块

**Files:**
- Create: `backend/app/core/deps.py`

- [ ] **Step 1: 创建 deps.py**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user import UserService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserService(db)
    user = user_service.get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/core/deps.py
git commit -m "feat: add dependency injection for current user"
```

---

## Task 6: User Schemas

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/user.py`

- [ ] **Step 1: 创建 user.py schemas**

```python
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    nickname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = None
    status: int = 1


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)


class UserUpdate(BaseModel):
    nickname: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    status: int | None = None


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6, max_length=50)


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    email: str | None
    phone: str | None
    status: int
    created_at: datetime

    model_config = {"from_attributes": True}
```

- [ ] **Step 2: 更新 schemas/__init__.py**

```python
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
)

__all__ = ["UserCreate", "UserUpdate", "UserPasswordUpdate", "UserResponse"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/schemas/__init__.py backend/app/schemas/user.py
git commit -m "feat: add user Pydantic schemas"
```

---

## Task 7: Auth Schemas

**Files:**
- Create: `backend/app/schemas/auth.py`

- [ ] **Step 1: 创建 auth.py**

```python
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    token: str
    expires_in: int  # seconds
```

- [ ] **Step 2: 更新 schemas/__init__.py**

```python
from app.schemas.auth import LoginRequest, LoginResponse

__all__ = ["UserCreate", "UserUpdate", "UserPasswordUpdate", "UserResponse", "LoginRequest", "LoginResponse"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/schemas/auth.py
git commit -m "feat: add auth Pydantic schemas"
```

---

## Task 8: User 服务

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/user.py`

- [ ] **Step 1: 创建 user.py service**

```python
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


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
        user = User(
            username=user_create.username,
            password=hash_password(user_create.password),
            nickname=user_create.nickname,
            email=user_create.email,
            phone=user_create.phone,
            status=user_create.status,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
```

- [ ] **Step 2: 更新 services/__init__.py**

```python
from app.services.user import UserService

__all__ = ["UserService"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/services/__init__.py backend/app/services/user.py
git commit -m "feat: add user service"
```

---

## Task 9: Auth 服务

**Files:**
- Create: `backend/app/services/auth.py`

- [ ] **Step 1: 创建 auth.py service**

```python
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user import UserService
from app.core.security import verify_password, create_access_token
from app.config import settings


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

    def get_current_user(self, username: str) -> User | None:
        return self.user_service.get_by_username(username)
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/services/auth.py
git commit -m "feat: add auth service"
```

---

## Task 10: 认证路由

**Files:**
- Create: `backend/app/routers/__init__.py`
- Create: `backend/app/routers/auth.py`

- [ ] **Step 1: 创建 auth.py router**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserResponse
from app.services.auth import AuthService
from app.core.deps import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("", response_model=dict)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    result = auth_service.authenticate(login_request.username, login_request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, user = result
    return {
        "data": {
            "token": access_token,
            "expires_in": settings.jwt_expire_hours * 3600,
        }
    }


@router.delete("", response_model=dict)
def logout(current_user: User = Depends(get_current_user)):
    return {"data": None}


@router.get("/me", response_model=dict)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {"data": UserResponse.model_validate(current_user).model_dump()}
```

- [ ] **Step 2: 更新 routers/__init__.py**

```python
from app.routers.auth import router as auth_router

__all__ = ["auth_router"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/routers/__init__.py backend/app/routers/auth.py
git commit -m "feat: add auth router"
```

---

## Task 11: 用户路由

**Files:**
- Create: `backend/app/routers/user.py`

- [ ] **Step 1: 创建 user.py router**

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate, UserResponse
from app.services.user import UserService
from app.core.deps import get_current_user
from app.models.user import User
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.get("", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    users, total = user_service.list_users(page, size)
    return {
        "data": [UserResponse.model_validate(u).model_dump() for u in users],
        "$page": page,
        "$size": size,
        "total": total,
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.create(user_create)
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.get("/{user_id}", response_model=dict)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.put("/{user_id}", response_model=dict)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.update(user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": UserResponse.model_validate(user).model_dump()}


@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    success = user_service.delete(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": None}


@router.put("/{user_id}/password", response_model=dict)
def change_password(
    user_id: int,
    password_update: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password_update.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    user.password = hash_password(password_update.new_password)
    db.commit()
    return {"data": None}
```

- [ ] **Step 2: 更新 routers/__init__.py**

```python
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router

__all__ = ["auth_router", "user_router"]
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/routers/user.py
git commit -m "feat: add user router with CRUD operations"
```

---

## Task 12: FastAPI 主应用

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 1: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth_router, user_router

app = FastAPI(
    title="SDD-DEV API",
    description="SDD-DEV Backend API",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

- [ ] **Step 2: Commit**

```bash
git add backend/app/main.py
git commit -m "feat: add FastAPI main application"
```

---

## Task 13: 数据库迁移

**Files:**
- Copy: `backend/migrations/V1.0R26C00/V20260513120000__Create_User_Table.sql`

- [ ] **Step 1: 创建迁移目录并复制 SQL 脚本**

```bash
mkdir -p backend/migrations/V1.0R26C00
```

复制 `D:\work\cursorWorks\ai-exam-base-java\backend\src\main\resources\db\migration\V1.0R26C00\V20260513120000__Create_User_Table.sql` 到 `backend/migrations/V1.0R26C00/`

- [ ] **Step 2: Commit**

```bash
git add backend/migrations/
git commit -m "feat: add Flyway migration scripts"
```

---

## Task 14: 测试基础配置

**Files:**
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: 创建 conftest.py**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

- [ ] **Step 2: Commit**

```bash
git add backend/tests/__init__.py backend/tests/conftest.py
git commit -m "test: add pytest configuration"
```

---

## Task 15: 安全模块测试

**Files:**
- Create: `backend/tests/test_security.py`

- [ ] **Step 1: 编写安全模块测试**

```python
import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_hash_password():
    password = "test_password123"
    hashed = hash_password(password)
    assert hashed != password
    assert hashed.startswith("$2b$")


def test_verify_password():
    password = "test_password123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_create_and_decode_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None
    decoded = decode_access_token(token)
    assert decoded.get("sub") == "testuser"
```

- [ ] **Step 2: 运行测试**

Run: `pytest backend/tests/test_security.py -v`
Expected: 3 passed

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_security.py
git commit -m "test: add security module tests"
```

---

## Task 16: 认证功能测试

**Files:**
- Create: `backend/tests/test_auth.py`

- [ ] **Step 1: 编写认证测试**

```python
import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.models.user import User


def test_login_success(client, db_session):
    # 创建测试用户
    user = User(
        username="testuser",
        password=hash_password("password123"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    # 测试登录
    response = client.post(
        "/api/v1/auth",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]
    assert "expires_in" in data["data"]


def test_login_invalid_credentials(client, db_session):
    response = client.post(
        "/api/v1/auth",
        json={"username": "nonexistent", "password": "wrong"},
    )
    assert response.status_code == 401


def test_get_current_user(client, db_session):
    # 创建测试用户
    user = User(
        username="testuser",
        password=hash_password("password123"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    # 登录获取 token
    login_response = client.post(
        "/api/v1/auth",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["data"]["token"]

    # 获取当前用户
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"
    assert data["data"]["nickname"] == "Test User"
```

- [ ] **Step 2: 运行测试**

Run: `pytest backend/tests/test_auth.py -v`
Expected: 3 passed

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_auth.py
git commit -m "test: add authentication tests"
```

---

## Task 17: 用户 CRUD 测试

**Files:**
- Create: `backend/tests/test_user.py`

- [ ] **Step 1: 编写用户 CRUD 测试**

```python
import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.models.user import User


def get_auth_headers(client: TestClient, db_session) -> dict:
    user = User(
        username="admin",
        password=hash_password("admin123"),
        nickname="Admin",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/v1/auth",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_response.json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_users(client, db_session):
    # 创建测试用户
    for i in range(3):
        user = User(
            username=f"user{i}",
            password=hash_password("password"),
            nickname=f"User {i}",
            status=1,
        )
        db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 3
    assert "$page" in data
    assert "total" in data


def test_create_user(client, db_session):
    headers = get_auth_headers(client, db_session)
    response = client.post(
        "/api/v1/users",
        json={
            "username": "newuser",
            "password": "newpass123",
            "nickname": "New User",
            "email": "new@example.com",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["username"] == "newuser"
    assert data["data"]["nickname"] == "New User"


def test_get_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.get(f"/api/v1/users/{user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "testuser"


def test_update_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.put(
        f"/api/v1/users/{user.id}",
        json={"nickname": "Updated Name"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["nickname"] == "Updated Name"


def test_delete_user(client, db_session):
    user = User(
        username="testuser",
        password=hash_password("password"),
        nickname="Test User",
        status=1,
    )
    db_session.add(user)
    db_session.commit()

    headers = get_auth_headers(client, db_session)
    response = client.delete(f"/api/v1/users/{user.id}", headers=headers)
    assert response.status_code == 200
```

- [ ] **Step 2: 运行测试**

Run: `pytest backend/tests/test_user.py -v`
Expected: 5 passed

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_user.py
git commit -m "test: add user CRUD tests"
```

---

## 实施总结

| Task | 描述 | 文件数 |
|------|------|--------|
| 1 | 项目基础设置 | 3 |
| 2 | 配置与数据库模块 | 3 |
| 3 | User 模型 | 2 |
| 4 | 安全模块 | 2 |
| 5 | 依赖注入 | 1 |
| 6 | User Schemas | 2 |
| 7 | Auth Schemas | 1 |
| 8 | User 服务 | 2 |
| 9 | Auth 服务 | 1 |
| 10 | 认证路由 | 2 |
| 11 | 用户路由 | 2 |
| 12 | FastAPI 主应用 | 1 |
| 13 | 数据库迁移 | 1 |
| 14-17 | 测试 | 8 |

**总计**: 17 个 Task，约 33 个文件
