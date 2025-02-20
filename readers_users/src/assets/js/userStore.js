import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    setUser(userData) {
      this.user = userData;
      localStorage.setItem('user', JSON.stringify(userData)); // Persist user data
    },
    clearUser() {
      this.user = null;
      localStorage.removeItem('user'); // Remove user on logout
    }
  }
});
