import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import {VueQueryPlugin } from '@tanstack/vue-query'
import { library } from '@fortawesome/fontawesome-svg-core';
import { faLocationDot } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { refreshAxiosInterceptor } from './axios-setup'

createApp(App).use(router).use(VueQueryPlugin).mount('#app')

library.add(faLocationDot);

//App.component('font-awesome-icon', FontAwesomeIcon); // esto falla, hay que verlo

refreshAxiosInterceptor()
