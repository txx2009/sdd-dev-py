from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

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


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
