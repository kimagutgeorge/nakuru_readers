<template>
  <div class="app-wrapper">
    <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="home-wrapper col-100">
      <div class="home-top-bar">
        <div class="col-100 col-flex">
          <div class="col-80 col-flex">
            <router-link to="/profile" class="col-100 col-flex color-dark">
            <div class="col-10">
              <img src="../assets/860.jpg" class="home-logo">
            </div>
            <div class="col-90">
              <p>Welcome, <br>
              <span class="fw-bold">George</span></p>
            </div>
            <!-- end of profile -->
            </router-link>
          </div>
          <div class="col-20 col-flex">
            <i class="fa-solid fa-bell"></i>
            <i class="fa-solid fa-power-off"></i>
          </div>
        </div>
      </div>
      <div class="home-main-bar col-flex">
        <div class="col-33 text-center">
          <i class="fa-solid fa-envelope"></i>
        </div>
        <div class="col-33 text-center">
          <i class="fa-solid fa-shopping-cart"></i>
        </div>
        <div class="col-33 text-center">
          <i class="fa-solid fa-book-open-reader"></i>
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
import UserResponse from '@/components/UserResponse.vue';
import UserNavigation from '@/components/UserNavigation.vue';

export default {
  name: 'HomeView',
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
