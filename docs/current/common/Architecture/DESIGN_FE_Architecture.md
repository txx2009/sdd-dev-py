# DESIGN_FE_Architecture - 前端工程架构设计

> **版本**: V1.0
> **日期**: 2026-05-16
> **项目**: AI-EXAM-BASE-PYTHON

---

## 1. 概述

前端工程采用 Vue 3 + Vite 技术体系，实现管理后台项目。

### 1.1 目标

- 搭建 Vue 3 + Vite 前端工程
- 集成 Element Plus 作为 UI 组件库
- 实现暗色/亮色主题切换功能
- 搭建基础管理后台布局框架
- 与项目现有 SPEC_FE_Style.md 样式规范保持一致

### 1.2 约束

- 暂不做权限管理（后续扩展）
- 暂不做多语言支持（后续扩展）
- 仅支持中文界面

## 2. 技术方案

### 2.1 技术栈选型

| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | Vue.js | 3.x | Composition API |
| 构建工具 | Vite | 5.x | 快速开发体验 |
| UI 组件库 | Element Plus | 2.x | Vue 3 组件库 |
| 状态管理 | Pinia | 2.x | Vue 3 官方推荐 |
| 路由 | Vue Router | 4.x | SPA 路由管理 |
| HTTP 客户端 | Axios | 1.x | HTTP 请求 |

### 2.2 依赖说明

```json
{
  "dependencies": {
    "vue": "^3.4.x",
    "vue-router": "^4.3.x",
    "pinia": "^2.1.x",
    "element-plus": "^2.5.x",
    "axios": "^1.7.x",
    "@element-plus/icons-vue": "^2.3.x"
  },
  "devDependencies": {
    "vite": "^5.4.x",
    "@vitejs/plugin-vue": "^5.x"
  }
}
```

## 3. 项目结构

```
frontend/                          # 前端工程目录
├── public/                         # 静态资源
│   └── favicon.ico                # 网站图标
├── src/
│   ├── assets/                    # 资源文件
│   │   └── styles/                # 样式目录
│   │       ├── theme.less         # 主题变量
│   │       ├── base.less          # 基础样式重置
│   │       └── index.less         # 样式入口文件
│   ├── components/                # 公共组件
│   │   └── common/                # 通用组件
│   │       └── ThemeSwitch.vue    # 主题切换组件
│   ├── layouts/                   # 布局组件
│   │   └── MainLayout.vue         # 主布局
│   ├── router/                    # 路由配置
│   │   └── index.js               # 路由定义
│   ├── stores/                    # Pinia 状态管理
│   │   └── theme.js               # 主题状态管理
│   ├── views/                     # 页面视图
│   │   ├── dashboard/             # 仪表盘
│   │   │   └── index.vue
│   │   └── login/                 # 登录页
│   │       └── index.vue
│   ├── App.vue                    # 根组件
│   ├── main.js                    # 入口文件
│   └── api/                       # API 请求模块
│       └── index.js               # Axios 实例配置
├── .env.development               # 开发环境配置
├── .env.production                # 生产环境配置
├── index.html                     # HTML 入口
├── package.json
├── vite.config.js                 # Vite 配置
└── README.md                      # 工程说明文档
```

## 4. 核心功能设计

### 4.1 暗色/亮色主题切换

使用 Element Plus 的 `ElConfigProvider` 组件 + CSS 变量实现主题切换。

**CSS 变量定义**（基于 SPEC_FE_Style.md）：

```less
// 亮色主题
:root {
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f5f7fa;
  --color-text-primary: #303133;
  --color-primary: #409eff;
}

// 暗色主题
html.dark {
  --color-bg-primary: #1a1a1a;
  --color-bg-secondary: #2d2d2d;
  --color-text-primary: #e5eaf3;
  --color-primary: #66b1ff;
}
```

### 4.2 管理后台布局

主布局结构：Header (64px) + Sidebar (200px/64px 折叠) + Content Area

- 侧边栏：Logo + 系统名称 + 导航菜单（可折叠）
- Header：折叠按钮 + 主题切换 + 用户头像

### 4.3 路由配置

```javascript
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘' }
      }
    ]
  }
]
```

## 5. 环境配置

### 5.1 .env.development

```env
VITE_APP_TITLE=AI-EXAM-BASE-PYTHON
VITE_API_BASE_URL=http://localhost:5000/api
VITE_SPAWN_BACKEND=false
```

### 5.2 .env.production

```env
VITE_APP_TITLE=AI-EXAM-BASE-PYTHON
VITE_API_BASE_URL=/api
VITE_SPAWN_BACKEND=false
```

## 6. 样式规范适配

详见 [SPEC_FE_Style.md](../SPEC_FE_Style.md)

### 6.1 样式文件加载顺序

1. `theme.less` - 主题变量定义
2. `base.less` - 基础样式重置
3. `index.less` - 全局样式入口

## 7. 验收标准

- [ ] Vue 3 工程使用 Vite 构建启动成功
- [ ] Element Plus 组件正常渲染
- [ ] 暗色/亮色主题切换正常
- [ ] 侧边栏导航可折叠
- [ ] 登录页和仪表盘页面可访问
- [ ] `npm run dev` 仅前端开发模式正常启动
- [ ] 样式规范与 SPEC_FE_Style.md 变量保持一致

## 8. 待后续扩展功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 权限管理 | 菜单/按钮级别权限控制 | P1 |
| 多语言 | 中英文切换 | P2 |
| 实际认证 | 登录接口对接 | P1 |
| 用户管理模块 | CRUD 基础模块 | P2 |

---

## 关联文档

- [SPEC_Architecture.md](../SPEC_Architecture.md) - 架构设计规范
- [SPEC_FE_Coding.md](../SPEC_FE_Coding.md) - 前端编码规范
- [SPEC_FE_Style.md](../SPEC_FE_Style.md) - 前端样式规范
