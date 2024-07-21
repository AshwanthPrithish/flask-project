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

Vue.use(Router);

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: AboutPage },
  { path: '/feedbacks', component: FeedbacksPage },
  { path: '/contact', component: ContactPage },
  { path: '/student-dash', component: StudentDash },
  { path: '/sp-graphs', component: SpGraphs },
  { path: '/sp-dash', component: SpDash },
  { path: '/new-section', component: NewSection },
  { path: '/pending-requests', component: PendingRequests },
  { path: '/sections', component: LibSections },
  { path: '/account', component: Account },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/sp-login', component: SpLogin },
  { path: '/sp-register', component: SpRegister },
  { path: '/student-graphs', component: StudentGraphs },
  { path: '/student-requests', component: StudentRequests },
  { path: '/student-issued', component: StudentIssued },
];

const router = new Router({
    mode: 'history',
    routes,
});

export default router;
