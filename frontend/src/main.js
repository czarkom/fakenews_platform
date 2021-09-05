import Vue from 'vue'
import App from './App.vue'
import router from './router'
import '@/assets/css/tailwind.css'
import axios from "axios";


Vue.config.productionTip = false
// console.log(process.env.VUE_APP_BASE_URL);
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
