import { createRouter, createWebHistory } from 'vue-router'
import UserSignUp from '@/views/UserSignUp.vue'
import UserLogin from '@/views/UserLogin.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/signup',
    name: 'Sign Up',
    component: UserSignUp
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
