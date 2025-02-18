import Home from '@/views/admin/AdminDashboard.vue';
import Users from '@/views/admin/AdminUsers.vue';
import Events from '@/views/admin/AdminEvents.vue';
import Books from '@/views/admin/AdminBooks.vue';
import AddBook from '@/views/admin/AddBook.vue';
import AdminProduct from '@/views/admin/AdminProduct.vue';
import ManageBook from '@/views/admin/ManageBook.vue';
import AdminCollection from '@/views/admin/ManageCollection.vue'
import AddUser from '@/views/admin/AddUser.vue';
import AdminViewUser from '@/views/admin/AdminViewUser.vue';
import AddEvent from '@/views/admin/AddEvent.vue';
import ViewEvent from '@/views/admin/AdminViewEvent.vue';
import Orders from '@/views/admin/AdminOrders.vue';
import Payments from '@/views/admin/AdminPayment.vue';
import AdminRating from '@/views/admin/AdminRating.vue';
import AdminSettings from '@/views/admin/AdminSettings.vue';
import AdminPaymentSettings from '@/views/admin/AdminPaymentSettings.vue';
import AdminGuidelines from '@/views/admin/AdminGuidelines.vue';
import AdminReads from '@/views/admin/AdminReads.vue';
import AddRead from '@/views/admin/AddRead.vue';
import AdminViewRead from '@/views/admin/AdminViewRead.vue';
import AdminRoles from '@/views/admin/AdminRoles.vue';

export default [
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      children: [
        { 
          path: '/admin/dashboard', 
          name: 'HomeView',
          component: Home
        },
        { 
          path: '/admin/users', 
          name: 'Users',
          component: Users
        },
        { path: '/admin/events', 
          name:'Events',
          component: () => Events
        },
        { 
          path: '/admin/books', 
          name:'Books',
          component: Books,
        },
        { 
          path: '/admin/add-book',
          name:'AddBook', 
          component: AddBook
        },
        {
          path: '/admin/add-event',
          name:'AddEvent',
          component: AddEvent
        },
        {
          path:'/admin/orders',
          name:'Orders',
          component:Orders
        },
        {
          path:'/admin/payments',
          name:'Payments',
          component:Payments
        },
        {
          path:'/admin/roles',
          name: 'AdminRoles',
          component: AdminRoles
        },
        {
          path:'/admin/rating',
          name:'Ratings',
          component:AdminRating
        },
        {
          path:'/admin/reads',
          name: 'Reads',
          component: AdminReads
        },
        {
          path:'/admin/add-read',
          name: 'AddRead',
          component: AddRead
        },
        { 
          path: '/admin/product/:id', 
          name:'Product Details',
          component: AdminProduct,
          props:true
        },
        { 
          path: '/admin/event/:id', 
          name:'Event Details',
          component: ViewEvent,
          props:true
        },
        { 
          path: '/admin/user/:id', 
          name:'User Details',
          component: AdminViewUser,
          props:true
        },
        { 
          path: '/admin/read/:id', 
          name:'Read Details',
          component: AdminViewRead,
          props:true
        },
        { 
          path: '/admin/manage-books', 
          name:'Genre',
          component: ManageBook
        },
        { 
          path: '/admin/settings', 
          name:'Settings',
          component: AdminSettings
        },
        {
          path:'/admin/payment-settings',
          name:'Payment Settings',
          component: AdminPaymentSettings
        },
        {
          path:'/admin/guidelines',
          name:'Guidelines',
          component: AdminGuidelines
        },
        { path: '/admin/manage-collections', 
          name:'Collections',
          component: AdminCollection
        },
        { path: '/admin/add-user', 
          name:'AddUser',
          component: AddUser
        },
      ],
    },
  ];
  