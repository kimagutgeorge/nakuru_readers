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
import ViewEvent from '@/views/admin/AdminViewEvent.vue'

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
          path: '/admin/manage-books', 
          name:'Genre',
          component: ManageBook
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
  