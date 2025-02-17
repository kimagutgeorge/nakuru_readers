<template>
  <!-- <AdminResponse :class="['response-message', responseClass]" :dbResponse="dbResponse"/> -->
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Manage </span> <span class="title-label-small"><i class="fa-solid fa-angle-right"></i>Rules & Guidelines</span></p>
      </div>
      <div class="col-100 admin-panel-body col-flex">
          <div class="col-50">
              <div class="form-group">
                  <label class="title-label-small">Guideline Title</label>
                  <input type="number" v-model="rule_id" hidden>
                  <input type="text" v-model="title" class="universal-input form-input" placeholder="Guideline">
              </div>
              <div class="form-group">
                <label class="title-label-small" style="padding-bottom:10px;">Guideline</label>
                <textarea id="editor_content"></textarea>
            </div>
              <div class="form-group col-flex">
                  <button class="btn btn-success" @click="addGuideline">SUBMIT</button>
                  <button class="btn btn-cancel" @click="cancelEdit" v-if="cancel">CANCEL</button>
              </div>
          </div>
          <div class="col-50 table-container">
              <!-- data table -->
              <table style="width:90%; margin-left:5%;" class="my-tbl" cellspacing="0">
                <thead>
                    <tr>
                        <th hidden>#</th>
                        <th style="width:70%;">Guideline</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(rule, index) in rules" :key="index">
                        <td hidden>{{ rule.id }}</td>
                        <td>
                          <p class="title-label-small">{{ rule.title }}</p>
                          <div class="col-100" v-if="rule.isvisible" v-html="rule.description"></div>
                        </td>
                        <td>
                          <i class="fa-solid fa-angle-down" v-if="!rule.isvisible" @click="viewRule(index)"></i>
                          <i class="fa-solid fa-angle-up" v-if="rule.isvisible" @click="hideRule(index)"></i>
                          <i class="fa-solid fa-edit" @click="toEdit(rule.id, rule.title, rule.description)"></i>
                          <i class="fa-solid fa-trash" @click="deleteRule(rule.id)"></i>
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
export default {
name: 'Guidelines',
components: {
  AdminResponse, //DataTable
},
data() {
  return {
      title: '',
      description:'',
      responseClass: '',
      rule_id:'',
      dbResponse: '',
      rules: [],
      cancel:false
  } 
},
methods: {
  viewRule(index){
    this.rules[index].isvisible = true
  },
  hideRule(index){
    this.rules[index].isvisible = false
  },
  toEdit(id, title, description){
    this.rule_id = id
    this.title = title
    tinymce.get('editor_content').setContent(description);
    this.cancel = true
  },
  cancelEdit(){
    this.cancel = false
    this.rule_id = ''
    this.title = ''
    tinymce.get('editor_content').setContent('');
  },
  async addGuideline() {
      const editorContent = tinymce.activeEditor.getContent()
      const formData = new FormData();
      formData.append("title", this.title)
      formData.append("description", editorContent)
      formData.append("id", this.rule_id)
      
      if (this.title === '' || editorContent == '') {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'Please fill the required Fields'
          return
      }
      try {
          const response = await axios.post('http://127.0.0.1:5000/add-rule', formData)
          const data = response.data
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Added Successfully';
            //clear form
            this.title = ''
            tinymce.get('editor_content').setContent('');
            this.getRules();
          }else if(gotten_response == '2'){
            this.responseClass = 'my-red displayed';
            this.dbResponse =  "Failed";
          }else{
            this.responseClass = 'my-red displayed';
            this.dbResponse = 'Guideline Already Exists!';
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
  async getRules(){
    try {
      const response = await axios.get('http://127.0.0.1:5000/get-rules');

      const data = response.data;

      if (data.length > 0) {
        this.rules = data;
        this.rules = this.rules.map(rule => ({
          ...rule,
          isvisible: false
        }))
      } else {
          this.responseClass = 'my-red displayed';
          this.dbResponse = 'No rules & guidelines found!';
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
  async deleteRule(id){
    if(confirm('Deleting this guideline?') == false){
        return
      }
    try {
      const response = await axios.post('http://127.0.0.1:5000/del-rule', {
        rule_id: id
      });

          const data = response.data;
          //response
          const gotten_response = data.message
          if(gotten_response == '1'){
            this.responseClass = 'my-success displayed';
            this.dbResponse =  'Deleted Successfully';
            //clear form
            this.getRules();
          }else if(gotten_response == '2'){
            this.responseClass = 'my-red displayed';
            this.dbResponse =  "Failed";
          }
      } catch (error) {
        this.responseClass = 'my-red displayed';
        this.dbResponse = 'Failed. Server Offline. Please try again later.';
        if (error.response) {
          this.dbResponse = error.response;
        }
      }
  }
},
mounted() {
  // new DataTable('#example');
  this.getRules();
  this.InitEditor();
}
}
</script>