"""Insert admin user

Revision ID: 20260513100001
Revises: 20260513100000
Create Date: 2026-05-13 10:00:01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260513100001'
down_revision: Union[str, None] = '20260513100000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 初始管理员账户 (密码: admin123, BCrypt加密)
    # 使用 BCrypt 哈希，避免每次运行时重新计算
    hashed_password = '$2a$10$BScxd/KzBW.lU.a/XP6HGe4ArF.Y9xUj7wsgma2IjHBPdbBhnaZDm'
    op.execute(
        f"INSERT INTO t_user (username, password, nickname, email, phone, status, created_at) "
        f"SELECT 'admin', '{hashed_password}', '管理员', 'admin@example.com', '13800138000', 1, CURRENT_TIMESTAMP "
        f"WHERE NOT EXISTS (SELECT 1 FROM t_user WHERE username = 'admin')"
    )


def downgrade() -> None:
    op.execute("DELETE FROM t_user WHERE username = 'admin'")
