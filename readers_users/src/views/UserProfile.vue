<template>
    <div class="app-wrapper">
      <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
      <div class="sign-up-page" style="padding-top:0px;">
        <div class="sign-up-page-inner">
          <!-- contents -->
           <div class="form-group col-100 text-center">
            <img src="../assets/860.jpg" class="profile-pic">
           </div>
            <div class="form-group col-100 col-flex">
                <div class="col-50">
                    <input type="email" class="universal-input form-input" placeholder="First Name" v-model="fname">
                </div>
                <div class="col-50">
                    <input type="text" class="universal-input form-input" placeholder="Last Name" v-model="lname">
                </div>
            </div>
          <div class="form-group col-100 col-flex">
            <div class="col-50">
                <input type="email" class="universal-input form-input" placeholder="Username/Email" v-model="email">
            </div>
            <div class="col-50">
                <input type="number" class="universal-input form-input" placeholder="Phone" v-model="phone">
            </div>
          </div>
          <div class="form-group col-100">
            <label class="sm-font light-dark">Preffered Genres</label>
            <select class="universal-input form-input" v-model="new_genre" id="current_genre" @change="selectPrefferred" style="background-color:#ffffff;">
                <option  v-for="(category, index) in categories" :key="index"  :value="category.id">{{ category.name }}</option>
            </select>
          </div>
          <div class="form-group col-100 col-flex">
            <!-- preffered genres -->
            <div class="col-flex genre-list" v-for="(genre, index) in prefferred_genres" :key="index">
                {{genre.name }}
            <i class="fa-solid fa-close"  @click="deleteGenre(genre.id)"></i>
            </div>
          </div>
          <div class="form-group col-100">
            <input type="text" class="universal-input form-input" placeholder="Location" v-model="password">
          </div>
          <div class="form-group col-100">
            <textarea class="universal-input form-input" placeholder="Bio" v-model="bio" style="height:50px;"></textarea>
          </div>
          <div class="form-group col-100">
            <button class="btn-default col-100" @click="signUp">Save</button>
          </div>
          <!-- end of contents -->
        </div>
      </div>
      <!-- Navbar -->
      <UserNavigation/>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import UserResponse from '@/components/UserResponse.vue';
  import UserNavigation from '@/components/UserNavigation.vue';

  export default {
    name: 'UserProfile',
    components: { 
      UserResponse, UserNavigation
    },
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        prefferred_genres: [],
        categories: [],
        fname: '',
        lname: '',
        email: '',
        password: '',
        con_password: '',
        phone: '',
        new_genre: ''
      }
    },
    methods: {
      closeResponse() {
        this.responseClass = '';
        this.dbResponse = '';
      },
      deleteGenre(genreId) {
      this.prefferred_genres = this.prefferred_genres.filter(
        (genre) => genre.id !== genreId
      );
        },
      selectPrefferred(){
        const currentGenre = document.getElementById("current_genre").value
        const selecTed = document.getElementById("current_genre");
        const selectedOption = selecTed.options[selecTed.selectedIndex].text
        if (!this.prefferred_genres.find(genre => genre.id === currentGenre)) {
            this.prefferred_genres.push({ "name": selectedOption, "id": currentGenre })
        }
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
      async signUp(){
        if(this.fname == '' || this.lname == '' ||this.email == '' || this.password == '' || this.con_password == '' || this.phone == ''){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        if(this.password != this.con_password){
          this.responseClass = 'my-red displayed';
            this.dbResponse = 'Passwords do not match!'
          return
        }
        //set the form here
        const formData = new FormData()
        formData.append("fname", this.fname)
        formData.append("lname", this.lname)
        formData.append("email", this.email)
        formData.append("phone", this.phone)
        formData.append("password", this.password)
        //save info
        try {
            const response = await axios.post('http://127.0.0.1:5000/user-reg', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }});
            const data = response.data
            //response
            const gotten_response = data.message
            if(gotten_response == '1'){
              this.responseClass = 'my-success displayed';
              this.dbResponse =  'Registered Successfully';
              // clear form
              this.fname = ''
              this.lname = ''
              this.email = ''
              this.password = ''
              this.phone = ''
              this.con_password = ''

            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else if(gotten_response == '3'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'You are already a member, please login';
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'You are already a member, please login!';
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
    mounted(){
        this.getCategories();
    }
  }
  </script>