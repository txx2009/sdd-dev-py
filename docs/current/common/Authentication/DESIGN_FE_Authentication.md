# 认证模块前端设计文档

> **版本**: V1.0R26C00
> **项目**: AI-EXAM-BASE-PYTHON
> **模块**: Authentication-FE
> **归档日期**: 2026-05-16
> **源文档**: `docs/superpowers/specs/2026-05-16-authentication-design.md`

---

## 1. 概述

认证前端模块提供用户登录、登出及用户管理界面，采用 JWT Token 无状态认证方案。

### 1.1 核心功能

- **登录页面**: 用户名密码登录，获取并存储 JWT Token
- **用户管理页面**: 用户列表查询、创建、编辑、删除

### 1.2 技术选型

| 技术 | 说明 |
|------|------|
| Vue 3 | 前端框架 |
| Axios | HTTP 客户端 |
| Pinia | 状态管理 |
| Vue Router | 路由管理 |
| Element Plus | UI 组件库 |

---

## 2. 前端目录结构

```
frontend/src/
├── api/
│   └── index.js           # 统一 API 客户端（含拦截器）
├── views/
│   ├── login/
│   │   └── index.vue      # 登录页
│   └── users/
│       └── index.vue      # 用户管理页
├── stores/
│   ├── auth.js            # 认证状态
│   └── theme.js           # 主题状态
├── router/
│   └── index.js           # 路由配置（含守卫）
└── main.js
```

---

## 3. 页面组件

### 3.1 登录页 `/login`

| 功能 | 说明 |
|------|------|
| 用户名输入 | 表单字段 |
| 密码输入 | 表单字段，支持显示/隐藏 |
| 登录按钮 | 提交表单 |
| 错误提示 | 登录失败时显示 |

**交互流程**:
1. 用户输入用户名密码
2. 点击登录，调用 `POST /api/v1/auth/login`
3. 成功后存储 Token 到 localStorage
4. 跳转到 `/users`

### 3.2 用户管理页 `/users`

| 功能 | 说明 |
|------|------|
| 用户列表 | 分页展示用户信息 |
| 创建用户 | 弹窗表单 |
| 编辑用户 | 弹窗表单 |
| 删除用户 | 确认对话框 |
| 修改密码 | 弹窗表单 |

---

## 4. API 封装

统一在 `src/api/index.js` 中封装：

```javascript
// 认证相关
POST   /api/v1/auth/login     # 登录
POST   /api/v1/auth/logout    # 登出
GET    /api/v1/auth/me        # 获取当前用户

// 用户管理相关
GET    /api/v1/users                # 用户列表
POST   /api/v1/users                # 创建用户
GET    /api/v1/users/{id}           # 用户详情
PUT    /api/v1/users/{id}           # 更新用户
DELETE /api/v1/users/{id}           # 删除用户
PUT    /api/v1/users/{id}/password  # 修改密码
```

---

## 5. 路由守卫

| 场景 | 行为 |
|------|------|
| 未登录访问 `/users` | 跳转 `/login` |
| 已登录访问 `/login` | 跳转 `/users` |
| Token 过期（401） | 清除 Token，跳转 `/login` |

---

## 6. 核心代码位置

| 组件 | 文件路径 |
|------|----------|
| API 封装 | `frontend/src/api/index.js` |
| 登录页面 | `frontend/src/views/login/index.vue` |
| 用户管理页 | `frontend/src/views/users/index.vue` |
| 路由配置 | `frontend/src/router/index.js` |
| 认证状态 | `frontend/src/stores/auth.js` |
| 主题状态 | `frontend/src/stores/theme.js` |

---

## 7. 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-16 | V1.0R26C00 | 初始版本 |
