import { createRouter, createWebHistory } from 'vue-router'
import UserSignUp from '@/views/UserSignUp.vue'
import UserLogin from '@/views/UserLogin.vue'
import HomeView from '@/views/HomeView.vue'
import UserProfile from '@/views/UserProfile.vue'

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
  },
  {
    path:'/profile',
    name: 'UserProfile',
    component: UserProfile
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
