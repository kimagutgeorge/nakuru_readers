import { createRouter, createWebHistory } from 'vue-router'
import UserSignUp from '@/views/UserSignUp.vue'
import UserLogin from '@/views/UserLogin.vue'
import HomeView from '@/views/HomeView.vue'
import UserProfile from '@/views/UserProfile.vue'
import UserReads from '@/views/UserReads.vue'
import UserMessages from '@/views/UserMessages.vue'
import UserReadsDetails from '@/views/UserReadsDetails.vue'

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
  },
  {
    path: '/messages',
    name: 'UserMessages',
    component: UserMessages
  },
  {
    path: '/reads',
    name: 'UserReads',
    component: UserReads
  },
  {
    path: '/read/:id',
    name: 'Read Details',
    component: UserReadsDetails,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
