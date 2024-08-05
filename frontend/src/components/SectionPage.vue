<template>
    <div>
      <h1>Section Details</h1>
      <div class="container">
        <div v-if="role === 'librarian'">
          <a class="btn btn-secondary btn-sm m-1" :href="`/update-section/${section.id}`">Update Section</a>
          <button type="button" class="btn btn-danger btn-sm m-1" 
        data-toggle="modal" 
        data-target="#deleteModal" 
        @click="setSectionId(section.id)">Delete Section</button>
          <a class="btn btn-secondary btn-sm m-1" :href="`/add-book/${section.id}`">Add a Book to this section</a>
        </div>
        <b>Added by Librarian:</b> {{ section.librarian_username }}<br />
        <b>Date Created:</b> {{ formatDate(section.date_created) }}<br />
        <b>Section Name:</b> {{ section.name }}<br />
        <b>Description:</b> {{ section.description }}<br />
      </div>
  
      <br />
      <div v-if="section.books.length > 0" class="container">
        <h3>Books in {{ section.name }} Section</h3>
        <div v-for="(book, index) in section.books" :key="index" class="container">
          <div v-if="role === 'librarian'">
            <a class="btn btn-secondary btn-sm m-1" :href="`/update-book/${section.id}/${book.id}`">Update This Book</a>
            <button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" :data-target="'#delete' + book.id + 'BookModal'">Delete This Book</button>
          </div>
          <b>Title: </b>{{ book.title }}<br />
          <b>Author: </b>{{ book.author }}<br />
          <b>Language: </b>{{ book.lang }}<br />
          <b>Rating: </b>{{ book.rating }}<br />
          <b>Released year: </b>{{ formatDate(book.release_year) }}<br />
  
          <div class="modal fade" :id="'delete' + book.id + 'BookModal'" tabindex="-1" role="dialog" aria-labelledby="deleteBookLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Book "{{ book.title }}"?</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <form :action="`/delete-book/${section.id}/${book.id}`" method="POST">
                            <input type="submit" class="btn btn-danger" value="Delete" />
                        </form>
                    </div>
                </div>
            </div>
        </div>

          
        </div>
      </div>
      <br />
      
      <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteLabel" aria-hidden="true" v-if="showModal">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Delete Section?</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <p>Warning! Deleting the Section will delete all its books!</p>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <button type="button" class="btn btn-danger" @click="confirmDelete()">Delete</button>
            </div>
          </div>
        </div>
      </div>
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
    computed:{
        ...mapState(['isAuthenticated', 'role', 'id']),
    },
    data() {
    return {
      section: null, // Initialize section data
      sectionToDelete: null,
      showModal:false
    };
  },
  created() {
    this.fetchSectionData(); // Fetch section data when the component is created
  },
  methods: {
    ...mapActions(['fetchAuthStatus']),
    setSectionId(id) {
            this.sectionIdToDelete = id; // Set the ID when the button is clicked
            this.showModal=true;
        },
        async confirmDelete() {
          try{
                const response = await axios.post('/delete-section',{'section_id':this.sectionIdToDelete});
                if(response.data.success){
                  this.showModal=false;
                    this.$router.push("/home");
                }
              }
              catch (error) {
                console.error('Error fetching section data:', error);
              }
                   
        },
    async fetchSectionData() {
      try {
        const response = await axios.post(`/section`,{'section_id':this.section_id}); // Make an API call using section_id
        this.section = response.data.section; // Populate section data
        this.section.books=response.data.book_list;
    } catch (error) {
        console.error('Error fetching section data:', error);
      }
    },
    formatDate(dateString) {
      const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
  };
  </script>
  
  <style scoped>
  .container {
    margin: 1rem 0;
  }
  </style>
  
<!-- 
   <template>
    <div>
      <h1>Section Details</h1>
      <div class="container">
        <div v-if="role === 'librarian'">
          <a class="btn btn-secondary btn-sm m-1" :href="`/update-section/${section.id}`">Update Section</a>
          <button type="button" class="btn btn-danger btn-sm m-1" @click="setSectionId(section.id)">Delete Section</button>
          <a class="btn btn-secondary btn-sm m-1" :href="`/add-book/${section.id}`">Add a Book to this section</a>
        </div>
        <b>Added by Librarian:</b> {{ section.librarian_username }}<br />
        <b>Date Created:</b> {{ formatDate(section.date_created) }}<br />
        <b>Section Name:</b> {{ section.name }}<br />
        <b>Description:</b> {{ section.description }}<br />
      </div>
  
      <br />
      <div v-if="section.books.length > 0" class="container">
        <h3>Books in {{ section.name }} Section</h3>
        <div v-for="(book, index) in section.books" :key="index" class="container">
          <div v-if="role === 'librarian'">
            <a class="btn btn-secondary btn-sm m-1" :href="`/update-book/${section.id}/${book.id}`">Update This Book</a>
            <button type="button" class="btn btn-danger btn-sm m-1" @click="setBookId(book.id)">Delete This Book</button>
          </div>
          <b>Title: </b>{{ book.title }}<br />
          <b>Author: </b>{{ book.author }}<br />
          <b>Language: </b>{{ book.lang }}<br />
          <b>Rating: </b>{{ book.rating }}<br />
          <b>Released year: </b>{{ formatDate(book.release_year) }}<br />

          <div class="modal fade" :id="'delete' + book.id + 'BookModal'" tabindex="-1" role="dialog" aria-labelledby="deleteBookLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Delete Book "{{ book.title }}"?</h5>
                  <button type="button" class="close" @click="closeBookModal">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeBookModal">Close</button>
                  <form :action="`/delete-book/${section.id}/${book.id}`" method="POST">
                    <input type="submit" class="btn btn-danger" value="Delete" />
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <br />
  
      <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteLabel" aria-hidden="true" v-if="showModal">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Delete Section?</h5>
              <button type="button" class="close" @click="closeModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <p>Warning! Deleting the Section will delete all its books!</p>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              <button type="button" class="btn btn-danger" @click="confirmDelete()">Delete</button>
            </div>
          </div>
        </div>
      </div>
  
      <div class="modal-backdrop fade" v-if="showModal"></div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex';
  import axios from 'axios';
  
  export default {
    props: {
      section_id: {
        type: String,
        required: true,
      },
    },
    computed: {
      ...mapState(['isAuthenticated', 'role', 'id']),
    },
    data() {
      return {
        section: null,
        sectionIdToDelete: null,
        showModal: false,
      };
    },
    created() {
      this.fetchSectionData();
    },
    methods: {
      ...mapActions(['fetchAuthStatus']),
      setSectionId(id) {
        this.sectionIdToDelete = id;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
      closeBookModal() {
        // Implement functionality to close the book modal if needed
      },
      async confirmDelete() {
        try {
          const response = await axios.post('/delete-section', { section_id: this.sectionIdToDelete });
          if (response.data.success) {
            this.showModal = false;
            this.$router.push("/home");
          }
        } catch (error) {
          console.error('Error deleting section:', error);
        }
      },
      async fetchSectionData() {
        try {
          const response = await axios.post(`/section`, { section_id: this.section_id });
          this.section = response.data.section;
          this.section.books = response.data.book_list;
        } catch (error) {
          console.error('Error fetching section data:', error);
        }
      },
      formatDate(dateString) {
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    margin: 1rem 0;
  }
  </style>
   -->