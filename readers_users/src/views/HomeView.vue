<template>
  <div class="app-wrapper">
    <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="home-wrapper col-100">
      <div class="home-top-bar">
        <div class="col-100 col-flex">
          <div class="col-80 col-flex ">
            <router-link to="/profile" class="col-100 col-flex-fixed color-dark">
            <!-- <RouterLink :to="{ name: 'Profile', params: { id: product.id }}" :key="$route.fullPath">  -->
            <div class="col-10">
              <img :src="pic" class="home-logo">
            </div>
            <div class="col-90">
              <p>Welcome, <br>
              <span class="fw-bold">{{ fname }}</span></p>
            </div>
            <!-- end of profile -->
          <!-- </RouterLink> -->
        </router-link>
          </div>
          <div class="col-20 col-flex" style="flex-wrap:nowrap;">
            <i class="fa-solid fa-bell"></i>
            <router-link to="/" class="col-100 col-flex color-dark">
            <i class="fa-solid fa-power-off"></i>
          </router-link>
          </div>
        </div>
      </div>
      <div class="home-main-bar col-flex">
        <div class="col-33 text-center">
          <router-link to="/messages">
            <i class="fa-solid fa-envelope"></i>
          </router-link>
        </div>
        <div class="col-33 text-center">
          <i class="fa-solid fa-shopping-cart"></i>
        </div>
        <div class="col-33 text-center">
          <router-link to="/reads">
            <i class="fa-solid fa-book-open-reader"></i>
          </router-link>
        </div>
      </div>
      <!-- quick actions -->
      <div class="home-main-actions col-flex">
        <div class="col-100">
          <p>Quick Actions</p>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-list"></i>
            <p>Books</p>
          </div>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-star text-center"></i>
            <p>Favourites</p>
          </div>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-calendar text-center"></i>
            <p>Events</p>
          </div>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-envelope text-center"></i>
            <p>Messages</p>
          </div>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-store text-center"></i>
            <p>Store</p>
          </div>
        </div>
        <div class="col-33 text-center">
          <div class="col-40 text-center">
            <i class="fa-solid fa-list text-center"></i>
            <p>Orders</p>
          </div>
        </div>
      </div>
      <!-- end of quick actions -->
      <div class="home-main-actions col-flex">
        <div class="col-100">
          <p>Latest Messages</p>
        </div>
        <div class="col-100 msg-box">
          <p class="fw-bold">Mtu Fulani</p>
          <p>Hii ndo message ametuma</p>
          <span class="fw-bold">02/08 20:46</span>
        </div>
        <div class="col-100 msg-box">
          <p class="fw-bold">Mtu Fulani</p>
          <p>Hii ndo message ametuma</p>
          <span class="fw-bold">02/08 20:46</span>
        </div>
        <div class="col-100 text-center">
          <span class="fw-bold default-color">See More</span>
        </div>
      </div>
    </div>
    <!-- end of message -->
     <UserNavigation/>
  </div>
</template>

<script>
import axios from 'axios';
import UserResponse from '@/components/UserResponse.vue';
import UserNavigation from '@/components/UserNavigation.vue';
import { useUserStore } from '@/assets/js/userStore.js'

export default {
  name: 'HomeView',
  components: { UserResponse, UserNavigation },
  data() {
      return {
        responseClass: '',
        dbResponse: '',
        email: '',
        password: '',
        fname: '',
        pic: ''
      }
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
      async getProfile(){
      try {
        const response = await axios.post('http://192.168.1.125:5000/get-profile', {
          id: this.userStore.user
        });

        const data = response.data;
        this.fname = data[0].f_name
        this.pic = data[0].photo

        if (data.length > 0) {
          this.categories = data;
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'User Not Found!';
          }
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
     },
    },
    mounted() {
      this.getProfile();
    }
}
</script>
