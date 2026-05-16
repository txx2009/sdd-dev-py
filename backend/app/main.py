from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth_router, user_router
from app.models import User  # noqa: F401 - 导入以注册模型

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


@app.on_event("startup")
def create_tables():
    """启动时创建所有表"""
    Base.metadata.create_all(bind=engine)


# 注册路由
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
