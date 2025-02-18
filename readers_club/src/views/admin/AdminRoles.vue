<template>
    <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Manage</span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i> Roles</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-30">
                <p class="title-label">Add Role</p>
                <div class="form-group">
                    <label class="title-label-small">Role</label>
                    <input type="text" v-model="role_name" class="universal-input form-input" placeholder="Role">
                </div>
                <div class="form-group">
                    <button class="btn btn-success" @click="addRole">SUBMIT</button>
                </div>
            </div>
            <div class="col-70 table-container">
                <!-- data table -->
                <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
                  <thead>
                      <tr>
                          <th hidden>#</th>
                          <th style="width:70%;">Role</th>
                          <th>Action</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(role, index) in roles" :key="index">
                          <td hidden>{{ role.id }}</td>
                          <td :class="{'editable-input': !role.isReadOnly, 'read-only-input': role.isReadOnly}"><input type="text" class="universal-input transaparent-input col-50" v-model="role.name" :readonly="role.isReadOnly"></td>
                          <td :class="{'editable-input': !role.isReadOnly, 'read-only-input': role.isReadOnly}">
                            <i 
                            :class="role.isReadOnly ? 'fa-solid fa-edit text-primary' : 'fa-solid fa-check text-success'"
                            @click="role.isReadOnly ? makeEditable(index) : saverole(role.id, role.name)"
                            ></i>
                            <i class="fa-solid fa-trash" @click="deleterole(role.id)"></i>
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
  name: 'AdminRoles',
  components: {
    AdminResponse, //DataTable
  },
  data() {
    return {
        role_name: '',
        responseClass: '',
        dbResponse: '',
        roles: [],
    } 
  },
  methods: {
    async addRole() {
        if (this.role_name === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-role', {
            name: this.role_name
            })
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              //clear form
              this.role_name = ''
              this.getroles();
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Role Already Exists!';
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
    async getroles(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-roles');

        const data = response.data;

        if (data.length > 0) {
          this.roles = data;
          this.roles = this.roles.map(role => ({
          ...role,
          isReadOnly:true
        }))
        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'No roles found!';
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
      this.roles[index].isReadOnly = false
    },
    toggleStatus(role) {
    // Toggle the status between 0 and 1
    role.status = role.status === 1 ? 0 : 1;

    // Optionally, save the status change to the server
    this.saveroleStatus(role.id, role.status);
  },
    async saverole(id, name){
      const catId = id
      const catName = name
      if (catName === '') {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/save-role', {
          name: catName,
          id: catId
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Updated Successfully';
            this.getroles();
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
    async deleterole(id){
      if(confirm('Deleting this role will delete all related users. Proceed?') == false){
        return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/del-role', {
          id: id
          })
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse = 'Deleted Successfully';
            this.getroles();
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
    this.getroles();
  }
}
</script>