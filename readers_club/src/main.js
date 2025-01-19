import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '../src/assets/style/global.css'
import '../src/assets/fontawesome/css/all.css'
import '../src/assets/fontawesome/css/all.min.css'

createApp(App).use(router).mount('#app')
