<template>
    <div class="app-wrapper">
        <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
        <div class="home-wrapper col-100">
            <div class="col-100 title-bar col-flex">
                <div class="col-100">
                    <p class="title-text"><i class="fa-solid fa-bars"></i>CATEGORIES</p>
                </div>
            </div>
            <!-- page -->
            <div class="chat-body col-flex no-pad">
                <div class="col-100 fit-height col-flex-fixed search-bar">
                    <input type="text" class="universal-input form-input"><button class="btn-default"><i class="fa-solid fa-search"></i></button>
                </div>
                <div class="col-100">
                    <div class="col-50-r">
                        <select name="" id="" class="universal-input form-input col-100">
                            <option value="">Search By</option>
                            <option value="">Complete</option>
                            <option value="">Pending</option>
                        </select>
                    </div>
                </div>
                <div class="col-100 shop-body col-flex default-bg">
                    <div class="col-50 product-card white-bg" v-for="(read, index) in reads" :key="index">
                        <div class="col-100 ">
                            <RouterLink :to="{ name: 'Read Details', params: { id: read.id }}" :key="$route.fullPath"> 
                            <img :src="read.image" alt="Loading..." class="col-100">
                            </RouterLink>
                            <div class="col-90">
                                <p class="c-grey">{{ read.name }}</p>
                            </div>
                            <div class="col-90">
                                <button class="btn-download col-100" @click="downloadBook(read.id)">
                                    DOWNLOAD
                                </button>
                            </div>
                        </div>
                    </div>
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
//   import { useUserStore } from '@/assets/js/userStore.js'
//   import { ref, onMounted, onUnmounted } from 'vue';
  
  export default {
    name: 'UserReads',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        reads: [],
      }
    },
    components: {
      UserResponse, UserNavigation
    },
    methods: {
      closeResponse() {
        this.responseClass = '';
        this.dbResponse = '';
      },
      async getReads(){
        try {
          const response = await axios.get('http://192.168.1.125:5000/get-reads');
  
          const data = response.data;
  
          if (data.length > 0) {
            this.reads = data;
          } else {
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'No books found!';
            }
          } catch (error) {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Failed. Server Offline. Please try again later.';
            if (error.response) {
              this.dbResponse = error.response;
            }
          }
      },
      async downloadBook(id) {
        try {
            // Send the book ID to Flask
            const response = await axios.post('http://192.168.1.125:5000/download-book', {
                book_id: id
            });

            // Check if the response contains a download link
            if (response.data.download_link) {
                // Trigger the download
                window.location.href = response.data.download_link;
            } else {
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'No download link received from the server.';
            }
        } catch (error) {
            console.error("Error downloading the book:", error);
        }
    }
      
    },
    mounted(){
      this.getReads();
    }
  }
  </script>