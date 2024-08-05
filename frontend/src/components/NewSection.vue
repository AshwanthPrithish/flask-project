<template>
    <div class="container">
      <form @submit.prevent="submitForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">{{ legend }}</legend>
  
          <div class="form-group">
            <label class="form-control-label">Title</label>
            <input 
              v-model="title" 
              type="text" 
              class="form-control form-control-lg" 
              :class="{'is-invalid': errors.title}" 
            />
            <div class="invalid-feedback" v-if="errors.title">
              <span v-for="error in errors.title" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label class="form-control-label">Date Created</label>
            <input 
              v-model="date_created" 
              type="date" 
              class="form-control form-control-lg" 
              :class="{'is-invalid': errors.date_created}" 
            />
            <div class="invalid-feedback" v-if="errors.date_created">
              <span v-for="error in errors.date_created" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label class="form-control-label">Content</label>
            <textarea 
              v-model="content" 
              class="form-control form-control-lg" 
              :class="{'is-invalid': errors.content}" 
            ></textarea>
            <div class="invalid-feedback" v-if="errors.content">
              <span v-for="error in errors.content" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Submit</button>
          </div>
        </fieldset>
      </form>
    </div>
  </template>
  
  <script>
    import { mapState } from 'vuex';
    import { mapActions } from 'vuex';
    import axios from 'axios';

  export default {
    data() {
      return {
        legend: 'New Section',
       
          title: '',
          date_created: '',
          content: '',
        errors: {}
      };
    },
    computed:{
        ...mapState(['isAuthenticated', 'role', 'id']),
    },
    methods: {
        ...mapActions(['fetchAuthStatus']),
      async submitForm() {
        try {
          const response = await axios.post('/section/new', {
            'title': this.title,
            'content': this.content,
            'date_created': this.date_created,
            'librarian_id':this.id
          });
          if(response.data.success){
          // Handle success response (e.g., redirect or show a success message)
          this.$router.push('/sections'); // Adjust according to your routing logic
          }
        } catch (error) {
          if (error.response && error.response.data) {
            this.errors = error.response.data.errors || {}; // Assuming your API returns errors in this format
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here if needed */
  </style>
  