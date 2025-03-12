<template>
    <div class="app-wrapper">
        <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
        <div class="home-wrapper col-100">
            <div class="col-100 title-bar col-flex">
                <div class="col-100">
                    <p class="title-text"><i class="fa-solid fa-book-open"></i>{{name}}</p>
                </div>
            </div>
            <!-- page -->
            <div class="chat-body col-flex">
              <img :src="image" alt="Loading..." class="fixed-img">
              <div class="col-100 book-details">
                <h2 class="default-color-2">{{ name }}</h2>
                <p><span class="fw-bold">Genre:</span> {{ genre }}</p>
                <p><span class="fw-bold">Collection:</span> {{ collection }}</p>
              </div>
              <div class="col-100 book-details" v-html="description">
              </div>
              <div class="col-100">
                <button class="btn-download">DOWNLOAD</button>
              </div>
            </div>
        </div>
    </div>

<UserNavigation/>
</template>

<script>
import axios from 'axios';
import UserResponse from '@/components/UserResponse.vue';
import UserNavigation from '@/components/UserNavigation.vue';

  export default{
    name: 'UserReadsDetails',
    components: {
        UserResponse, UserNavigation
    },
    props: ["id"],
    data() {
        return{
            responseClass: '',
            dbResponse: '',
            name: '',
            image: '',
            genre: '',
            collection: '',
            description : '',
        }
    },
    methods: {
        closeResponse() {
        this.responseClass = '';
        this.dbResponse = '';
      },
      async getRead(){
        try {
          const response = await axios.post('http://192.168.1.125:5000/get-read',{
            id: this.id
          });
  
          const data = response.data;
  
          if (data.length > 0) {
            this.name = data[0].name
            this.image = data[0].image
            this.genre = data[0].genre
            this.collection = data[0].collection
            this.description = data[0].description
          } else {
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'No details found!';
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
    mounted(){
      this.getRead()
    }
  }
</script>