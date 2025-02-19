<template>
    <div class="app-wrapper">
      <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
      <div class="sign-up-page">
        <div class="sign-up-page-inner">
          <!-- contents -->
            <div class="form-group col-100">
              <input type="email" class="universal-input form-input" placeholder="Username/Email" v-model="email">
            </div>
          <div class="form-group col-100">
            <input type="text" class="universal-input form-input" placeholder="First Name" v-model="fname">
          </div>
          <div class="form-group col-100">
            <input type="text" class="universal-input form-input" placeholder="Last Name" v-model="lname">
          </div>
          <div class="form-group col-100">
            <input type="number" class="universal-input form-input" placeholder="Phone" v-model="phone">
          </div>
          <div class="form-group col-100">
            <input type="password" class="universal-input form-input" placeholder="Create password" v-model="password">
          </div>
          <div class="form-group col-100">
            <input type="password" class="universal-input form-input" placeholder="Confirm password" v-model="con_password">
          </div>
          <div class="form-group col-100">
            <button class="btn-default col-100" @click="signUp">Sign up</button>
          </div>
          <div class="form-group col-100">
            <p>Already have an account? <span class="fw-bold"><router-link to="/" class="default-color">Login
          </router-link></span></p>
          </div>
          <!-- end of contents -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import UserResponse from '@/components/UserResponse.vue';

  export default {
    name: 'UserSignUp',
    components: { 
      UserResponse
    },
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        fname: '',
        lname: '',
        email: '',
        password: '',
        con_password: '',
        phone: ''
      }
    },
    methods: {
      closeResponse() {
        this.responseClass = '';
        this.dbResponse = '';
      },
      async signUp(){
        if(this.fname == '' || this.lname == '' ||this.email == '' || this.password == '' || this.con_password == '' || this.phone == ''){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        if(this.password != this.con_password){
          this.responseClass = 'my-red displayed';
            this.dbResponse = 'Passwords do not match!'
          return
        }
        //set the form here
        const formData = new FormData()
        formData.append("fname", this.fname)
        formData.append("lname", this.lname)
        formData.append("email", this.email)
        formData.append("phone", this.phone)
        formData.append("password", this.password)
        //save info
        try {
            const response = await axios.post('http://127.0.0.1:5000/user-reg', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }});
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Registered Successfully';
              // clear form
              this.fname = ''
              this.lname = ''
              this.email = ''
              this.password = ''
              this.phone = ''
              this.con_password = ''

            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else if(gotten_response == '3'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'You are already a member, please login';
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'You are already a member, please login!';
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
    }
  }
  </script>