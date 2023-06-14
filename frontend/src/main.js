import './assets/main.css'
import '@fortawesome/fontawesome-free/css/all.css';


import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import Toast from './components/Toast.vue'


axios.defaults.baseURL = 'http://127.0.0.1:8000/'
// npm run dev -- --host 192.168.1.105



const app = createApp(App)

app.use(createPinia())
app.use(router, axios)

app.component('toast', Toast )

app.mount('#app')
