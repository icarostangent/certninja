import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'vue-toastification/dist/index.css'

import { createApp } from 'vue'
import Toast, { POSITION } from 'vue-toastification'

import App from './App.vue'
import router from './router'
import store from './store'

let app = createApp(App)
app.use(store)
app.use(router)
app.use(Toast, { position: POSITION.TOP_CENTER })
app.config.compilerOptions.isCustomElement = (tag) => {
    return tag.startsWith('stripe')
}
app.mount('#app')
