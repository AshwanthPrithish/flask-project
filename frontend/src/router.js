import Vue from 'vue';
import Router from 'vue-router';
import HomePage from './components/HomePage.vue';
import AboutPage from './components/AboutPage.vue';
import FeedbacksPage from './components/FeedbackPage.vue';
import ContactPage from './components/ContactPage.vue';
import StudentDash from './components/StudentDash.vue';
import SpGraphs from './components/SpGraphs.vue';
import SpDash from './components/SpDash.vue';
import NewSection from './components/NewSection.vue';
import PendingRequests from './components/PendingRequests.vue';
import LibSections from './components/LibSections.vue';
import Account from './components/AccountPage.vue';
import Login from './components/LoginPage.vue';
import Register from './components/StudentRegister.vue';
import SpLogin from './components/SpLogin.vue';
import SpRegister from './components/SpRegister.vue';
import StudentGraphs from './components/StudentGraphs.vue';
import StudentRequests from './components/StudentRequests.vue';
import StudentIssued from './components/StudentIssued.vue';
import SearchResultsAuthor from './components/SearchResultsAuthor.vue';
import store from './store';


Vue.use(Router);

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/about', component: AboutPage },
  { path: '/feedbacks', component: FeedbacksPage },
  { path: '/contact', component: ContactPage },
  { path: '/student-dash', name: 'student-dash', meta:{requiresAuth:true},component: StudentDash },
  {
    path: '/search-results-author/:query',
    name: 'SearchResultsAuthor',
    component: SearchResultsAuthor,
    props: true
  },
  { path: '/sp-graphs', component: SpGraphs },
  { path: '/sp-dash', component: SpDash },
  { path: '/new-section', component: NewSection },
  { path: '/pending-requests', component: PendingRequests },
  { path: '/sections', component: LibSections },
  { path: '/account', component: Account },
  { path: '/login',name:'login',meta:{requiresGuest: true}, component: Login },
  { path: '/register', component: Register },
  { path: '/sp-login', component: SpLogin },
  { path: '/sp-register', component: SpRegister },
  { path: '/student-graphs', component: StudentGraphs },
  { path: '/student-requests', component: StudentRequests },
  { path: '/student-issued', component: StudentIssued },
  {
    path: '/logout',
    name: 'logout',
    component: {
      template: '<div>Logging out...</div>',
      created() {
        this.logoutUser();
      },
      methods: {
        async logoutUser() {
          await this.$store.dispatch('logout');
        }
      }
    }
  },
];

const router = new Router({
    mode: 'history',
    routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.isAuthenticated) {
      next({ name: 'home' }); // Redirect to login if not authenticated
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (store.state.isAuthenticated) {
      next({ name: 'home' }); // Redirect to dashboard if already authenticated
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
