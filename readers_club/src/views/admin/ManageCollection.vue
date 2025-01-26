<template>
    <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Collections</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Collection</p>
                <div class="form-group">
                    <label class="title-label-small">Collection Name</label>
                    <input type="text" v-model="collection_name" class="universal-input form-input" placeholder="Best Seller">
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="addCollection">SUBMIT</button>
                </div>
            </div>
            <div class="col-70 table-container">
                <!-- data table -->
                <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
                  <thead>
                      <tr>
                          <th hidden>#</th>
                          <th style="width:70%;">Collection Name</th>
                          <th>Action</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(collection, index) in collections" :key="index">
                          <td hidden>{{ collection.id }}</td>
                          <td :class="{'editable-input': !collection.isReadOnly, 'read-only-input': collection.isReadOnly}"><input type="text" class="universal-input transaparent-input col-50" v-model="collection.name" :readonly="collection.isReadOnly"></td>
                          <td :class="{'editable-input': !collection.isReadOnly, 'read-only-input': collection.isReadOnly}">
                            <i 
                            :class="collection.isReadOnly ? 'fa-solid fa-edit text-primary' : 'fa-solid fa-check text-success'"
                            @click="collection.isReadOnly ? makeEditable(index) : saveCollection(collection.id, collection.name)"
                            ></i>
                            <i 
                            :class="collection.status === 1 ? 'fa-solid fa-toggle-on text-success' : 'fa-solid fa-toggle-off text-danger'" 
                            @click="toggleStatus(collection)"
                            ></i>
                            <i class="fa-solid fa-trash" @click="deleteCollection(collection.id)"></i>
                          </td>
                      </tr>
                      </tbody>
                      </table>
                      <!-- end of table -->
                <!-- <DataTable
                :data="collections"
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
        collection_name: '',
        responseClass: '',
        dbResponse: '',
        collections: [],
    } 
  },
  methods: {
    toggleStatus(collection) {
    // Toggle the status between 0 and 1
    collection.status = collection.status === 1 ? 0 : 1;

    // Optionally, save the status change to the server
    this.saveCollectionStatus(collection.id, collection.status);
  },
  async saveCollectionStatus(id, status){
      try {
          const response = await axios.post('http://127.0.0.1:5000/status-collection', {
          collection_id: id,
          collection_status: status
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Updated Successfully';
            this.getCollections();
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
    async addCollection() {
        if (this.collection_name === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-collection', {
            name: this.collection_name
            })
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              //clear form
              this.collection_name = ''
              this.getCollections();
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Collection Already Exists!';
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
    async getCollections(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-collections');

        const data = response.data;

        if (data.length > 0) {
          this.collections = data;
          this.collections = this.collections.map(collection => ({
          ...collection,
          isReadOnly:true
        }))
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No Collections found!';
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
      this.collections[index].isReadOnly = false
    },
    async saveCollection(id, name){
      const collectionId = id
      const collectionName = name
      if (collectionName === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/save-collection', {
          name: collectionName,
          id: collectionId
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Updated Successfully';
            this.getCollections();
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
    async deleteCollection(id){
      if(confirm('Deleting this Collection will delete all related books. Proceed?') == false){
        return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/del-collection', {
          id: id
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Deleted Successfully';
            this.getCollections();
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
    this.getCollections();
  }
}
</script>