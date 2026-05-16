import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# 数据库 URL 处理
# 开发环境使用 SQLite 文件数据库（与 H2 兼容）
# 格式: sqlite:///./data/db/sdd-dev.db
_database_url = os.environ.get("DATABASE_URL", settings.database_url)

# 将 H2 JDBC URL 转换为 SQLite URL
if "jdbc:h2:file:" in _database_url:
    # jdbc:h2:file:./data/db/sdd-dev -> sqlite:///./data/db/sdd-dev.db
    db_path = _database_url.replace("jdbc:h2:file:", "")
    database_url = f"sqlite:///{db_path}.db"
else:
    database_url = _database_url

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
