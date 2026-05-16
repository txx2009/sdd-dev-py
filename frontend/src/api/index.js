import axios from 'axios'
import { message } from 'ant-design-vue'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可在此添加 token 等认证信息
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    const { data } = response
    if (data.code !== 0) {
      message.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
    return data
  },
  (error) => {
    if (error.response) {
      const { status } = error.response
      if (status === 401) {
        message.error('登录已过期，请重新登录')
        // 可跳转至登录页
      } else if (status === 403) {
        message.error('没有权限')
      } else if (status === 500) {
        message.error('服务器错误')
      } else {
        message.error('请求失败')
      }
    } else {
      message.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default apiClient
