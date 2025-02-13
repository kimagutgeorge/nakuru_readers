<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Add User</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-50 col-flex">
                <div style="margin-left:5%" class="col-80" v-if="imageUrl">
                    <p>Profile </p>
                    <img :src="imageUrl" alt="Selected" style="width:100px; height:100px;" />
                  </div>
                  <div class="col-50" style="margin-top:10px">
                    <label>First Name</label>
                    <input type="text" :readonly="!editable" class="universal-input form-input" v-model="fname" placeholder="First Name">
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Last Name</label>
                    <input type="text" :readonly="!editable" class="universal-input form-input" v-model="lname" placeholder="Last Name">
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Phone</label>
                    <input type="number" :readonly="!editable" class="universal-input form-input" v-model="phone" placeholder="Phone Number">
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Email</label>
                    <input type="email" :readonly="!editable" class="universal-input form-input" v-model="email" placeholder="Email">
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Profile Photo</label>
                    <input type="file" :disabled="!editable" class="universal-input form-input" @change="onFileChange" accept="image/*" />
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Preferred Genres</label>
                    <select class="universal-input form-input" :disabled="!editable" v-model="new_genre" @change="selectPrefferred">
                        <option :value="genreid">{{ genre }}</option>
                        <option  v-for="(category, index) in categories" :key="index"  :value="category.id">{{ category.name }}</option>
                    </select>
                </div>
                <div class="col-100 col-flex" style="margin-top:10px">
                    <div class="col-flex genre-list" v-for="(genre, index) in prefferred_genres" :key="index">
                        {{genre.name }}
                        <i class="fa-solid fa-close" @click="deleteGenre(genre.id)"></i>
                    </div>
                </div>
                <div class="col-50" style="margin-top:10px">
                    <label>Location</label>
                    <input type="text" :readonly="!editable" class="universal-input form-input" v-model="location" placeholder="Location">
                </div>
                <div class="col-100" style="margin-top:10px">
                    <label style="padding-bottom:10px;">User Bio</label>
                    <textarea :readonly="!editable" class="universal-input form-input" style="height:80px" placeholder="John Doe is a ..." v-model="bio"></textarea>
                </div>
                
                <div class="col-100" style="margin-top:10px">
                    <button class="btn btn-success btn-primary" @click="toggleEdit">
                        {{ editable ? 'SAVE' : 'EDIT' }} 
                        <i :class="editable ? 'fa-solid fa-save' : 'fa-solid fa-edit'"></i>
                    </button>
                </div>
             </div>
         <div class="col-50 col-flex">
            <!-- other details -->
         </div>
         <!-- en of form details -->
         
        </div>
    </div>
  </template>
  <script>
  import axios from 'axios';
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  
  export default {
    name: 'AdminViewUser',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        categories: [],
        prefferred_genres: [],
        fname: '',
        lname: '',
        phone: '',
        email: '',
        genre: '',
        location: '',
        bio: '',
        profileImage:'',
        imageUrl:'',
        editable: false,
        genreid:'',
        new_genre:''
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
      toggleEdit() {
        this.editable = !this.editable;
        this.InitEditor();
        //save data after edit
        if(this.editable == false){
        //   this.editUser();
        }
      },
      onFileChange(event) {
      const file = event.target.files[0]; // Get the selected file
      this.profileImage = file
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageUrl = e.target.result; // Set the image URL
        };
        reader.readAsDataURL(file); // Read the file as a data URL
      } else {
        this.imageUrl = null; // Clear the image if no file is selected
      }
    },
      selectPrefferred(){
        const currentGenre = document.getElementById("current_genre").value
        const selecTed = document.getElementById("current_genre");
        const selectedOption = selecTed.options[selecTed.selectedIndex].text
        if (!this.prefferred_genres.find(genre => genre.id === currentGenre)) {
            this.prefferred_genres.push({ "name": selectedOption, "id": currentGenre })
        }
      },
      deleteGenre(genreId) {
      this.prefferred_genres = this.prefferred_genres.filter(
        (genre) => genre.id !== genreId
      );
    },
      async getCategories(){
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-categories');

        const data = response.data;

        if (data.length > 0) {
          this.categories = data;
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
    async getUser(){
      try {
        const response = await axios.post('http://127.0.0.1:5000/get-user', {
          id:this.id
        });
        const data = response.data;
        if (data.length > 0) {
          const data = response.data;
          const user = data[0]
          // allocate values

        } else {
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Product Not Found!';
          }
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
    },
    },
    mounted() {
        this.getCategories();
    }
  }
  </script>