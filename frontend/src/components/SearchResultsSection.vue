<template>
  <div>
    <h1>Search Results of Sections</h1>
    <div class="container">
      <ul class="section-list">
        <li v-for="(section, index) in parsedData.sections" :key="index" class="section-card">
          <b>Section Name:</b>
          <a class="article-title" :href="`/section/${section[0].id}`">{{ section[0].name }}</a><br />
          <b>Date Created:</b> {{ formatDate(section[0].date_created) }}<br />
          <b>Description:</b> {{ section[0].description }}<br />
          <b>Added by Librarian:</b> {{ section[0].librarian_username }}<br />
          <div class="books">
            <b>Books in this Section:</b>
            <ul>
              <li v-for="(book, bookIndex) in section[0].books" :key="bookIndex">
                <b>Title:</b> {{ book.title }}<br />
                <b>Author:</b> {{ book.author }}<br />
                <b>Rating:</b> {{ book.rating }}<br />
                <b>Released Year:</b> {{ new Date(book.release_year).getFullYear() }}<br />
                <br />
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  props: {
    data: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState(['isAuthenticated', 'role', 'id']),
    parsedData() {
      return JSON.parse(this.data); // Parse the JSON string into an object
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.section-list {
  list-style-type: none; /* Remove default list styles */
  padding: 0; /* Remove default padding */
}

.section-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
