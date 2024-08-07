import { createApp } from 'vue'

import App from './App.vue'
import router from './routes'
import axios from 'axios'
import BootstrapVue3 from "bootstrap-vue-3";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";
// import {toast} from 'vue3-toastify';
// import 'vue3-toastify/dist/index.css';

const app = createApp(App)

axios.defaults.baseURL = 'http://127.0.0.1:8000';
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})

app.config.globalProperties.$axios = axiosInstance;
app.use(router);
app.use(BootstrapVue3);
// app.use(toast);

app.mount('#app');
