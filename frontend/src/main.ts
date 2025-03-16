import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import {VueQueryPlugin } from '@tanstack/vue-query'
import { library } from '@fortawesome/fontawesome-svg-core';
import { faLocationDot } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';
import * as a from './axios-setup';
import { defineRule } from 'vee-validate';
import { required } from '@vee-validate/rules';

// Define VeeValidate rules
defineRule('required', required);

const notyf = new Notyf({
    duration: 3000,
    position: { x: 'center', y: 'top' },
  });

const app = createApp(App);
app.config.globalProperties.$notyf = notyf;

app.use(router).use(VueQueryPlugin).mount('#app')

library.add(faLocationDot);

//App.component('font-awesome-icon', FontAwesomeIcon); // esto falla, hay que verlo
