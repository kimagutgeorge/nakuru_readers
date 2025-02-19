<template>
    <div class="app-wrapper">
      <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
      <div class="home-wrapper col-100">
        <div class="col-100 title-bar col-flex">
            <div class="col-100">
                <p class="title-text"><i class="fa-solid fa-envelope"> </i>Messages</p>
            </div>
            <div class="col-100">
                <input type="text" class="universal-input form-input" style="width:93% !important;" placeholder="Search user" v-model="password">
            </div>
        </div>
        <div class="chat-body">
            <div class="chat-box col-flex">
                <div class="col-20">
                    <img src="../assets/860.jpg" class="read-pic"> 
                </div>
                <div class="col-67">
                    Lorem ipsum dolor...
                </div>
                <div class="col-10 text-center">
                    <p class="sm-time">12:10</p>
                    <div class="not-dot">
                        <div class="not-dot-inner">
                            2
                        </div>
                    </div>
                </div>
            </div>
            <div class="chat-box col-flex">
                <div class="col-20">
                    <img src="../assets/g10.png" class="read-pic"> 
                </div>
                <div class="col-67">
                    Lorem ipsum dolor...
                </div>
                <div class="col-10">
                    <p class="sm-font">12:10</p>
                </div>
            </div>
        </div>
      </div>
      <!-- end of message -->
       <UserNavigation/>
    </div>
  </template>
  
  <script>
  import UserResponse from '@/components/UserResponse.vue';
  import UserNavigation from '@/components/UserNavigation.vue';
  
  export default {
    name: 'UserReads',
    components: { UserResponse, UserNavigation },
    data() {
        return {
          responseClass: '',
          dbResponse: '',
          email: '',
          password: '',
        }
      },
      methods: {
        closeResponse() {
          this.responseClass = '';
          this.dbResponse = '';
        },
      }
  }
  </script>
  