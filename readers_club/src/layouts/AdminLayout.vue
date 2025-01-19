<template>
    <div class="admin-layout">
      <div class="col-15">
        <AdminNavbar/>
      </div>
      <div class="col-85">
        <AdminTopBar/>
        <router-view />
      </div>
    </div>
  </template>
  <script>
import AdminNavbar from '@/components/admin/NavBar.vue';
import AdminTopBar from '@/components/admin/AdminTopBar.vue';

export default {
  name: 'HomeView',
  components: {
    AdminNavbar, AdminTopBar
  }
}
</script>