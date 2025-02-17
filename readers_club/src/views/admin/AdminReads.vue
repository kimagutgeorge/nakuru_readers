<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Reads</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
          <!-- card -->
            <div class="col-card col-20" v-for="(read, index) in reads" :key="index">
              <img :src="read.image" alt="" class="col-card-img">
              <div class="col-card-body">
              <p hidden>{{ read.id }}</p>
              <h4 class="col-card-title">{{ read.name }}</h4>
              </div>
              <div class="col-card-controls col-flex col-100">
                <div class="col-30">
                  <RouterLink :to="{ name: 'Read Details', params: { id: read.id }}" :key="$route.fullPath"> 
                    <i class="fa-solid fa-eye front-blue"></i>
                    </RouterLink>
                </div>
                <div class="col-30">
                  <i class="fa-solid fa-download"></i>
                </div>
                <div class="col-30">
                  <i class="fa-solid fa-trash front-red" @click="deleteBook(read.id)"></i>
                </div>
              </div>
            </div>
            <!-- card -->
        </div>
    </div>
  </template>
  <script>
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  import axios from 'axios';
  
  export default {
    name: 'Reads',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        reads: [],
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
      async getReads(){
        try {
          const response = await axios.get('http://127.0.0.1:5000/get-reads');
  
          const data = response.data;
  
          if (data.length > 0) {
            this.reads = data;
          } else {
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'No products found!';
            }
          } catch (error) {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Failed. Server Offline. Please try again later.';
            if (error.response) {
              this.dbResponse = error.response;
            }
          }
      },
      async deleteBook(id){
        if(confirm("Delete this book?") == true){
          const book_id = id
        try {
              const response = await axios.post('http://127.0.0.1:5000/del-book', {
              id: book_id
              })
              const data = response.data
              //response
              const gotten_response = data.message
              if(gotten_response == '1'){
                this.responseClass = 'my-success displayed';
                this.dbResponse =  'Deleted Successfully';
                //clear form
                this.category_name = ''
                this.getProducts();
              }else{
                this.responseClass = 'my-red displayed';
                this.dbResponse =  "Failed";
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
        }
        
      }
    },
    mounted(){
      this.getReads();
    }
  }
  </script>