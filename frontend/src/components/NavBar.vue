<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-body">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About Us</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/feedbacks">Student Feedbacks</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/contact">Contact</router-link>
          </li>
          <template v-if="isAuthenticated">
            <template v-if="role === 'student'">
              <li class="nav-item">
                <router-link class="nav-link" to="/student-dash">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/student-graphs">View Student Graphs</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/student-requests">View Requested Books</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/student-issued">View my Issued Books</router-link>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/sp-graphs">View Library Graphs</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/sp-dash">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/new-section">New Section</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/pending-requests">Pending Requests</router-link>
              </li>
            </template>
            <li class="nav-item">
              <router-link class="nav-link" to="/sections">Sections</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/account">Account</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">General User Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">General User Register</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/sp-login">Admin Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/sp-register">Admin Register</router-link>
            </li>
          </template>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  computed: {
    ...mapState(['isAuthenticated', 'role']),
  },
  methods: {
    ...mapActions(['fetchAuthStatus']),
    async logout() {
    await this.$store.dispatch('logout');
  },
  },
  created() {
    this.fetchAuthStatus();
  }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
