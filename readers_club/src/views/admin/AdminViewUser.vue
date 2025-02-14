<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">{{ fname }} {{ lname }}</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
            <div class="col-50 col-flex">
                <div class="col-50" v-if="imageUrl">
                    <p>Profile </p>
                    <img :src="imageUrl" alt="No Profile" style="width:60px; margin-top:10px;" />
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
                    <select class="universal-input form-input" :disabled="!editable" v-model="new_genre" id="current_genre" @change="selectPrefferred">
                        <option  v-for="(category, index) in categories" :key="index"  :value="category.id">{{ category.name }}</option>
                    </select>
                </div>
                <div class="col-100 col-flex" style="margin-top:10px">
                    <div class="col-flex genre-list" v-for="(genre, index) in prefferred_genres" :key="index">
                        {{genre.name }}
                        <i class="fa-solid fa-close" v-if="editable" @click="deleteGenre(genre.id)"></i>
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
          <div class="col-50" style="margin-top:10px;">
            <label>Verified</label>
            <input type="text" readonly class="universal-input form-input" v-model="is_verified" placeholder="Verified">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Active Status</label>
          <input type="text" class="universal-input form-input" v-model="is_active" readonly placeholder="Active Status">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Last Login</label>
          <input type="text" class="universal-input form-input" v-model="last_login" readonly placeholder="Last Login">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Last Active</label>
          <input type="text" class="universal-input form-input" v-model="last_active" readonly placeholder="Last Active">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Total Books Read</label>
          <input type="text" class="universal-input form-input" v-model="books" readonly placeholder="Books Read">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Role</label>
          <input type="text" class="universal-input form-input" v-model="role" readonly placeholder="Role">
        </div>
        <div class="col-50" style="margin-top:10px">
          <label>Unread Notifications</label>
          <input type="text" class="universal-input form-input" v-model="notifications" readonly placeholder="Unread Notifications">
        </div>
        <div class="col-100 col-flex" style="margin-top:10px">
          <label>Wishlist</label>
          <div class="col-flex genre-list" v-for="(single_book, index) in wishlist" :key="index">
              {{single_book.name }}
          </div>
        </div>
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
    props: ['id'],
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
        new_genre:'',
        reg:'',
        is_verified:'',
        is_active:'',
        last_login:'',
        last_active:'',
        books:'',
        role:'',
        notifications:'',
        preferred_genres:'',
        wishlist: []
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
        // this.InitEditor();
        //save data after edit
        if(this.editable == false){
          this.editUser();
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
          //allocate values
          this.fname = data.f_name
          this.lname = data.l_name
          this.phone = data.phone
          this.email = data.email
          this.location = data.location
          this.bio = data.bio
          this.imageUrl = data.photo
          this.prefferred_genres = data.preferred_genres
          this.reg = data.reg
          this.is_verified = data.is_verified
          this.is_active = data.is_active
          this.last_login = data.last_login
          this.last_active = data.last_active
          this.books = data.books
          this.role = data.role
          this.notifications = data.notifications
          this.preferred_genres = data.preferred_genres
          this.wishlist = data.wishlist
        } catch (error) {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Failed. Server Offline. Please try again later.';
          if (error.response) {
            this.dbResponse = error.response;
          }
        }
    },
    async editUser(){
        if(this.fname == '' || this.lname == '' || this.phone == '' || this.email == '' || this.location == ''){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        //set the form here
        const formData = new FormData()
        formData.append("user_id", this.id)
        formData.append("fname", this.fname)
        formData.append("lname", this.lname)
        formData.append("phone", this.phone)
        formData.append("email", this.email)
        formData.append("location", this.location)
        formData.append("bio", this.bio)
        formData.append("productImage", this.profileImage)
        this.prefferred_genres.forEach(function(genre){
            const single_genre = genre.id
            formData.append("genres[]", single_genre)
        })
        //save info
        try {
            const response = await axios.post('http://127.0.0.1:5000/edit-user', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }});
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Added Successfully';
              // clear form

            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else if(gotten_response == '3'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'User Already Exists!';
            }else if(gotten_response == '4'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Failed. Only jpeg, jpg, png';
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Already Exists!';
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
    },
    mounted() {
        this.getCategories();
        this.getUser();
    }
  }
  </script>