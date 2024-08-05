<template>
    <div class="container">
      <form @submit.prevent="submitForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Join Today</legend>
  
          <!-- Error Alert -->
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>
  
          <div class="form-group">
            <label for="username" class="form-control-label">Username</label>
            <input
              type="text"
              v-model="username"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.username.length }"
              id="username"
            />
            <div v-if="errors.username.length" class="invalid-feedback">
              <span v-for="error in errors.username" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label for="email" class="form-control-label">Email</label>
            <input
              type="email"
              v-model="email"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.email.length }"
              id="email"
            />
            <div v-if="errors.email.length" class="invalid-feedback">
              <span v-for="error in errors.email" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label for="admin_id" class="form-control-label">Admin ID</label>
            <input
              type="text"
              v-model="admin_id"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.admin_id.length }"
              id="admin_id"
            />
            <div v-if="errors.admin_id.length" class="invalid-feedback">
              <span v-for="error in errors.admin_id" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label for="password" class="form-control-label">Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.password.length }"
              id="password"
            />
            <div v-if="errors.password.length" class="invalid-feedback">
              <span v-for="error in errors.password" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label for="confirm_password" class="form-control-label">Confirm Password</label>
            <input
              type="password"
              v-model="confirm_password"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.confirm_password.length }"
              id="confirm_password"
            />
            <div v-if="errors.confirm_password.length" class="invalid-feedback">
              <span v-for="error in errors.confirm_password" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Register</button>
          </div>
        </fieldset>
      </form>
  
      <div class="border-top pt-3">
        <small class="text-muted">Already Have an Account? <router-link to="/sp-login">Sign In</router-link></small>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import store from '@/store';
  const csrfToken = store.state.csrf;
  
  export default {
    data() {
      return {
        username: '',
        email: '',
        admin_id: '',
        password: '',
        confirm_password: '',
        errors: {
          username: [],
          email: [],
          admin_id: [],
          password: [],
          confirm_password: []
        },
        errorMessage: ''  // For general error messages
      };
    },
    methods: {
      async submitForm() {
        this.errors = { username: [], email: [], admin_id: [], password: [], confirm_password: [] };
        this.errorMessage = '';  // Clear previous error message
        try {
            await axios.post('http://localhost:5000/sp-register', {
            username: this.username,
            email: this.email,
            admin_id: this.admin_id,
            password: this.password,
            confirm_password: this.confirm_password,
            csrf: csrfToken
          });
          this.$router.push({ name: 'sp-login' }); // Redirect to login page
        } catch (error) {
          if (error.response && error.response.data.errors) {
            this.errors = error.response.data.errors;
          }
          if (error.response && error.response.data.message) {
            this.errorMessage = error.response.data.message;
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 20px;
  }
  .is-invalid {
    border-color: red;
  }
  .invalid-feedback {
    color: red;
  }
  .alert {
    margin-top: 20px;
  }
  </style>
  