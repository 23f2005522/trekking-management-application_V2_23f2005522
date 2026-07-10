import { createApp } from 'vue'
import App from './App.vue'

// Import the favicon and set it as the page's favicon
import favicon from '@/assets/hiking.png'
const link = document.querySelector("link[rel~='icon']")
link.href = favicon


// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'


import router from './router'
import {createPinia} from "pinia"



const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
