<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Events</span></p>
      </div>
      <div class="col-100 admin-panel-body table-container">
        <table style="width:98%" class="my-tbl" cellspacing="0">
          <thead>
              <tr>
                  <th hidden>#</th>
                  <th style="width:40%;">Event</th>
                  <th style="width:30%">Location & Time</th>
                  <th style="width:10%">Status</th>
                  <th>Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(user, index) in users" :key="index">
                  <td hidden>{{ user.id }}</td>
                  <td>
                    
                  </td>
                    <td>
                      <p><span class="status-indicator">{{ user.status }}</span></p>
                    </td>
                    <td>

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
  name: 'Events',
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
    async getEvents(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-events');

        const data = response.data;

        if (data.length > 0) {
          this.users = data;
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No events found!';
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
    this.getEvents();
  }
}
</script>
