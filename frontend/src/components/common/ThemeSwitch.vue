<template>
  <a-tooltip :title="isDark ? '切换亮色模式' : '切换暗色模式'" placement="bottom">
    <a-switch
      :checked="isDark"
      checked-children="🌙"
      un-checked-children="☀️"
      @change="toggleTheme"
    />
  </a-tooltip>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const isDark = computed(() => themeStore.isDark)

function toggleTheme() {
  themeStore.toggleTheme()
}
</script>
