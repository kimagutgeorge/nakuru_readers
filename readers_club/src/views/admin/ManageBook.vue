<template>
    <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Categories</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Category</p>
                <div class="form-group">
                    <label class="title-label-small">Category Name</label>
                    <input type="text" v-model="category_name" class="universal-input form-input" placeholder="Money">
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="addCategory">SUBMIT</button>
                </div>
            </div>
            <div class="col-70">
                <!-- data table -->
                <DataTable
                :data="users"
                :columns="columns"
                :rows-per-page="5"
                :enable-search="true"
                :enable-pagination="true"
                />
                  <!-- end of data table -->
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import AdminResponse from '@/components/admin/AdminResponse.vue';
import DataTable from '@/components/admin/DataTable.vue';
export default {
  name: 'ManageBook',
  components: {
    AdminResponse, DataTable
  },
  data() {
    return {
        category_name: '',
        responseClass: '',
        dbResponse: '',
        //tables
        users: [
        { name: "Alice", age: 25, city: "New York" },
        { name: "Bob", age: 30, city: "Los Angeles" },
        { name: "Charlie", age: 35, city: "Chicago" },
        { name: "George", age: 26, city: "Kapsabet" },
        { name: "Kimagut", age: 26, city: "Eldama Ravine" },
        { name: "Matte", age: 21, city: "Nakuru" },
        { name: "Bomet", age: 21, city: "Ravine" },
      ],
      columns: [
        { label: "Name", key: "name" },
        { label: "Age", key: "age" },
        { label: "City", key: "city" },
      ],
    } 
  },
  methods: {
    async addCategory() {
        if (this.category_name === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-category', {
            name: this.category_name
            })
            const data = response.data
            //response
            this.responseClass = 'my-success displayed';
            this.dbResponse =  data.message
            this.category_name = ''
        }catch (error) {
            if (error.response) {
            console.log(error.response)
            }
        }
    },
    closeResponse() {
      this.responseClass = '';
      this.dbResponse = '';
    },
  }
}
</script>