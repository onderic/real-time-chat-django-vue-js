import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'


axios.defaults.baseURL = 'http://127.0.0.1:8000/'
// npm run dev -- --host 192.168.1.105



const app = createApp(App)

app.use(createPinia())
app.use(router, axios)


app.mount('#app')
