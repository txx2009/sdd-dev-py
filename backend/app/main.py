from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app.routers import auth_router, user_router
from app.models import User  # noqa: F401 - 导入以注册模型
from app.core.security import hash_password

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
def init_db():
    """启动时初始化数据库"""
    Base.metadata.create_all(bind=engine)

    # 创建默认管理员账户
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password=hash_password("admin123"),
                nickname="管理员",
                email="admin@example.com",
                phone="13800138000",
                status=1,
            )
            db.add(admin)
            db.commit()
            print("默认管理员账户已创建: admin / admin123")
    finally:
        db.close()


# 注册路由
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
