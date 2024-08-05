<template>
    <div>
      <h1>List of Available Sections</h1>
      <div class="container" v-for="section in sortedSections" :key="section[0].id">
        <b>Section Name:</b>
        <a class="article-title" :href="`/section/${section[0].id}`">{{ section[0].name }}</a><br />
        <b>Date Created:</b> {{ formatDate(section[0].date_created) }}<br />
        <b>Description:</b> {{ section[0].description }}<br />
        <b>Added by Librarian:</b> {{ section[1] }}<br />
        <br />
      </div>
    </div>
  </template>
  
  <script>

  import { mapState } from 'vuex';
  import { mapActions } from 'vuex';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        sections: [],
      };
    },
    computed: {
        ...mapState(['isAuthenticated', 'role', 'id']),
      sortedSections() {
        return this.sections
          .slice()
          .sort((a, b) => new Date(b[0].date_created) - new Date(a[0].date_created));
      },
    },
    methods: {
        ...mapActions(['fetchAuthStatus']),
      async fetchSections() {
        try {
          const response = await axios.get('/sections'); // Adjust the endpoint as needed
          this.sections = response.data.sections;
        } catch (error) {
          console.error("Error fetching sections:", error);
        }
      },
      formatDate(dateString) {
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
    },
    mounted() {
      this.fetchSections();
    },
  };
  </script>
  
  <style scoped>
  /* Add any necessary styles here */
  </style>
  