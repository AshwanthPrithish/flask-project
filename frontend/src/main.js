import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.css';

Vue.config.productionTip = false;

axios.defaults.headers.common['X-CSRF-Token'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content')

store.dispatch('fetchAuthStatus').then(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app');
}).catch(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app');
});