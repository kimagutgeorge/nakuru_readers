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
            <p class="col-card-text">Quantity: {{ new Intl.NumberFormat().format(product.balance) }}</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue" @click="viewProduct(product.id)"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
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
import router from '@/router';

export default {
  name: 'AdminBooks',
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
    async viewProduct(id){
      const productId = id
      try {
        const response = await axios.post('http://127.0.0.1:5000/product-to-view', {
          product_id: productId
        });
        const data = response.data;
        if (data.length > 0) {
          //redirect
          router.push('/admin/product');
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
    this.getProducts();
  }
}
</script>