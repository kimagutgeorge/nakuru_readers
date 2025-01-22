<template>
  <AdminResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
  <div class="admin-panel col-flex">
      <div class="col-100">
          <p><span  class="title-label">Books</span></p>
      </div>
      <div class="col-100 admin-panel-body col-flex">
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/logo.png" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/images/atomic.jpeg" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/logo.png" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/logo.png" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/logo.png" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
        <!-- card -->
          <div class="col-card col-20">
            <img src="../../assets/logo.png" alt="" class="col-card-img">
            <div class="col-card-body">
            <h4 class="col-card-title">This is the title</h4>
            <p class="col-card-text">This is a very small text about card</p>
            </div>
            <div class="col-card-controls col-flex col-100">
              <div class="col-30">
                <i class="fa-solid fa-eye front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-edit front-blue"></i>
              </div>
              <div class="col-30">
                <i class="fa-solid fa-trash front-red"></i>
              </div>
            </div>
          </div>
          <!-- card -->
      </div>
  </div>
</template>
<script>
import AdminResponse from '@/components/admin/AdminResponse.vue';

export default {
  name: 'AdminBooks',
  data() {
    return {
      responseClass: '',
      dbResponse: '',
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
  }
}
</script>