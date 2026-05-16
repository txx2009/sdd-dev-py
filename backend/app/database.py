import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# 转换 JDBC URL 为 SQLAlchemy 支持的 H2 URL
# jdbc:h2:file:./data/db/sdd-dev -> h2:./data/db/sdd-dev
# 支持通过环境变量覆盖（用于测试）
_database_url = os.environ.get("DATABASE_URL", settings.database_url)
database_url = _database_url.replace("jdbc:h2:file:", "h2:")

engine = create_engine(
    database_url,
    connect_args={"mode": "MYSQL", "scale": 2} if "h2" in database_url else {},
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
