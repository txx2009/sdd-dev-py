# SPEC_Database_Migration - 数据库版本控制规范

本文档详细描述了 AI-EXAM-BASE-PYTHON 项目的数据库迁移与版本控制规范，基于 Alembic 工具实现。

## 1. Alembic 数据库脚本编写规范

为了保证数据库版本控制的稳定性和可维护性，编写 Alembic 迁移脚本时请遵循以下规则：

### 1.1 目录结构规范

- **基础路径**: `backend/migrations/`
- **版本目录**: `backend/migrations/versions/`
- **示例结构**:
    ```
    migrations/
    ├── versions/
    │   ├── V20260513100000__Create_User_Table.py
    │   ├── V20260513100001__Insert_Admin_User.py
    │   └── V20260516110000__Add_User_Email_Column.py
    ├── env.py
    └── alembic.ini
    ```

### 1.2 文件命名规范

- **格式**: `{TimeStamp}__{Description}.py`
- **TimeStamp**: 必须符合 `yyyyMMddHHmmss` 格式，代表脚本创建时间
- **Separator**: 时间戳与描述之间必须使用**双下划线** `__` 分隔
- **Description**: 使用清晰的英文描述（下划线分隔的单词），首字母大写
- **强制规则**: 脚本文件命名**只能**是 `V20260516100000__Create_User_Table.py` 格式
- **示例**:
    - ✅ `V20260513100000__Create_User_Table.py` (正确)
    - ✅ `V20260513100001__Insert_Admin_User.py` (正确)
    - ❌ `001_create_user_table.py` (错误 - 不符合规范)
    - ❌ `abc123_create_user_table.py` (错误 - 不符合规范)

> **说明**: Alembic 默认生成的 revision ID 为短哈希（如 `a1b2c3d4`），不符合本规范要求。生成迁移后，需将文件重命名以符合 `{TimeStamp}__{Description}.py` 格式，同时修改文件内部的 `revision` 变量值。

### 1.3 迁移脚本内容规范

- **幂等性 (Idempotency)**: 迁移脚本应尽可能幂等。使用 `op.create_table_if_not_exists()`、`op.drop_table_if_exists()` 等方法确保脚本可重复执行。
- **单一职责**: 每个脚本只做一件主要的事（如创建一个模块的所有表，或修改一个表结构）。避免将无关的修改混在一个脚本中。
- **不可变性**: 一旦脚本被应用（Upgraded），**绝对禁止**修改已提交的迁移文件内容。如果需要修改，请创建新的迁移脚本。
- **回滚支持**: 使用 `upgrade()` 和 `downgrade()` 方法，确保可以回滚到上一个版本。

### 1.4 存放位置

- 脚本统一存放于: `backend/migrations/versions/`
- 每个版本的脚本必须放在对应版本号的子目录中

## 2. 版本管理策略

### 2.1 时间戳生成规则

- **时间戳格式**: `yyyyMMddHHmmss` (年月日时分秒)
- **生成方式**: 建议使用脚本自动生成或手动编写，避免使用 Alembic 默认的短哈希 revision
- **示例**: `20260516100000` 表示 2026年05月16日 10:00:00

### 2.2 时间戳命名规则

- **格式**: `yyyyMMddHHmmss`（14位数字时间戳）
- **含义**: 精确到秒的时间戳，保证唯一性和执行顺序
- **示例**: `20260513100000` -> `20260513100001` -> `20260516110000`

### 2.3 多人协作规范

- **版本冲突避免**: 使用精确到秒的时间戳可有效避免多人开发时的版本冲突
- **分支开发**: 在功能分支中开发时，建议预留足够的时间间隔或使用分支特定前缀
- **合并策略**: 合并前检查迁移版本是否冲突，必要时调整时间戳

## 3. 迁移命令

```bash
# 创建新迁移（生成后需按规范重命名）
flask db revision -m "Create user table"

# 升级数据库
flask db upgrade

# 降级数据库
flask db downgrade

# 查看当前版本
flask db current

# 查看迁移历史
flask db history
```

## 4. 迁移流程 (Migration Process)

1. 开发者在本地编写并测试模型变更。
2. 使用 `flask db revision -m "description"` 生成迁移脚本。
3. 将生成的文件移动到对应的版本号子目录（如 `versions/V26R26C00/`）。
4. 将文件名重命名为 `V{yyyyMMddHHmmss}__{Description}.py` 格式。
5. 修改文件内部的 `revision` 变量为与文件名一致的时间戳格式（如 `V20260516100000`）。
6. 手动检查生成的迁移脚本，确保内容正确。
7. 使用 `flask db upgrade` 执行迁移。
8. 如需回滚，使用 `flask db downgrade`。

## 5. Alembic 配置

### 5.1 alembic.ini 配置

在 `backend/alembic.ini` 中配置 `file_template` 以符合规范：

```ini
[alembic]
# path to migration scripts
script_location = migrations

# 格式: V{revision}__{description}
file_template = V%%(rev)s__%%(slug)s
```

### 5.2 版本路径分隔符

```ini
# 版本路径分隔符（支持 os/PATH/SQLITE 默认）
version_path_separator = os
```

## 6. Flask-Migrate 快速开始

### 6.1 初始化

```bash
# 在 backend 目录下
flask db init
```

### 6.2 创建迁移

```bash
flask db revision -m "Create users table"
```

### 5.3 重命名迁移文件（按规范）

将 Alembic 生成的 `versions/xxx_create_users_table.py` 重命名为：

```
versions/20260513100000__Create_Users_Table.py
```

并修改文件内部的 `revision` 和 `down_revision`：

```python
revision = '20260513100000'
down_revision = None  # 或上一个版本的 revision
```

### 5.4 编辑迁移脚本

```python
def upgrade():
    op.create_table('users',
        db.Column('id', db.Integer(), nullable=False),
        db.Column('username', db.String(length=50), nullable=False),
        db.Column('email', db.String(length=100), nullable=False),
        # ... 其他字段
        db.PrimaryKeyConstraint('id')
    )
    # 创建索引
    op.create_index('idx_users_username', 'users', ['username'])

def downgrade():
    op.drop_index('idx_users_username', table_name='users')
    op.drop_table('users')
```

## 7. 最佳实践

1. **始终使用 ORM 或 Alembic**: 避免直接修改数据库
2. **小而独立的迁移**: 每个迁移只做一件事
3. **测试回滚**: 在生产环境前测试 `downgrade()`
4. **版本注释**: 每个迁移要有清晰的描述
5. **文件名规范**: 严格按照 `V{TimeStamp}__{Description}.py` 格式命名

## 8. 参考文档

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
**最后更新**: 2026-05-16
