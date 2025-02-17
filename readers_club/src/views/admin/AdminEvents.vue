<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span class="title-label">Events</span></p>
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
              <tr v-for="(event, index) in events" :key="index">
                  <td hidden>{{ event.id }}</td>
                  <td class="col-row" :class="{'editable-input': !event.isReadOnly, 'read-only-input': event.isReadOnly}" style="width:40%" >
                    <div class="full_width_td col-100">
                      <input type="text" class="universal-input form-input"  :readonly="event.isReadOnly" :value="event.title" placeholder="Title" style="width:80% !important;">
                    </div>
                    <div class="full_width_td col-100">
                      <textarea class="universal-input form-input col-100"  :readonly="event.isReadOnly" style="height:80px; width:80% !important;" placeholder="Event Description">{{ event.description }}</textarea>
                    </div>
                  </td>
                  <td class="col-row" :class="{'editable-input': !event.isReadOnly, 'read-only-input': event.isReadOnly}">
                      <div class="full_width_td col-100">
                        <input type="text" class="universal-input form-input col-100"  :readonly="event.isReadOnly" :value="event.location" placeholder="Location" style="width:80% !important;">
                      </div>
                      <div class="full_width_td col-100">
                        <input type="datetime-local" class="universal-input form-input col-100" :disabled="event.isReadOnly" :value="formatDateTime(event.time)" placeholder="Date & Time" style="width:80% !important;">
                      </div>
                      <div class="full_width_td col-100">
                        <input type="text" class="universal-input form-input col-100"  :readonly="event.isReadOnly" :value="event.link" placeholder="Meeting Link" style="width:80% !important;">
                      </div>
                  </td>
                  <td class="col-row" :class="{'editable-input': !event.isReadOnly, 'read-only-input': event.isReadOnly}">
                    <p><span class="status-indicator">{{ event.status }}</span></p>
                  </td>
                  <td class="col-row" :class="{'editable-input': !event.isReadOnly, 'read-only-input': event.isReadOnly}">
                    <RouterLink :to="{ name: 'Event Details', params: { id: event.id }}" :key="$route.fullPath"> 
                      <i class="fa-solid fa-eye front-blue"></i>
                    </RouterLink>
                    <i class="fa-solid fa-trash" @click="deleteEvent(event.id)"></i>
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
      events: [],
    };
  },
  components: {
    AdminResponse
  },
  methods: {
    closeResponse() {
      this.responseClass = '';
      this.dbResponse = '';
    },
    formatDateTime(dbTime) {
      if (!dbTime) return '';
      const date = new Date(dbTime);
      return date.toISOString().slice(0, 16);
    },
    async getEvents(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-events');
        const data = response.data;
        if (data.length > 0) {
          this.events = data.map(event => ({
            ...event,
            isReadOnly: true
          }));
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
    async deleteEvent(id){
      if(confirm('Deleting this event?') == false){
        return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/del-event', {
          id: id
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Deleted Successfully';
            this.getEvents();
          }else if(gotten_response == '2'){
            this.responseClass = 'my-red displayed';
            this.dbResponse =  "Failed";
          }
          
      }catch (error) {
          if (error.response) {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Failed. Server Offline. Please try again later.';
            if (error.response) {
              this.dbResponse = error.response;
            }
          }
      }
    },
  },
  mounted(){
    this.getEvents();
  }
}
</script>