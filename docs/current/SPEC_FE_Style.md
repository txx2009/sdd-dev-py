# 前端样式规范

**版本**: V1.0 | **日期**: 2026-05-16 | **状态**: 已审核

## 一、通用样式变量

### 1.1 字体体系

| 变量名 | 值 | 用途 |
|--------|-----|------|
| `--font-family` | 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif | 主字体 |
| `--font-size-base` | 14px | 基础字号 |
| `--font-size-sm` | 12px | 小字号 |
| `--font-size-lg` | 16px | 大字号 |
| `--font-size-xl` | 20px | 标题小 |
| `--font-size-2xl` | 24px | 标题大 |

> Plus Jakarta Sans 为 Google Fonts 开源字体，专为 SaaS 产品设计，兼顾专业性与友好感。[字体官网](https://fonts.google.com/specimen/Plus+Jakarta+Sans) | [CSS 引入](https://fonts.google.com/share?selection.family=Plus+Jakarta+Sans:wght@300;400;500;600;700)

### 1.2 过渡动画变量

| 变量名 | 值 | 用途 |
|--------|-----|------|
| `--transition-fast` | 150ms ease | 微交互（hover、focus） |
| `--transition-normal` | 200ms ease | 颜色变化 |
| `--transition-slow` | 300ms ease-in-out | 展开/收起、主题切换 |
| `--transition-page` | 150ms ease-out | 页面切换 |

> 动效时长应控制在 150-300ms，过长会让界面感觉迟钝。

### 1.3 鼠标指针变量

| 变量名 | 值 | 用途 |
|--------|-----|------|
| `--cursor-pointer` | pointer | 可点击元素 |
| `--cursor-default` | default | 默认元素 |
| `--cursor-not-allowed` | not-allowed | 禁用状态 |

> 所有可点击/可悬停元素必须声明 `cursor-pointer`，避免默认光标造成认知困惑。

### 1.4 颜色体系

#### 背景色

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-bg-primary` | #ffffff | #1a1a1a | 页面主背景 |
| `--color-bg-secondary` | #f5f7fa | #2d2d2d | 内容区块背景 |
| `--color-bg-tertiary` | #f0f2f5 | #3d3d3d | 卡片、表格背景 |
| `--color-bg-hover` | #e6e8eb | #4a4a4a | hover 状态背景 |

#### 文字色

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-text-primary` | #303133 | #e5eaf3 | 主文字 |
| `--color-text-secondary` | #606266 | #a0a8b3 | 辅助文字 |
| `--color-text-tertiary` | #909399 | #737373 | 三级文字 |
| `--color-text-disabled` | #c0c4cc | #525252 | 禁用状态文字 |

#### 边框色

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-border` | #dcdfe6 | #4a4a4a | 边框 |
| `--color-border-hover` | #c0c4cc | #606060 | hover 状态边框 |
| `--color-border-focus` | #409eff | #66b1ff | focus 状态边框 |

#### 主色调

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-primary` | #409eff | #66b1ff | 主色调（Element Plus） |
| `--color-danger` | #f56c6c | #f56c6c | 错误、危险操作 |
| `--color-success` | #67c23a | #67c23a | 成功状态 |
| `--color-warning` | #e6a23c | #e6a23c | 警告状态 |

#### 卡片色

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-card-bg` | #ffffff | #2d2d2d | 卡片背景 |
| `--color-card-border` | #e4e7ed | #4a4a4a | 卡片边框 |

### 1.5 侧边栏专用变量

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--color-sidebar-bg` | linear-gradient(180deg, #f5f7fa 0%, #f0f2f5 100%) | linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%) | 侧边栏背景（渐变） |
| `--color-sidebar-border` | #e4e7ed | transparent | 侧边栏边框 |
| `--color-sidebar-text` | #303133 | #e5eaf3 | 侧边栏文字 |
| `--color-sidebar-text-secondary` | #606266 | #a0a8b3 | 侧边栏辅助文字 |
| `--color-sidebar-text-active` | #409eff | #66b1ff | 激活菜单文字 |
| `--color-sidebar-item-hover` | rgba(64, 158, 255, 0.08) | rgba(102, 177, 255, 0.1) | 菜单项 hover 背景 |
| `--color-sidebar-item-active` | rgba(64, 158, 255, 0.15) | rgba(102, 177, 255, 0.2) | 激活菜单项背景 |
| `--color-sidebar-icon-bg` | rgba(64, 158, 255, 0.1) | rgba(102, 177, 255, 0.15) | 菜单图标背景 |
| `--color-sidebar-icon-active` | #409eff | #66b1ff | 激活菜单图标色 |

### 1.6 阴影层级

| 变量名 | 亮色值 | 暗色值 | 用途 |
|--------|--------|--------|------|
| `--shadow-sm` | 0 1px 2px 0 rgba(0, 0, 0, 0.05) | 0 1px 2px 0 rgba(0, 0, 0, 0.3) | 轻微浮起 |
| `--shadow-md` | 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1) | 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3) | 卡片、下拉菜单 |
| `--shadow-lg` | 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1) | 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4) | 弹窗 |

### 1.7 品牌主色

| 场景 | 亮色 | 暗色 |
|------|------|------|
| 主色 | `#409EFF` | `#66B1FF` |
| 悬停 | `#66B1FF` | `#8CC0FF` |
| 按下 | `#337ECC` | `#409EFF` |

> 注：品牌主色用于产品核心标识（Logo、主按钮、强调链接等），与系统主色 `--color-primary` 等价使用。

### 1.8 CSS 变量使用规范

所有颜色必须使用 CSS 变量，禁止硬编码色值：

```less
// ✅ 正确
.card {
  background: var(--color-card-bg);
  color: var(--color-text-primary);
  border: 1px solid var(--color-card-border);
  box-shadow: var(--shadow-sm);
  cursor: var(--cursor-pointer);
  transition: all var(--transition-normal);
}

// ❌ 错误
.card {
  background: #ffffff;
  color: #333;
  cursor: default;
}
```

## 二、交互状态规范

### 2.1 基础状态

| 状态 | 实现方式 | 效果 |
|------|----------|------|
| `hover` | 背景 `--color-bg-hover`，过渡 `--transition-normal` | 轻微高亮 |
| `active` | 背景加深 10% 或主色调 | 点击反馈 |
| `focus` | 边框 `--color-border-focus`，阴影 `--shadow-sm` | 聚焦标识 |
| `disabled` | 透明度 0.5，文字 `--color-text-disabled`，cursor: `--cursor-not-allowed` | 禁用标识 |

### 2.2 过渡动画

所有过渡动画必须使用 CSS 变量，便于统一管理和主题切换：

```less
// ✅ 正确
.button {
  transition: all var(--transition-normal);
}

// ❌ 错误
.button {
  transition: all 0.2s ease;
}
```

### 2.3 加载状态

| 元素 | 样式 |
|------|------|
| 按钮 | 旋转图标 + "加载中..."，禁用点击 |
| 页面 | 居中骨架屏或加载动画 |
| 列表 | 骨架行，高度与实际内容一致 |

### 2.4 错误状态

| 场景 | 样式 |
|------|------|
| 输入框 | 边框 `--color-danger`，下方红色错误文字 |
| 表单失败 | 错误提示条，背景 `--color-danger`，白色文字 |
| 页面失败 | 居中错误图标 + 信息 + 重试按钮 |

## 三、页面结构规范

### 3.1 页面基础结构

```vue
<template>
  <div class="page-container">
    <header class="page-header">
      <h1 class="page-title">页面标题</h1>
    </header>
    <main class="page-content">
      <!-- 内容区域 -->
    </main>
  </div>
</template>
```

### 3.2 页面布局规则

| 规则 | 说明 |
|------|------|
| 页面容器 | `padding: 24px`，背景 `--color-bg-secondary` |
| 页面标题 | 字号 `--font-size-2xl`，字重 600，下方间距 16px |
| 内容区块 | 背景 `--color-bg-primary` + 阴影 `--shadow-sm` |
| 区块间距 | 使用 24px |

### 3.3 卡片规范

| 属性 | 值 |
|------|-----|
| 背景 | `--color-bg-primary` |
| 边框 | `--color-card-border` |
| 阴影 | `--shadow-sm` 或 `--shadow-md` |
| 内边距 | 16px 或 2rem（按组件调整） |
| 交互 | 必须添加 `cursor: var(--cursor-pointer)` |

## 四、使用指南

### 4.1 字体引入

在 `index.html` 或 `main.js` 中引入 Plus Jakarta Sans 字体：

```html
<!-- index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

或在 `main.js` 中引入：

```javascript
// main.js
import 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap'
```

### 4.2 文件引入

```javascript
// main.js
import './assets/styles/index.less'
```

样式文件导入顺序：
1. `theme.less` — 主题变量
2. `base.less` — 基础样式重置
3. `index.less` — 全局组件样式

### 4.3 变量使用方式

```css
/* 直接使用 */
.card {
  background: var(--color-bg-primary);
}

/* 渐变使用 */
.sidebar {
  background: var(--color-sidebar-bg);
}

/* 半透明叠加 */
.overlay {
  background: var(--color-sidebar-item-hover);
}

/* 过渡动画 */
.button {
  transition: all var(--transition-normal);
}

/* 鼠标指针 */
.clickable-element {
  cursor: var(--cursor-pointer);
}
```

### 4.4 主题切换

通过 `<html class="dark">` 控制，CSS 变量自动切换。Element Plus 主题通过 `ElConfigProvider` 组件的 `predefine` 属性自定义主题变量。

```html
<html class="dark">  <!-- 暗色 -->
<html>               <!-- 亮色（默认） -->
```

### 4.5 无障碍支持

#### 减少动效偏好

必须尊重用户的系统动效偏好设置，在全局样式中添加：

```less
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

> 连续动画容易分散注意力，仅用于加载指示器。对于装饰性元素禁止使用无限动画。

#### Focus 可见性

所有可交互元素必须具有清晰的 focus 状态：

```less
// ✅ 正确
.button:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
  box-shadow: var(--shadow-sm);
}

// ❌ 错误 - 仅依靠浏览器默认 outline
.button:focus {
  outline: none;
}
```

#### 颜色对比度

文本与背景的颜色对比度必须满足 WCAG 2.1 AA 标准（4.5:1）：

| 场景 | 最小对比度 |
|------|-----------|
| 普通文本 | 4.5:1 |
| 大文本（>=18px 或 14px 粗体） | 3:1 |
| UI 组件边界 | 3:1 |

---

**文档版本**: V1.0R26C00
**创建日期**: 2026-05-16
