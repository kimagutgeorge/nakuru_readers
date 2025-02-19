<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Groups</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Group</p>
                <div class="form-group">
                    <label class="title-label-small">Group Name</label>
                    <input type="text" v-model="group_name" class="universal-input form-input" placeholder="Rich Dad Forum">
                </div>
                <div class="form-group">
                    <label class="title-label-small">Group Description</label>
                    <textarea v-model="group_bio" class="universal-input form-input" placeholder="Discussion of this group">{{ group_bio }}</textarea>
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="editGroup">SAVE</button>
                </div>
            </div>
            <div class="col-70 table-container">
                <!-- group messages -->
                <div class="chat-box col-100 col-flex">

                </div>
                <!-- end of messages -->
            </div>
        </div>
    </div>
  </template>
  
  <script>
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  import axios from 'axios';
  
  export default {
    name: 'AdminViewGroup',
    props: ['id'],
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        group_name: '',
        group_bio: ''
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
      async getGroup(){
        try {
          const response = await axios.post('http://127.0.0.1:5000/get-group',{
            id: this.id
          });
  
          const data = response.data;
  
          if (data.length > 0) {
            const group = data[0]
            this.group_name = group.name
            this.group_bio = group.bio
          } else {
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Group not found';
            }
          } catch (error) {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Failed. Server Offline. Please try again later.';
            if (error.response) {
              this.dbResponse = error.response;
            }
          }
      },
      async editGroup() {
        if (this.group_name === '' || this.group_bio == '' || this.id == '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/edit-group', {
            name: this.group_name,
            bio: this.group_bio,
            id: this.id
            })
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Updated Successfully';
              
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Group Already Exists!';
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
      this.getGroup();
    }
  }
  </script>
  