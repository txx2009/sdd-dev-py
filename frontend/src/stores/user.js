import { defineStore } from 'pinia';
import { login as loginApi, logout as logoutApi } from '@/api/auth';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      const response = await loginApi({ username, password });
      const { token, expiresIn } = response.data;
      this.token = token;
      localStorage.setItem('token', token);
      return { token, expiresIn };
    },

    async logout() {
      try {
        await logoutApi();
      } finally {
        this.token = '';
        this.userInfo = null;
        localStorage.removeItem('token');
      }
    },

    setUserInfo(userInfo) {
      this.userInfo = userInfo;
    },

    clearAuth() {
      this.token = '';
      this.userInfo = null;
      localStorage.removeItem('token');
    },
  },
});