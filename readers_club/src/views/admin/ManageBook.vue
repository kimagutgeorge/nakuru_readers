<template>
    <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Genres</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Genre</p>
                <div class="form-group">
                    <label class="title-label-small">Genre Name</label>
                    <input type="text" v-model="category_name" class="universal-input form-input" placeholder="Money">
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="addCategory">SUBMIT</button>
                </div>
            </div>
            <div class="col-70 table-container">
                <!-- data table -->
                <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
                  <thead>
                      <tr>
                          <th hidden>#</th>
                          <th style="width:70%;">Genre Name</th>
                          <th>Action</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(category, index) in categories" :key="index">
                          <td hidden>{{ category.id }}</td>
                          <td :class="{'editable-input': !category.isReadOnly, 'read-only-input': category.isReadOnly}"><input type="text" class="universal-input transaparent-input col-50" v-model="category.name" :readonly="category.isReadOnly"></td>
                          <td :class="{'editable-input': !category.isReadOnly, 'read-only-input': category.isReadOnly}">
                            <i 
                            :class="category.isReadOnly ? 'fa-solid fa-edit text-primary' : 'fa-solid fa-check text-success'"
                            @click="category.isReadOnly ? makeEditable(index) : saveCategory(category.id, category.name)"
                            ></i>
                            <i class="fa-solid fa-trash" @click="deleteCategory(category.id)"></i>
                          </td>
                      </tr>
                      </tbody>
                      </table>
                      <!-- end of table -->
                <!-- <DataTable
                :data="categories"
                :columns="columns"
                :rows-per-page="5"
                :enable-search="true"
                :enable-pagination="true"
                /> -->
                  <!-- end of data table -->
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import AdminResponse from '@/components/admin/AdminResponse.vue';
// import DataTable from '@/components/admin/DataTable.vue';
export default {
  name: 'ManageBook',
  components: {
    AdminResponse, //DataTable
  },
  data() {
    return {
        category_name: '',
        responseClass: '',
        dbResponse: '',
        categories: [],
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
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              //clear form
              this.category_name = ''
              this.getCategories();
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Genre Already Exists!';
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
    },
    closeResponse() {
      this.responseClass = '';
      this.dbResponse = '';
    },
    async getCategories(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-categories');

        const data = response.data;

        if (data.length > 0) {
          this.categories = data;
          this.categories = this.categories.map(category => ({
          ...category,
          isReadOnly:true
        }))
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No genres found!';
          }
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
    },
    makeEditable(index){
      this.categories[index].isReadOnly = false
    },
    async saveCategory(id, name){
      const catId = id
      const catName = name
      if (catName === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/save-category', {
          name: catName,
          id: catId
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Updated Successfully';
            this.getCategories();
          }else if(gotten_response == '2'){
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
    },
    async deleteCategory(id){
      if(confirm('Deleting this genre will delete all related books. Proceed?') == false){
        return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/del-category', {
          id: id
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Deleted Successfully';
            this.getCategories();
          }else if(gotten_response == '2'){
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
    },
  },
  mounted() {
    // new DataTable('#example');
    this.getCategories();
  }
}
</script>