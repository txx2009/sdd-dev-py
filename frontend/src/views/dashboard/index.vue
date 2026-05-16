<template>
  <div class="page-container">
    <header class="page-header">
      <h1 class="page-title">仪表盘</h1>
    </header>
    <main class="page-content">
      <a-row :gutter="[24, 24]">
        <a-col :span="24">
          <div class="content-card welcome-card">
            <h2>欢迎使用 SDD-DEV 管理后台</h2>
            <p>这是一个基于 Vue 3 + Ant Design Vue 构建的管理系统。</p>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="8">
          <div class="content-card stat-card">
            <div class="stat-icon stat-icon-primary">
              <UserOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-value">-</div>
              <div class="stat-label">用户数</div>
            </div>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="8">
          <div class="content-card stat-card">
            <div class="stat-icon stat-icon-success">
              <FileTextOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-value">-</div>
              <div class="stat-label">文章数</div>
            </div>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="8">
          <div class="content-card stat-card">
            <div class="stat-icon stat-icon-warning">
              <AlertOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-value">-</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </a-col>
      </a-row>
    </main>
  </div>
</template>

<script setup>
import { UserOutlined, FileTextOutlined, AlertOutlined } from '@ant-design/icons-vue'
</script>

<style scoped lang="less">
.welcome-card {
  text-align: center;
  padding: 48px 24px;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }

  h2 {
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 12px;
  }

  p {
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
    margin: 0;
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  transition: box-shadow var(--transition-normal), border-color var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--color-border-hover);
  }
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: transform var(--transition-normal);

  &:hover {
    transform: scale(1.05);
  }
}

.stat-icon-primary {
  background: rgba(19, 75, 234, 0.1);
  color: var(--color-primary);
}

.stat-icon-success {
  background: rgba(22, 163, 74, 0.1);
  color: var(--color-success);
}

.stat-icon-warning {
  background: rgba(243, 167, 0, 0.1);
  color: var(--color-warning);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-top: 4px;
}
</style>
