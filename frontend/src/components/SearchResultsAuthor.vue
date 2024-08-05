<template>
    <div>
      <h1>Search Results of Book Author</h1>
      <div class="container">
        <ul class="book-list">
          <li v-for="(book, index) in parsedData.books" :key="index" class="book-card">
            <div v-if="role === 'student' && !book.content">
              <a class="btn btn-secondary btn-sm m-1" :href="`/request_book/${book.section_id}/${book.id}`">Request This Book</a>
            </div>
            <b>Title: </b>{{ book.title }}<br />
            <b>Author: </b>{{ book.author }}<br />
            <b>Language: </b>{{ book.lang }}<br />
            <b>Section: </b>{{ book.section }}<br />
            <div v-if="book.content">
              <b>Content: </b>
              <div class="card" style="height: 300px; overflow-y: auto;">
                <div class="card-body">
                  <center><b>{{ book.title }}</b></center>
                  <center>By - <em>{{ book.author }}</em></center>
                  <hr />
                  {{ book.content }}
                </div>
              </div>
              <br />
            </div>
            <b>Rating: </b>{{ book.rating }}<br />
            <b>Released year: </b>{{ new Date(book.release_year).getFullYear() }}<br />
          </li>
        </ul>
      </div>
    </div>
  </template>

<script>

    import { mapState } from 'vuex';
    import { mapActions } from 'vuex';
    export default{
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
    ...mapActions(['fetchAuthStatus']),
    formatReleaseYear(date) {
      return new Date(date).getFullYear(); // Format release year as needed
    },
  },
    }
</script>

<style scoped>
    .book-list {
  list-style-type: none; /* Remove default list styles */
  padding: 0; /* Remove default padding */
}

.book-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content-textarea {
  width: 100%;
  height: 150px;
  resize: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  font-family: Arial, sans-serif;
}
</style>