import { createRouter, createWebHistory } from 'vue-router';
import adminRoutes from './admin';
// import userRoutes from './users';

const routes = [...adminRoutes/*, ...userRoutes*/];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


/* for authentication later */
// router.beforeEach((to, from, next) => {
//   const userRole = getUserRole(); // Replace with your auth logic
//   if (to.path.startsWith('/admin') && userRole !== 'admin') {
//     return next({ path: '/' });
//   }
//   next();
// });

export default router
