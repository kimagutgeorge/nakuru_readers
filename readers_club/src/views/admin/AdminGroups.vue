<template>
    <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Groups</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Group</p>
                <div class="form-group">
                    <label class="title-label-small">Group Name</label>
                    <input type="text" v-model="group_name" class="universal-input form-input" placeholder="Rich Dad Forum">
                </div>
                <div class="form-group">
                    <label class="title-label-small">Group Description</label>
                    <textarea v-model="group_bio" class="universal-input form-input" placeholder="Discussion of this group"></textarea>
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="addGroup">SUBMIT</button>
                </div>
            </div>
            <div class="col-70 table-container">
                <!-- data table -->
                <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
                  <thead>
                      <tr>
                          <th hidden>#</th>
                          <th style="width:60%;">Group Name</th>
                          <th style="width:20%;">Status</th>
                          <th>Action</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(group, index) in groups" :key="index">
                          <td hidden>{{ group.id }}</td>
                          <td :class="{'editable-input': !group.isReadOnly, 'read-only-input': group.isReadOnly}"><input type="text" class="universal-input transaparent-input col-50" v-model="group.name" :readonly="group.isReadOnly"></td>
                          <td><span  class="status-indicator">{{ group.status }} </span></td>
                          <td :class="{'editable-input': !group.isReadOnly, 'read-only-input': group.isReadOnly}">
                            <i 
                            :class="group.isReadOnly ? 'fa-solid fa-edit text-primary' : 'fa-solid fa-check text-success'"
                            @click="group.isReadOnly ? makeEditable(index) : savegroup(group.id, group.name)"
                            ></i>
                            <i 
                            :class="group.status === 'Active' ? 'fa-solid fa-toggle-on text-success' : 'fa-solid fa-toggle-off text-danger'" 
                            @click="toggleStatus(group)"
                            ></i>
                            <i class="fa-solid fa-trash" @click="deletegroup(group.id)"></i>
                          </td>
                      </tr>
                      </tbody>
                      </table>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import AdminResponse from '@/components/admin/AdminResponse.vue';
// import DataTable from '@/components/admin/DataTable.vue';
export default {
  name: 'ManageGroups',
  components: {
    AdminResponse, //DataTable
  },
  data() {
    return {
        group_name: '',
        group_description: '',
        responseClass: '',
        dbResponse: '',
        groups: [],
    } 
  },
  methods: {
    async addGroup() {
        if (this.group_name === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-group', {
            name: this.group_name,
            bio: this.group_description
            })
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              //clear form
              this.group_name = ''
              this.getgroups();
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Group Already Exists!';
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
    async getgroups(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-groups');

        const data = response.data;

        if (data.length > 0) {
          this.groups = data;
          this.groups = this.groups.map(group => ({
          ...group,
          isReadOnly:true
        }))
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No groups found!';
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
      this.groups[index].isReadOnly = false
    },
    toggleStatus(group) {
    // Toggle the status between 0 and 1
    group.status = group.status === 'Active' ? 'Inactive' : 'Active';

    // Optionally, save the status change to the server
    this.savegroupStatus(group.id, group.status);
  },
    async savegroup(id, name){
      const catId = id
      const catName = name
      if (catName === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/save-group', {
          name: catName,
          id: catId
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Updated Successfully';
            this.getgroups();
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
    async savegroupStatus(id, status){
      let new_status = status
      if(new_status == 'Active'){
        new_status == '1'
      }else if(new_status == 'Inactive'){
        new_status == '0'
      }
      alert(new_status)
      return
      try {
          const response = await axios.post('http://127.0.0.1:5000/status-group', {
          cat_id: id,
          cat_status: status
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Updated Successfully';
            this.getgroups();
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
    async deletegroup(id){
      if(confirm('Deleting this genre will delete all related books. Proceed?') == false){
        return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/del-group', {
          id: id
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Deleted Successfully';
            this.getgroups();
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
    this.getgroups();
  }
}
</script>