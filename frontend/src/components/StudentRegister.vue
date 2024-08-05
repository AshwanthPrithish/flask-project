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
              v-model="confirmPassword"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': errors.confirmPassword.length }"
              id="confirm_password"
            />
            <div v-if="errors.confirmPassword.length" class="invalid-feedback">
              <span v-for="error in errors.confirmPassword" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Register</button>
          </div>
        </fieldset>
      </form>
  
      <div class="border-top pt-3">
        <small class="text-muted">Already Have an Account? <router-link to="/login">Sign In</router-link></small>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  import axios from 'axios';
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        errors: {
          username: [],
          email: [],
          password: [],
          confirmPassword: []
        },
        errorMessage: ''  // For general error messages
      };
    },
    computed: {
    ...mapState(['csrf'])
  },
    methods: {
      async submitForm() {
        this.errors = { username: [], email: [], password: [], confirmPassword: [] };
        this.errorMessage = '';  // Clear previous error message
        try {
          await axios.post('http://localhost:5000/register', {
            username: this.username,
            email: this.email,
            password: this.password,
            confirm_password: this.confirmPassword,
            csrf_token: this.csrf
          });
          this.$router.push({ name: 'login' }); // Redirect to login page
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
  