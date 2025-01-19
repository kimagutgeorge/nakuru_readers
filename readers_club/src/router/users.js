export default [
    {
      path: '/',
      component: () => import('@/layouts/UserLayout.vue'),
      children: [
        { path: '', component: () => import('@/views/users/Home.vue') },
        { path: 'profile', component: () => import('@/views/users/Profile.vue') },
        { path: 'settings', component: () => import('@/views/users/Settings.vue') },
      ],
    },
  ];
  