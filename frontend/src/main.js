import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueApexCharts from "vue3-apexcharts";
import axios from 'axios'

axios.defaults.baseURL = 'http://10.0.0.242:8000';
//axios.defaults.baseURL = 'http://localhost:8000';
//axios.defaults.baseURL = 'http://chronicle2050.regevson.com';


const app = createApp(App);

app.use(VueApexCharts);
app.use(router)

app.config.globalProperties.$http = axios

app.mount("#app");
