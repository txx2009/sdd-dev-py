<template>
  <a-config-provider :theme="antTheme">
    <a-layout class="main-layout">
      <!-- 侧边栏 -->
      <a-layout-sider
        v-model:collapsed="collapsed"
        :trigger="null"
        collapsible
        class="sidebar"
        :style="{ background: 'var(--color-sidebar-bg)' }"
      >
        <div class="logo">
          <span v-if="!collapsed" class="logo-text">SDD-DEV</span>
          <span v-else class="logo-text-collapsed">SD</span>
        </div>
        <a-menu
          v-model:selectedKeys="selectedKeys"
          theme="light"
          mode="inline"
          class="sidebar-menu"
        >
          <a-menu-item key="/dashboard" @click="handleMenuClick('/dashboard')">
            <DashboardOutlined />
            <span>仪表盘</span>
          </a-menu-item>
          <a-menu-item key="/users" @click="handleMenuClick('/users')">
            <UserOutlined />
            <span>用户管理</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>

      <a-layout>
        <!-- Header -->
        <a-layout-header class="header">
          <div class="header-left">
            <menu-unfold-outlined v-if="collapsed" class="trigger" @click="toggleSidebar" />
            <menu-fold-outlined v-else class="trigger" @click="toggleSidebar" />
          </div>
          <div class="header-right">
            <ThemeSwitch />
            <a-dropdown class="user-dropdown">
              <a-avatar style="background-color: var(--color-primary); cursor: pointer">
                U
              </a-avatar>
              <template #overlay>
                <a-menu>
                  <a-menu-item key="logout" @click="handleLogout">
                    <LogoutOutlined />
                    退出登录
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </div>
        </a-layout-header>

        <!-- 内容区 -->
        <a-layout-content class="content">
          <router-view />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-config-provider>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { DashboardOutlined, MenuUnfoldOutlined, MenuFoldOutlined, LogoutOutlined, UserOutlined } from '@ant-design/icons-vue'
import ThemeSwitch from '@/components/common/ThemeSwitch.vue'
import { useThemeStore } from '@/stores/theme'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()
const userStore = useUserStore()

const collapsed = ref(false)
const selectedKeys = ref([route.path])

// Ant Design Vue 主题配置
const antTheme = computed(() => ({
  token: {
    colorPrimary: themeStore.isDark ? '#5b7fef' : '#134bea'
  }
}))

function toggleSidebar() {
  collapsed.value = !collapsed.value
}

function handleMenuClick(path) {
  router.push(path)
}

async function handleLogout() {
  try {
    await userStore.logout()
    message.success('已退出登录')
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
  }
}
</script>

<style scoped lang="less">
.main-layout {
  min-height: 100vh;
}

.sidebar {
  min-height: 100vh;
  background: var(--color-sidebar-bg) !important;
  border-right: 1px solid var(--color-sidebar-border);

  :deep(.ant-layout-sider-children) {
    display: flex;
    flex-direction: column;
  }
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--color-sidebar-border);
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-sidebar-text);
  letter-spacing: 1px;
}

.logo-text-collapsed {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-sidebar-text);
}

.sidebar-menu {
  background: transparent !important;
  border: none;

  :deep(.ant-menu-item) {
    color: var(--color-sidebar-text);
    margin: 4px 8px;
    border-radius: 6px;

    &:hover {
      background: var(--color-sidebar-item-hover) !important;
    }

    &.ant-menu-item-selected {
      background: var(--color-sidebar-item-active) !important;
      color: var(--color-sidebar-text-active);

      .anticon {
        color: var(--color-sidebar-icon-active);
      }
    }
  }

  :deep(.ant-menu-item .anticon) {
    color: var(--color-sidebar-text-secondary);
  }
}

.header {
  background: var(--color-bg-primary);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-sm);
  border-bottom: 1px solid var(--color-border);
}

.header-left {
  display: flex;
  align-items: center;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  color: var(--color-text-primary);
  transition: color 0.2s;

  &:hover {
    color: var(--color-primary);
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-dropdown {
  cursor: pointer;
}

.content {
  margin: 24px;
  min-height: calc(100vh - 64px - 48px);
}
</style>
