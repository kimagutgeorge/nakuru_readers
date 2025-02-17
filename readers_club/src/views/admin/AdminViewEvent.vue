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
                <input type="text" class="universal-input form-input" :readonly="!editable" v-model="title" placeholder="Event Title">
            </div>
            <div class="col-100" style="margin-top:10px">
                <label style="padding-bottom:10px;">Description</label>
                <textarea class="universal-input form-input" style="height:80px" :readonly="!editable" placeholder="Event Description" v-model="description"></textarea>
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Date and Time</label>
                <input type="datetime-local" class="universal-input form-input" :readonly="!editable" v-model="date_time" placeholder="Last Name">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Location</label>
                <input type="text" class="universal-input form-input" :readonly="!editable" v-model="location" placeholder="Physical location/virtual platform e.g zoom">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Meeting Link (Optional)</label>
                <input type="text" class="universal-input form-input" :readonly="!editable" v-model="event_link" placeholder="Link to Virtual Meeting">
            </div>
            <div class="col-100" style="margin-top:10px">
                <label>STATUS: {{ status }}</label>
                <div class="col-100 universal-input form-input" style="margin-top:10px">
                    <input type="radio" id="complete" v-model="new_status" value="1" :disabled="!editable">
                    <label for="html">Complete</label>
                </div>
                <div class="col-100 universal-input form-input" style="margin-top:10px">
                    <input type="radio" id="cancel" v-model="new_status" value="2" :disabled="!editable">
                    <label for="css">Cancel</label>
                </div>
                <div class="col-100 universal-input form-input" style="margin-top:10px">
                    <input type="radio" id="pending" v-model="new_status" value="0" :disabled="!editable">
                    <label for="javascript">Pending</label>
                </div>
            </div>
            <div class="col-100" style="margin-top:10px">
                <button class="btn btn-success btn-primary" @click="toggleEdit">
                    {{ editable ? 'SAVE' : 'EDIT' }} 
                    <i :class="editable ? 'fa-solid fa-save' : 'fa-solid fa-edit'"></i>
                </button>
            </div>
         </div>
         <div class="col-40 col-flex">
            <div class="col-100" style="margin-top:10px">
              <div class="col-50 col-flex" style="margin-top:10px">
                <label>Add Attendees</label>
                <select class="universal-input form-input" :disabled="!editable" v-if="editable" id="current_genre" @change="selectPrefferred">
                  <option  v-for="(user, index) in users" :key="index"  :value="user.id">{{ user.f_name }} {{ user.l_name }}</option>
              </select>
            </div>
              <div class="col-100 col-flex" style="margin-top:10px">
                <div class="col-flex genre-list" v-for="(genre, index) in prefferred_genres" :key="index">
                    {{genre.name }}
                    <i class="fa-solid fa-close" @click="deleteGenre(genre.id)"></i>
                </div>
                <!--  -->
                <div class="col-100 col-flex">
                  <div class="col-100">
                  <label >Attendees</label>
                  </div>
                <div class="col-flex genre-list" v-for="(attendee, index) in attendees" :key="index">
                  {{attendee.fname }} {{attendee.lname }}
              </div>
            </div>
            </div>
            </div>
         </div>
        </div>
    </div>
  </template>
  <script>
  import axios from 'axios';
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  
  export default {
    name: 'ViewEvent',
    props: ['id'],
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        editable: false,
        title: '',
        description: '',
        date_time: '',
        location: '',
        event_link: '',
        status: '',
        new_status:'',
        users: [],
        prefferred_genres:[],
        attendees:[]
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
      toggleEdit() {
        this.editable = !this.editable;
        //save data after edit
        if(this.editable == false){
          this.editEvent();
        }
        if(this.editable == true){
          this.getUsers();
        }
      },
      selectPrefferred(){
        const currentGenre = document.getElementById("current_genre").value
        const selecTed = document.getElementById("current_genre");
        const selectedOption = selecTed.options[selecTed.selectedIndex].text
        if (!this.prefferred_genres.find(genre => genre.id === currentGenre)) {
            this.prefferred_genres.push({ "name": selectedOption, "id": currentGenre })
        }
      },
      deleteGenre(genreId) {
      this.prefferred_genres = this.prefferred_genres.filter(
        (genre) => genre.id !== genreId
      );
    },
      async getEvent(){
      try {
        const response = await axios.post('http://127.0.0.1:5000/get-event',{
            event_id: this.id
        });

        const data = response.data;
        if (data.length > 0) {
          this.events = data;
          const event = this.events[0]
            this.title = event.title
            this.description = event.description
            this.location = event.location
            this.event_link = event.link
            this.status = event.status
            this.attendees = event.attendees
            // Convert "Tue, 25 Feb 2025 14:07:00 GMT" to "YYYY-MM-DDTHH:MM"
            const eventDate = new Date(event.time); // Convert string to Date object
            this.date_time = eventDate.toISOString().slice(0, 16); // Extract YYYY-MM-DDTHH:MM
          
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No event found!';
          }
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
        },
        async editEvent(){
            if(this.title == '' || this.description == '' || this.date_time == '' || this.location == ''){
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Please fill the required Fields'
                return
            }
            //set the form here
            const formData = new FormData()
            formData.append("id", this.id)
            formData.append("title", this.title)
            formData.append("description", this.description)
            formData.append("date_time", this.date_time)
            formData.append("location", this.location)
            formData.append("event_link", this.event_link)
            formData.append("status", this.new_status)
            this.prefferred_genres.forEach(function(genre){
            const single_genre = genre.id
            formData.append("attendees[]", single_genre)
        })
            //save info
            try {
                const response = await axios.post('http://127.0.0.1:5000/edit-event', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }});
                const data = response.data
                //response
                const gotten_response = data.message
                if(gotten_response == '1'){
                this.responseClass = 'my-success displayed';
                this.dbResponse =  'Updated Successfully';
                this.getEvent()

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
    mounted() {
        this.getEvent();
    }
  }
  </script>