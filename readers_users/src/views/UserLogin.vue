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
          <input type="password" class="universal-input form-input" placeholder="Confirm password" v-model="password">
        </div>
        <div class="form-group col-100">
          <button class="btn-default col-100" @click="login">Login</button>
        </div>
        <div class="form-group col-100">
          <p>Don't have an account? <span class="fw-bold"><router-link to="/signup" class="default-color">Sign Up
        </router-link></span></p>
        </div>
        <!-- end of contents -->
      </div>
    </div>
  </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useUserStore } from '@/assets/js/userStore.js'
  import UserResponse from '@/components/UserResponse.vue';

export default {
  name: 'UserLogin',
  components: { UserResponse },
  data() {
    return {
      responseClass: '',
      dbResponse: '',
      email: '',
      password: ''
    };
  },
  setup() {
    const userStore = useUserStore(); // Access Pinia store
    return { userStore };
  },
  methods: {
    closeResponse() {
      this.responseClass = '';
      this.dbResponse = '';
    },
    async login() {
      if (this.email === '' || this.password === '') {
        this.responseClass = 'my-red displayed';
        this.dbResponse = 'Please fill the required Fields';
        return;
      }

      try {
        const response = await axios.post('http://192.168.1.125:5000/login', {
          email: this.email,
          password: this.password
        });
        const data = response.data;
        const gotten_response = data.message;

        if (gotten_response === '1') {
          this.responseClass = 'my-success displayed';
          this.dbResponse = 'Login Successful';

          this.userStore.setUser(data.user); // Store user in Pinia
          
          setTimeout(() => {
            this.$router.push('/home');
          }, 1500);

          this.email = '';
          this.password = '';
        } else if (gotten_response === '2') {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Invalid credentials';
        } else {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Error Signing in';
        }
      } catch (error) {
        console.log(error)
        this.responseClass = 'my-red displayed';
        this.dbResponse = 'Failed. Server Offline. Please try again later.';
      }
    }
  }
};
  </script>