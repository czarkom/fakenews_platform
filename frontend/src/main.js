import { createApp } from 'vue'
import router from './router'
import '@/assets/css/tailwind.css'
import axios from "axios";
import "vue3-circle-progress/dist/circle-progress.css";
import App from './App.vue'
import {calculateArrowColorUtil, getArrowDirectionUtil} from "@/assets/utils/colorscale";

// Vue.config.productionTip = false
// console.log(process.env.VUE_APP_BASE_URL);
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;

const app  = createApp(App);
app.use(router);
app.mount('#app')

app.config.globalProperties.getArrowDirectionUtil = getArrowDirectionUtil
app.config.globalProperties.calculateArrowColorUtil = calculateArrowColorUtil