<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Users</span></p>
      </div>
      <div class="col-100 admin-panel-body table-container">
        <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
          <thead>
              <tr>
                  <th hidden>#</th>
                  <th style="width:70%;">User Name</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(user, index) in users" :key="index">
                  <td hidden>{{ user.id }}</td>
                  <td>
                    {{ user.name }}
                  </td>
                  <td>
                    <i 
                    :class="user.isReadOnly ? 'fa-solid fa-edit text-primary' : 'fa-solid fa-check text-success'"
                    @click="user.isReadOnly ? makeEditable(index) : saveuser(user.id, user.name)"
                    ></i>
                    <i 
                    :class="user.status === 1 ? 'fa-solid fa-toggle-on text-success' : 'fa-solid fa-toggle-off text-danger'" 
                    @click="toggleStatus(user)"
                    ></i>
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
    }
  },
  mounted(){
    this.getUsers();
  }
}
</script>
