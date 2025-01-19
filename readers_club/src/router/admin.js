export default [
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      children: [
        { path: '/admin/dashboard', component: () => import('@/views/admin/AdminDashboard.vue') },
        { path: '/admin/users', component: () => import('@/views/admin/AdminUsers.vue') },
        { path: '/admin/events', component: () => import('@/views/admin/AdminEvents.vue') },
        { path: '/admin/books', component: () => import('@/views/admin/AdminBooks.vue') },
        { path: '/admin/add-book', component: () => import('@/views/admin/AddBook.vue') },
      ],
    },
  ];
  