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
                <p style="margin-top:20px;">Group Chat</p>
                <!-- group messages -->
                <div class="chat-body col-100" @click.left="hideOptions" @contextmenu.prevent="handleRightClick">
                    <div class="full-chat-box col-100">
                    <div class="chat-box col-flex  user-sent" @click.right="showOptions">
                        <div class="chat-options" v-if="options">
                            <li><i class="fa-solid fa-close"></i> Delete</li>
                            <li><i class="fa-solid fa-reply"></i> Reply</li>
                        </div>
                        <div class="col-100" style="margin-bottom:7px;">
                            <span class="sm-font" style="font-weight:bold">Mtu Fulani</span>
                        </div>
                        <div class="col-90">
                            <p>This is the message that was sent by someone</p>
                        </div>
                        <div class="col-10 time">
                            <span class="sm-font">12:20</span>
                        </div>
                    </div>
                </div>
                    <!-- end of chat one -->
                <div class="full-chat-box col-100">
                    <div class="chat-box col-flex me-sent">
                        <div class="col-90">
                            <p>This is the message that was sent by me</p>
                        </div>
                        <div class="col-10 time">
                            <span class="sm-font">12:20</span>
                        </div>
                    </div>
                </div>
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
        group_bio: '',
        options: false
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
      showOptions(){
        this.options = true
      },
      hideOptions(){
        this.options = false
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
  