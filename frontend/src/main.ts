import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faLocationDot } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';
import * as a from './api';
import { defineRule, configure } from 'vee-validate';
import { required } from '@vee-validate/rules';
import { customMessages } from './validation-messages';
import { createPinia } from 'pinia';
import 'aos/dist/aos.css';
import AOS from 'aos';

AOS.init();

defineRule('required', required);

configure({
  validateOnInput: true,
  //@ts-ignore
  messages: customMessages,  // Usar solo los mensajes personalizados
});

const notyf = new Notyf({
  duration: 3000,
  position: { x: 'center', y: 'top' },
});

const app = createApp(App);

app.use(createPinia());

app.config.globalProperties.$notyf = notyf;

library.add(faLocationDot);

app.component('font-awesome-icon', FontAwesomeIcon);

app.use(router).use(VueQueryPlugin).mount('#app');
