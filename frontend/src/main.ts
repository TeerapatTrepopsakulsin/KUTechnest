import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import { createPinia } from 'pinia'
import vue3GoogleOauth from 'vue3-google-login'


const app = createApp(App);
const pinia = createPinia();
app.use(vue3GoogleOauth, { clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID });
app.use(pinia);
app.use(router);
app.mount('#app');
