<template>
    <div class="container">
      <form @submit.prevent="submitForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">{{ legend }}</legend>
  
          <div class="form-group">
            <label class="form-control-label">Section Name</label>
            <input
              v-model="section.name"
              type="text"
              class="form-control form-control-lg"
              :class="{'is-invalid': errors.name}"
            />
            <div class="invalid-feedback" v-if="errors.name">
              <span v-for="error in errors.name" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label class="form-control-label">Date Created</label>
            <input
              v-model="section.date_created"
              type="date"
              class="form-control form-control-lg"
              :class="{'is-invalid': errors.date_created}"
            />
            <div class="invalid-feedback" v-if="errors.date_created">
              <span v-for="error in errors.date_created" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <label class="form-control-label">Description</label>
            <textarea
              v-model="section.description"
              class="form-control form-control-lg"
              :class="{'is-invalid': errors.description}"
            ></textarea>
            <div class="invalid-feedback" v-if="errors.description">
              <span v-for="error in errors.description" :key="error">{{ error }}</span>
            </div>
          </div>
  
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Update</button>
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
    props: {
      section_id: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        legend: 'Update Section',
        section: {
          name: '',
          date_created: '',
          description: '',
        },
        errors: {},
      };
    },
    computed: {
      ...mapState(['isAuthenticated', 'role', 'id']),
    },
    created() {
      this.fetchSectionData(); // Fetch section data when the component is created
    },
    methods: {
      ...mapActions(['fetchAuthStatus']),
      async fetchSectionData() {
        try {
          const response = await axios.get("/section/update",{'section_id':this.section_id}); // Use GET request to fetch data
          this.section = response.data.section; // Populate section data
        } catch (error) {
          console.error('Error fetching section data:', error);
        }
      },
      async submitForm() {
        try {
          const response = await axios.post('/section/update', {
            'section_id': this.section_id,
            'name': this.section.name,
            'description': this.section.description,
            'date_created': this.section.date_created,
          });
          if (response.data.success) {
            // Handle success response (e.g., redirect or show a success message)
            this.$router.push('/sections'); // Adjust according to your routing logic
          }
        } catch (error) {
          if (error.response && error.response.data) {
            this.errors = error.response.data.errors || {}; // Assuming your API returns errors in this format
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here if needed */
  </style>
  