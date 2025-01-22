<template>
    <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
    <div class="admin-panel col-flex">
        <div class="col-100">
            <p><span  class="title-label">Add Books</span></p>
        </div>
        <div class="col-100 admin-panel-body col-flex">
         <div class="col-60 col-flex">
            <div class="col-50" style="margin-top:10px">
                <label>Book Name</label>
                <input type="text" class="universal-input form-input" v-model="bookName" placeholder="Book Name">
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Image</label>
                <input type="file" class="universal-input form-input" @change="onFileChange" accept="image/*" />
            </div>
            <div class="col-50" style="margin-top:10px">
              <label>Buying Price</label>
              <input type="number" class="universal-input form-input" v-model="buyingPrice" />
          </div>
            <div class="col-50" style="margin-top:10px">
              <label>Selling Price</label>
              <input type="number" class="universal-input form-input" v-model="sellingPrice" />
          </div>
          <div class="col-50" style="margin-top:10px">
            <label>Discount (%, Optional)</label>
            <input type="number" class="universal-input form-input" v-model="discount" />
        </div>
            <div class="col-50" style="margin-top:10px">
                <label>Genre</label>
                <select class="universal-input form-input" v-model="genre" placeholder="Select Genre">
                    <option  v-for="(category, index) in categories" :key="index"  :value="category.id">{{ category.name }}</option>
                </select>
            </div>
            <div class="col-50" style="margin-top:10px">
                <label>Collection</label>
                <select class="universal-input form-input" v-model="collection">
                    <option value="1">New Arrival</option>
                    <option value="2">Best Sellers</option>
                </select>
            </div>
            <div class="col-100" style="margin-top:10px">
                <label style="padding-bottom:10px;">Description</label>
                <textarea id="editor_content"></textarea>
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
    name: 'AdminBooks',
    data() {
      return {
        responseClass: '',
        dbResponse: '',
        categories: [],
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
      changeReadType() {
        if(this.bookType == '1'){
            this.isGroupRead = false
        }else{
            this.isGroupRead = true
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
        const editorContent = tinymce.get('editor_content').getContent()
        const genre = this.genre
        const bookName = this.bookName
        const productImage = this.productImage
        const collection = this.collection
        if(editorContent == '' || genre == '' || bookName == '' || productImage == ''){
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Please fill the required Fields'
            return
        }
        //set the form here
        const formData = new FormData()
        formData.append("description", editorContent)
        formData.append("genre", genre)
        formData.append("bookName", bookName)
        formData.append("productImage", productImage)
        formData.append("collection", collection)
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
              this.getCategories();
            }else if(gotten_response == '2'){
              this.responseClass = 'my-red displayed';
              this.dbResponse =  "Failed";
            }else{
              this.responseClass = 'my-red displayed';
              this.dbResponse = 'Book Already Exists!';
            }
            // clear form
            this.genre = ''
            this.bookName = ''
            this.productImage = ''
            this.collection = ''
            tinymce.activeEditor.setContent('');
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