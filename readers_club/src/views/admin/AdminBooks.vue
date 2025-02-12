<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Books</span></p>
      </div>
      <div class="col-100 admin-panel-body col-flex">
        <!-- card -->
          <div class="col-card col-20" v-for="(product, index) in products" :key="index">
            <img :src="product.image" alt="" class="col-card-img">
            <div class="col-card-body">
            <p hidden>{{ product.id }}</p>
            <h4 class="col-card-title">{{ product.name }}</h4>
            <p class="col-card-text">{{ new Intl.NumberFormat().format(product.price) }} KES</p>
            <p class="col-card-text" style="font-size:10px; color:red;"><span style="font-weight:bold">{{ new Intl.NumberFormat().format(product.balance) }}</span> left</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <RouterLink :to="{ name: 'Product Details', params: { id: product.id }}" :key="$route.fullPath"> 
                  <i class="fa-solid fa-eye front-blue"></i>
                  </RouterLink>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red" @click="deleteBook(product.id)"></i>
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
  name: 'Books',
  data() {
    return {
      responseClass: '',
      dbResponse: '',
      products: [],
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
    async getProducts(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-products');

        const data = response.data;

        if (data.length > 0) {
          this.products = data;
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
    this.getProducts();
  }
}
</script>