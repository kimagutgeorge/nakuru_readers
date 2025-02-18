<template>
  <div class="app-wrapper">
    <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="home-wrapper col-100">
      <div class="home-top-bar">
        <div class="col-100 col-flex">
          <div class="col-80 col-flex">
            <div class="col-10">
              <img src="../assets/860.jpg" class="home-logo">
            </div>
            <div class="col-90">
              <p>Welcome, <br>
              <span class="fw-bold">George</span></p>
            </div>
          </div>
          <div class="col-20">
            <i class="fa-solid fa-bell"></i>
          </div>
        </div>
      </div>
      <div class="home-main-bar col-flex">
        <div class="col-30 text-center">
          <i class="fa-solid fa-envelope"></i>
        </div>
        <div class="col-30 text-center">
          <i class="fa-solid fa-shopping-cart"></i>
        </div>
        <div class="col-30 text-center">
          <i class="fa-solid fa-book-open-reader"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserResponse from '@/components/UserResponse.vue';

export default {
  name: 'HomeView',
  components: { UserResponse },
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
