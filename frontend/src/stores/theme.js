import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  // 从 localStorage 恢复主题状态
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
  }

  // 监听变化，持久化并更新 DOM
  watch(
    isDark,
    (dark) => {
      localStorage.setItem('theme', dark ? 'dark' : 'light')
      document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
    },
    { immediate: true }
  )

  function toggleTheme() {
    isDark.value = !isDark.value
  }

  return { isDark, toggleTheme }
})
