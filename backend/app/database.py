import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# 数据库 URL
# 优先使用环境变量，否则使用配置默认值
database_url = os.environ.get("DATABASE_URL", settings.database_url)

# 创建引擎
engine_kwargs = {
    "echo": False,  # 生产环境可改为 True 查看 SQL
    "pool_pre_ping": True,
}
if "sqlite" in database_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
