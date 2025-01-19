<template>
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
                <!-- insert data here -->
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'ManageBook',
  data () {
    return {
        category_name: ''
    } 
  },
  methods: {
    async addCategory() {
        try {
            const response = await axios.post('http://127.0.0.1:5000/addcat', {
            name: this.category_name
            })

            const data = response.data
            console.log(data)
        }catch (error) {
            if (error.response) {
            console.log(error.response)
            }
        }
    }
  }
}
</script>