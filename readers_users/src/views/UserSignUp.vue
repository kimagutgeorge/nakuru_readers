<template>
    <div class="app-wrapper">
      <div class="sign-up-page">
        <div class="sign-up-page-inner">
          <!-- contents -->
            <div class="form-group col-100">
              <input type="email" class="universal-input form-input" placeholder="Username/Email">
            </div>
          <div class="form-group col-100">
            <input type="text" class="universal-input form-input" placeholder="First Name">
          </div>
          <div class="form-group col-100">
            <input type="text" class="universal-input form-input" placeholder="Last Name">
          </div>
          <div class="form-group col-100">
            <input type="password" class="universal-input form-input" placeholder="Create password">
          </div>
          <div class="form-group col-100">
            <input type="password" class="universal-input form-input" placeholder="Confirm password">
          </div>
          <div class="form-group col-100">
            <button class="btn-default col-100">Sign up</button>
          </div>
          <div class="form-group col-100 text-left">
            <p>Already have an account? <span class="fw-bold"><router-link to="/" class="default-color">Login
          </router-link></span></p>
          </div>
          <!-- end of contents -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'UserSignUp'
  }
  </script>