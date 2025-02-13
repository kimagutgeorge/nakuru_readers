<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Users</span></p>
      </div>
      <div class="col-100 admin-panel-body table-container">
        <table style="width:98%" class="my-tbl" cellspacing="0">
          <thead>
              <tr>
                  <th hidden>#</th>
                  <th style="width:50%;">User Details</th>
                  <th style="width:20%">Account Status</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(user, index) in users" :key="index">
                  <td hidden>{{ user.id }}</td>
                  <td class="col-flex">
                    <div class="col-20">
                      <img :src="user.photo" alt="" style="width:60px;">
                    </div>
                    <div class="col-80">
                      <p><span style="font-weight:bold">Name: </span>{{ user.f_name }} {{ user.l_name }}</p>
                      <p><span style="font-weight:bold">Email: </span>{{ user.email }}</p>
                      <p><span style="font-weight:bold">Phone: </span>+(254) {{ user.phone }}</p>
                    </div>
                    
                  </td>
                    <td>
                      <p><span class="status-indicator">{{ user.status }}</span></p>
                    </td>
                    <td>
                      <RouterLink :to="{ name: 'User Details', params: { id: user.id }}" :key="$route.fullPath"> 
                        <i class="fa-solid fa-eye front-blue"></i>
                        </RouterLink>
                    <i class="fa-solid fa-trash" @click="deleteUser(user.id)"></i>
                  </td>
              </tr>
              </tbody>
              </table>
      </div>
  </div>
</template>

<script>
import AdminResponse from '@/components/admin/AdminResponse.vue';
import axios from 'axios';

export default {
  name: 'Users',
  data() {
    return {
      responseClass: '',
      dbResponse: '',
      users: [],
    }
  },
  components: {
    AdminResponse
  },
  methods: {
    closeResponse() {
      this.responseClass = '';
      this.dbResponse = '';
    },
    async getUsers(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-users');

        const data = response.data;

        if (data.length > 0) {
          this.users = data;
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No users found!';
          }
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
    },
    deleteUser(id){
      const user_id = id
    }
  },
  mounted(){
    this.getUsers();
  }
}
</script>
