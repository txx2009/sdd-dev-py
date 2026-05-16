# SDD-DEV Frontend

## 项目简介

SDD-DEV 前端管理后台，基于 Vue 3 + Vite + Ant Design Vue 构建。

## 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue.js | 3.4.x |
| 构建工具 | Vite | 5.4.x |
| UI 组件库 | Ant Design Vue | 4.2.x |
| 状态管理 | Pinia | 2.1.x |
| 路由 | Vue Router | 4.3.x |
| HTTP 客户端 | Axios | 1.7.x |
| CSS 预处理器 | Less | 4.2.x |

## 开发

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 目录结构

```
frontend/
├── src/
│   ├── assets/          # 静态资源
│   ├── components/       # 公共组件
│   ├── layouts/         # 布局组件
│   ├── router/          # 路由配置
│   ├── stores/          # 状态管理
│   ├── views/           # 页面视图
│   ├── api/             # API 请求
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── .env.development     # 开发环境配置
├── .env.production      # 生产环境配置
├── index.html           # HTML 入口
├── package.json
├── vite.config.js       # Vite 配置
└── README.md
```

## 环境变量

| 变量名 | 说明 | 开发环境 | 生产环境 |
|--------|------|----------|----------|
| VITE_APP_TITLE | 应用标题 | SDD-DEV | SDD-DEV |
| VITE_API_BASE_URL | API 基础路径 | http://localhost:8080/api | /api |
| VITE_SPAWN_BACKEND | 是否启动后端 | false | false |
