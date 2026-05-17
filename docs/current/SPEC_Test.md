# 测试规范文档

## 1. 目的与范围

本规范定义 AI-EXAM-BASE-PYTHON 项目的测试策略、测试类型、测试工具使用及测试代码编写标准，确保软件质量并提高测试效率。

**适用范围**：
- 本规范为通用测试规范，适用于所有功能模块
- 各具体功能模块的测试设计见对应的测试文档

## 2. 测试策略

### 2.1 测试类型

本项目后端（Flask）测试主要包括：

1. **单元测试 (Unit Tests)**
   - 针对 Service、Model、Util 等组件
   - 使用 pytest
   - Mock 外部依赖，快速执行

2. **接口测试 (API Tests)**
   - 针对 API 端点
   - 使用 pytest + Flask 测试客户端
   - 验证 REST API 的正确性

3. **集成测试 (Integration Tests)**
   - 针对多个组件协作
   - 使用真实数据库（测试环境）
   - 验证完整业务流程

## 3. 后端测试规范 (Flask)

### 3.1 测试框架

- **测试框架**: pytest
- **Mock 框架**: pytest-mock / unittest.mock
- **Flask 测试**: Flask testing client
- **数据库**: SQLite 内存数据库（测试用）

### 3.2 测试文件组织

```
backend/                          # 后端工程
├── tests/                        # 测试目录
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── test_api/                # API 测试
│   │   ├── __init__.py
│   │   └── test_auth.py
│   ├── test_services/           # Service 测试
│   │   ├── __init__.py
│   │   └── test_auth_service.py
│   └── test_models/             # Model 测试
│       ├── __init__.py
│       └── test_user.py
```

**命名约定**:
- 测试文件：`test_*.py`
- 测试类：`TestClassName`
- 测试函数：`test_should_*`

### 3.3 pytest 配置

在 `backend/pytest.ini` 或 `pyproject.toml` 中配置：

```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short"
```

### 3.4 单元测试示例

```python
# tests/test_services/test_auth_service.py
import pytest
from unittest.mock import patch, MagicMock
from app.services.auth import AuthService

class TestAuthService:
    """认证服务单元测试"""

    def test_should_return_user_when_credentials_valid(self):
        """当凭证有效时应该返回用户"""
        # Given
        mock_user = MagicMock()
        mock_user.username = 'admin'
        mock_user.check_password.return_value = True

        with patch('app.services.auth.User') as MockUser:
            MockUser.query.filter_by.return_value.first.return_value = mock_user

            # When
            result = AuthService.authenticate('admin', 'password123')

            # Then
            assert result == mock_user
            mock_user.check_password.assert_called_once_with('password123')

    def test_should_return_none_when_credentials_invalid(self):
        """当凭证无效时应该返回 None"""
        # Given
        with patch('app.services.auth.User') as MockUser:
            MockUser.query.filter_by.return_value.first.return_value = None

            # When
            result = AuthService.authenticate('admin', 'wrongpassword')

            # Then
            assert result is None
```

### 3.5 接口测试示例

```python
# tests/test_api/test_auth.py
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def client():
    """创建测试客户端"""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """获取认证头"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_should_login_successfully(client):
    """应该成功登录"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 200
    assert 'access_token' in data['data']

def test_should_get_current_user(client, auth_headers):
    """应该获取当前用户信息"""
    response = client.get('/api/v1/auth/me', headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 200
    assert 'username' in data['data']
```

### 3.6 测试配置

使用 pytest fixtures 管理测试依赖：

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """创建测试 CLI runner"""
    return app.test_cli_runner()
```

## 4. 测试覆盖率要求

### 4.1 覆盖率指标

| 代码类型 | 行覆盖率 | 分支覆盖率 | 说明 |
|---------|---------|-----------|------|
| **核心业务逻辑** | ≥ 90% | ≥ 80% | Service、API、关键算法 |
| **一般业务逻辑** | ≥ 80% | ≥ 70% | 普通业务功能 |
| **工具类** | ≥ 85% | ≥ 75% | Util、Helper 类 |
| **模型类** | ≥ 60% | ≥ 50% | Model、Schema |

### 4.2 覆盖率工具

使用 `pytest-cov` 计算覆盖率：

```bash
# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html tests/

# 查看覆盖率报告
# 打开 htmlcov/index.html
```

## 5. 测试执行

### 5.1 本地执行

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api/test_auth.py

# 运行特定测试类
pytest tests/test_api/test_auth.py::TestAuth

# 跳过测试构建（不常用）
# pytest 不支持 skip tests，但可以用 pytest.mark.skip

# 查看覆盖率报告
pytest --cov=app --cov-report=html
```

### 5.2 CI/CD 集成

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        working-directory: ./backend
        run: |
          pytest --cov=app --cov-report=xml tests/

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend
```

## 6. 测试审查清单

在提交测试代码前，请确认：

- [ ] 测试命名清晰且表达意图
- [ ] 每个测试只验证一个行为
- [ ] 测试覆盖了正常流程和异常场景
- [ ] 使用了合适的断言
- [ ] Mock 了外部依赖
- [ ] 测试之间相互独立
- [ ] 清理了临时数据和资源
- [ ] 测试可重复运行且结果一致
- [ ] 添加了必要的注释说明复杂逻辑

## 7. 相关文档

### 7.1 设计规范文档
- [SPEC_FE_Coding.md](./SPEC_FE_Coding.md) - 前端编码规范
- [SPEC_BE_Coding.md](./SPEC_BE_Coding.md) - 后端编码规范

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
**最后更新**: 2026-05-16
