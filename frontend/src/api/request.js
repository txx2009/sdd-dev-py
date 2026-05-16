import axios from 'axios';
import { message } from 'ant-design-vue';

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
});

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const { response } = error;

    // 解析统一错误格式: { error: { code, message } }
    // 优先使用后端返回的 message，后端没有返回时才使用默认提示
    let errorMessage = null;

    if (response?.data?.error?.message) {
      errorMessage = response.data.error.message;
    }

    // 401 需要特殊处理：清除 token 并跳转登录
    if (response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    // 显示错误提示（如果有后端返回的 message）
    if (errorMessage) {
      message.error(errorMessage);
    }

    // 抛出统一格式的错误对象
    const err = new Error(errorMessage || '请求失败');
    err.code = response?.data?.error?.code || response?.status;
    err.response = response;
    return Promise.reject(err);
  }
);

export default request;
