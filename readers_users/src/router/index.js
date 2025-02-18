import { createRouter, createWebHistory } from 'vue-router'
import UserSignUp from '@/views/UserSignUp.vue'
import UserLogin from '@/views/UserLogin.vue'
import HomeView from '@/views/HomeView.vue'

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
  },
  {
    path:'/home',
    name: 'HomeView',
    component: HomeView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
