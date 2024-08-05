<template>
    <div class="container">
      <h1>Library Management System - Student {{ username }} Dashboard</h1>
  
      <form @submit.prevent="submitSectionForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Search by Section</legend>
          
          <div class="form-group">
            <label for="section" class="form-control-label">Section</label>
            <input
              type="text"
              v-model="section"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': sectionError }"
              id="section"
            />
            <div v-if="sectionError" class="invalid-feedback">
              <span>{{ sectionError }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Search</button>
          </div>
        </fieldset>
      </form>
  
      <form @submit.prevent="submitTitleForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Search by Title</legend>
          
          <div class="form-group">
            <label for="title" class="form-control-label">Title</label>
            <input
              type="text"
              v-model="title"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': titleError }"
              id="title"
            />
            <div v-if="titleError" class="invalid-feedback">
              <span>{{ titleError }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Search</button>
          </div>
        </fieldset>
      </form>
  
      <form @submit.prevent="submitAuthorForm">
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Search by Author</legend>
          
          <div class="form-group">
            <label for="author" class="form-control-label">Author</label>
            <input
              type="text"
              v-model="author"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': authorError }"
              id="author"
            />
            <div v-if="authorError" class="invalid-feedback">
              <span>{{ authorError }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Search</button>
          </div>
        </fieldset>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapState } from 'vuex';
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        section: '',
        title: '',
        author: '',
        sectionError: null,
        titleError: null,
        authorError: null
      };
    },
    computed: {
      ...mapState(['username'])
    },
    created() {
    this.fetchAuthStatus();
  },
    methods: {
      ...mapActions(['fetchAuthStatus']),
      async submitSectionForm() {
        this.sectionError = null;
  
        try {
          const response = await axios.post('http://localhost:5000/search-results-section', {
            section: this.section
          });
          if(response.data.success){
          this.$router.push({ name: 'SearchResultsSection', params: { 
      data: JSON.stringify({ section: this.section, sections: response.data.sections }) 
    }  });
          }
        } catch (error) {
          this.sectionError = error.response.data.message;
        }
      },
      async submitTitleForm() {
        this.titleError = null;
  
        try {
         await axios.post('http://localhost:5000/api/search_title', {
            title: this.title
          });
          this.$router.push({ name: 'SearchResultsTitle', query: { query: this.title } });
        } catch (error) {
          this.titleError = error.response.data.message;
        }
      },
      async submitAuthorForm() {
        this.authorError = null;
        try {

          const response = await axios.post('http://localhost:5000/search-results-author', {
            author: this.author
          });
          this.$router.push({ name: 'SearchResultsAuthor', params: { 
      data: JSON.stringify({ author: this.author, books: response.data.books }) 
    }  });
        } catch (error) {
          this.authorError = error.response.data.message;
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
  </style>
  