<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">SDD-DEV</h1>
        <p class="login-subtitle">管理后台</p>
      </div>

      <a-form
        :model="formState"
        :rules="rules"
        @finish="handleLogin"
        class="login-form"
      >
        <a-form-item name="username">
          <a-input
            v-model:value="formState.username"
            size="large"
            placeholder="用户名"
          >
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item name="password">
          <a-input-password
            v-model:value="formState.password"
            size="large"
            placeholder="密码"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            block
            :loading="loading"
            class="login-button"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const loading = ref(false)

const formState = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码' }]
}

async function handleLogin() {
  loading.value = true
  try {
    const userStore = useUserStore()
    await userStore.login(formState.username, formState.password)
    message.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    message.error(error.response?.data?.message || error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="less">
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-sidebar-bg);
  transition: background var(--transition-slow);
}

.login-card {
  width: 400px;
  padding: 40px;
  background: var(--color-card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-card-border);
  transition: box-shadow var(--transition-normal), border-color var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-lg);
    border-color: var(--color-border-hover);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-primary);
  margin: 0 0 8px;
  transition: color var(--transition-normal);
}

.login-subtitle {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

.login-form {
  :deep(.ant-input-affix-wrapper),
  :deep(.ant-input) {
    background: var(--color-bg-secondary);
    border-color: var(--color-border);
    transition: all var(--transition-normal);

    &:hover {
      border-color: var(--color-primary);
    }

    &:focus {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 2px rgba(19, 75, 234, 0.1);
    }
  }
}

.login-button {
  transition: all var(--transition-normal);

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }
}
</style>
