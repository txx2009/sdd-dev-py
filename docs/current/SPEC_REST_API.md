# SPEC_REST_API - REST 接口设计规范

本文档定义了 AI-EXAM-BASE-PYTHON 项目的 RESTful API 设计规范。

## 1. 协议基础 (Protocol Basics)

### 1.1 通信协议
- 默认使用 **HTTP/1.1** 或 **HTTP/2**。
- 生产环境强制使用 **HTTPS**。

### 1.2 接口版本控制
- 采用 URL 路径版本控制。
- 格式：`/api/v{version}/{resource}`
- 示例：`/api/v1/users`, `/api/v2/products`

### 1.3 数据传输格式
- **Content-Type**: `application/json; charset=UTF-8`
- 请求体和响应体均默认为 JSON 格式。
- 时间格式：统一使用 ISO-8601 标准或时间戳（推荐 ISO-8601）。

## 2. 资源定义与 URL 命名 (Resource & URL Naming)

采用**面向资源**的设计风格。

### 2.1 命名规范
- **使用名词**：URL 中应仅包含名词，避免动词（如 `/getUsers` 是错误的）。
- **复数形式**：资源名称统一使用复数形式。
- **连字符**：多个单词使用连字符 `-` 分隔（kebab-case），避免下划线或驼峰。
- **层级结构**：体现资源间的从属关系。

### 2.2 示例
- 获取用户列表：`GET /api/v1/users`
- 获取特定用户：`GET /api/v1/users/{id}`
- 创建用户：`POST /api/v1/users`
- 获取用户的订单：`GET /api/v1/users/{id}/orders`

### 2.3 HTTP 方法语义

| 方法 | 描述 | 幂等性 | 安全性 |
| :--- | :--- | :--- | :--- |
| **GET** | 获取资源或资源列表 | 是 | 是 |
| **POST** | 创建新资源 | 否 | 否 |
| **PUT** | 更新资源（全量或部分），或创建指定 ID 的资源 | 是 | 否 |
| **DELETE** | 删除资源 | 是 | 否 |

## 3. 响应规范 (Response)

所有接口统一返回 JSON 格式响应。

### 3.1 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

**单个对象响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": { "id": 1, "name": "user" }
}
```

**列表分页响应**:
当 `data` 为数组时，必须包含分页元数据。
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "id": 1, "name": "user1" },
    { "id": 2, "name": "user2" }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 100
  }
}
```

### 3.2 错误响应

```json
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

### 3.3 禁止裸数组返回

所有接口的 `data` 字段不允许直接返回原始类型数组（如 `string[]`、`number[]`），必须包装为对象数组。

**错误示例**:
```json
{
  "data": ["产品A", "产品B", "产品C"]
}
```

**正确示例**:
```json
{
  "data": [
    { "name": "产品A" },
    { "name": "产品B" },
    { "name": "产品C" }
  ]
}
```

## 4. 分页与排序

**请求参数**: `page` (默认1), `size` (默认10), `sort` (字段+排序)。

**分页响应**: 分页查询在 **Service 层内部** 处理分页逻辑，API 层直接返回。

| 字段 | 类型 | 说明 |
|------|------|------|
| data | `List` | 数据列表 |
| pagination.page | `Integer` | 当前页码 |
| pagination.size | `Integer` | 每页条数 |
| pagination.total | `Integer` | 总记录数 |

## 5. 状态码 (Status Codes)

使用业务状态码（与 HTTP 状态码配合）：

| HTTP 状态码 | 业务码 | 含义 |
|------------|--------|------|
| 200 | 200 | 成功 |
| 201 | 201 | 创建成功 |
| 400 | 400 | 参数错误 |
| 401 | 401 | 未登录 |
| 403 | 403 | 无权限 |
| 404 | 404 | 资源未找到 |
| 500 | 500 | 系统错误 |

## 6. 最佳实践

1. **Schema**: 请求/响应使用专用 Pydantic Schema，避免直接暴露模型。
2. **校验**: 使用 Pydantic 进行数据验证。
3. **空值**: 集合返 `[]`，对象返 `{}`，避免 `null`。
4. **幂等性**: GET、PUT、DELETE 应为幂等操作。

## 7. 示例 (Example)

```python
# Flask 路由示例
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/users', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)

    users = user_service.list_users(page=page, size=size)
    total = user_service.count_users()

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': [user.to_dict() for user in users],
        'pagination': {
            'page': page,
            'size': size,
            'total': total
        }
    })

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({
            'code': 404,
            'message': '用户不存在',
            'data': None
        }), 404

    return jsonify({
        'code': 200,
        'message': 'success',
        'data': user.to_dict()
    })
```

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
