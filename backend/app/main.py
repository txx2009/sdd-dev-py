from contextlib import asynccontextmanager
from pathlib import Path
import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command

from app.routers import auth_router, user_router


def run_migrations():
    """启动时运行数据库迁移"""
    # 获取 backend/ 目录（alembic.ini 所在目录）
    backend_dir = Path(__file__).resolve().parent.parent
    alembic_cfg = Config(backend_dir / "alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭的生命周期事件"""
    # 启动时：运行数据库迁移
    try:
        run_migrations()
        print("INFO:     Database migrations completed successfully.", flush=True)
    except Exception:
        print("ERROR:    Application startup failed during migration:", flush=True)
        traceback.print_exc(file=sys.stdout)
        raise
    yield
    # 关闭时：清理资源（如果有）


app = FastAPI(
    title="AI-EXAM-BASE-PYTHON API",
    description="AI-EXAM-BASE-PYTHON Backend API",
    version="1.0.0",
    lifespan=lifespan,
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
