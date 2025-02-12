<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Add User</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
         <div class="col-60 col-flex">
            <div class="col-50" style="margin-top:10px">
                <label>First Name</label>
                <input type="text" class="universal-input form-input" v-model="fname" placeholder="First Name">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Last Name</label>
                <input type="text" class="universal-input form-input" v-model="lname" placeholder="Last Name">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Phone</label>
                <input type="number" class="universal-input form-input" v-model="phone" placeholder="Phone Number">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Email</label>
                <input type="email" class="universal-input form-input" v-model="email" placeholder="Email">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Profile Photo</label>
                <input type="file" class="universal-input form-input" @change="onFileChange" accept="image/*" />
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Preferred Genres</label>
                <select class="universal-input form-input" v-model="genre" id="current_genre" @change="selectPrefferred">
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
                <input type="email" class="universal-input form-input" v-model="email" placeholder="Location">
            </div>
            <div class="col-100" style="margin-top:10px">
                <label style="padding-bottom:10px;">User Bio</label>
                <textarea class="universal-input form-input" style="height:80px" placeholder="John Doe is a ..."></textarea>
            </div>
            
            <div class="col-100" style="margin-top:10px">
                <button class="btn btn-success" @click="addBook">SAVE <i class="fa-solid fa-save"></i></button>
            </div>
         </div>
         <!-- en of form details -->
         <div class="col-40">
            <div style="margin-left:5%" class="col-80" v-if="imageUrl">
                <p>Selected Image:</p>
                <img :src="imageUrl" alt="Selected" style="max-width: 100%; height: auto;margin-top:15px;" />
              </div>
         </div>
        </div>
    </div>
  </template>
  <script>
  import axios from 'axios';
  import AdminResponse from '@/components/admin/AdminResponse.vue';
  
  export default {
    name: 'AddUser',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        categories: [],
        prefferred_genres: [],
        genre: '',
        imageUrl: '',
        bookName: '',
        productImage: '',
        collection: '',
        sellingPrice: '',
        buyingPrice: '',
        quantity: '',
        discount: '',
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
    /* editor */
    InitEditor(){
    tinymce.init({
      selector: '#editor_content',
      plugins: [
          // Core editing features
          'anchor', 'autolink', 'charmap', 'codesample', 'emoticons', 'link', 'lists', 'searchreplace', 'table', 'visualblocks', 'wordcount',
          // Your account includes a free trial of TinyMCE premium features
        //   'checklist', 'mediaembed', 'casechange', 'export', 'formatpainter', 'pageembed', 'a11ychecker', 'tinymcespellchecker', 'permanentpen', 'powerpaste', 'advtable', 'advcode', 'editimage', 'advtemplate', 'ai', 'mentions', 'tinycomments', 'tableofcontents', 'footnotes', 'mergetags', 'autocorrect', 'typography', 'inlinecss', 'markdown',
          // Early access to document converters
        //   'importword', 'exportword', 'exportpdf'
      ],
      toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
      tinycomments_mode: 'embedded',
      tinycomments_author: 'Author name',
      mergetags_list: [
          { value: 'First.Name', title: 'First Name' },
          { value: 'Email', title: 'Email' },
      ],
      ai_request: (request, respondWith) => respondWith.string(() => Promise.reject('See docs to implement AI Assistant')),
      
      // Image upload configuration
      images_upload_handler: function (blobInfo, success, failure) {
        const formData = new FormData();
        formData.append('file', blobInfo.blob(), blobInfo.filename());

        fetch('app.php?action=edit-event', { // Replace with your server's upload endpoint
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result && result.location) {
                success(result.location);
            } else {
                failure('Upload failed: Invalid response from server.');
            }
        })
        .catch(error => {
            failure('Upload failed: ' + error.message);
        });
    },

    file_picker_callback: function (callback, value, meta) {
        if (meta.filetype === 'image') {
            const input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');

            input.onchange = function () {
                const file = this.files[0];
                const reader = new FileReader();

                reader.onload = function () {
                    callback(reader.result, { alt: file.name });
                };

                reader.readAsDataURL(file);
            };

            input.click();
        }
    }
  });
  },
  onFileChange(event) {
      const file = event.target.files[0]; // Get the selected file
      this.productImage = file
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
    uploadBook(event) {
      const file = event.target.files[0]; // Get the selected file
      this.book = file
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
    async addBook(){
        const editorContent = tinymce.activeEditor.getContent() // tinymce.post('editor_content').getContent()
        if(editorContent == '' || this.genre == '' || this.bookName == '' || this.productImage == '' || this.sellingPrice == '' || this.buyingPrice == '' || this.quantity == '' ){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        //set the form here
        const formData = new FormData()
        formData.append("description", editorContent)
        formData.append("genre", this.genre)
        formData.append("bookName", this.bookName)
        formData.append("productImage", this.productImage)
        formData.append("collection", this.collection)
        formData.append("sellingPrice", this.sellingPrice)
        formData.append("buyingPrice", this.buyingPrice)
        formData.append("quantity", this.quantity)
        formData.append("discount", this.discount)
        
        //save info
        try {
            const response = await axios.post('http://127.0.0.1:5000/add-book', formData, {
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
              this.genre = ''
              this.bookName = ''
              this.productImage = ''
              this.collection = ''
              tinymce.activeEditor.setContent('');
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else if(gotten_response == '3'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Failed. Error processing image';
            }else if(gotten_response == '4'){
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Failed. Only jpeg, jpg, png, gif!';
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
        this.InitEditor();
    }
  }
  </script>