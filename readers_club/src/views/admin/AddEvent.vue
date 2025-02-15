<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Add Event</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
         <div class="col-60 col-flex">
            <div class="col-50" style="margin-top:10px">
                <label>Event Title</label>
                <input type="text" class="universal-input form-input" v-model="title" placeholder="Event Title">
            </div>
            <div class="col-100" style="margin-top:10px">
                <label style="padding-bottom:10px;">Description</label>
                <textarea class="universal-input form-input" style="height:80px" placeholder="Event Description" v-model="description"></textarea>
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Date and Time</label>
                <input type="datetime-local" class="universal-input form-input" v-model="date_time" placeholder="Last Name">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Location</label>
                <input type="text" class="universal-input form-input" v-model="location" placeholder="Physical location/virtual platform e.g zoom">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Meeting Link (Optional)</label>
                <input type="text" class="universal-input form-input" v-model="event_link" placeholder="Link to Virtual Meeting">
            </div>
            <div class="col-100" style="margin-top:10px">
                <button class="btn btn-success" @click="addEvent">SAVE <i class="fa-solid fa-save"></i></button>
            </div>
         </div>
        </div>
    </div>
  </template>
  <script>
  import axios from 'axios';
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  
  export default {
    name: 'AddEvent',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        title: '',
        description: '',
        date_time: '',
        location: '',
        event_link: '',
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
    async addEvent(){
        if(this.title == '' || this.description == '' || this.date_time == '' || this.location == ''){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        //set the form here
        const formData = new FormData()
        formData.append("title", this.title)
        formData.append("description", this.description)
        formData.append("date_time", this.date_time)
        formData.append("location", this.location)
        formData.append("event_link", this.event_link)
        //save info
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-event', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }});
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              // clear form
              this.title = ''
              this.description = ''
              this.date_time = ''
              this.location = ''
              this.event_link = ''

            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else if(gotten_response == '3'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Event Already Exists!';
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
        }
    }
  }
  </script>