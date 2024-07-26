<template>
    <div>
      <h1>View Student Feedbacks of our Books</h1>
         <p>Welcome, {{ username }}</p>
        <div v-for="(data, index) in feedbacks" :key="index" class="container">
          <b>Book Title: </b>{{ data.book_title }}<br />
          <b>Student Username: </b>{{ data.student_username }}<br />
          <b>Feedback: </b>{{ data.feedback }}<br />
          <br/>
        </div>
    
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapState, mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        feedbacks: []
      };
    },
    computed: {
      ...mapState(['isAuthenticated', 'role', 'username', 'email'])
    },
    created() {
      this.fetchAuthStatus();
      if (this.isAuthenticated) {
        this.fetchFeedbacks();
      }
    },
    methods: {
      ...mapActions(['fetchAuthStatus']),
      fetchFeedbacks() {
        axios.get('/feedbacks')
          .then(response => {
            this.feedbacks = response.data;
          })
          .catch(error => {
            console.error('Error fetching feedbacks:', error);
          });
      }
    },
    watch: {
      isAuthenticated(newVal) {
        if (newVal) {
          this.fetchFeedbacks();
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-bottom: 20px;
  }
  </style>
  