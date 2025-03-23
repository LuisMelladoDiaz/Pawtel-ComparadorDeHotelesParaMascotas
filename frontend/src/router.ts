import { createRouter, createWebHistory } from 'vue-router';

import HotelDetailsView from './views/HotelDetailView.vue';
import TemplateScreen1 from './views/TemplateScreen1.vue'
import TemplateScreen2 from './views/TemplateScreen2.vue'
import UserProfile from './views/UserProfile.vue'
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import HotelOwnerPanel from './views/HotelOwnerPanel.vue'
import Home from './views/Home.vue'
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';
import { h, type Component, type VNode } from 'vue';
import LayoutDefault from './views/LayoutDefault.vue';
import LayoutWithFilter from './views/LayoutWithFilter.vue';

type ComponentLike = Component | (() => Promise<Component>);

interface CreateComponentOptions {
  layout: ComponentLike;
  component: ComponentLike;
}

export function createComponent({ layout, component }: CreateComponentOptions): Component {
  if (!layout || !component) {
    throw new Error('[createComponent] Both "layout" and "component" are required.');
  }

  return {
    render() {
      return h(layout, {}, {
        default: () => h(component),
      });
    },
  };
}


const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/sobre-nosotros',
    component: createComponent({
      layout: LayoutDefault,
      component: AboutUs,
    })
  },
  {
    path: '/contacto',
    component: createComponent({
      layout: LayoutDefault,
      component: Contact,
    })
  },
  {
    path: '/hotels',
    component: createComponent({
      layout: LayoutDefault,
      component: HotelListScreen,
    })
  },
  {
    path: '/hotel/:id',
    name: 'HotelDetail',
    component: createComponent({
      layout: LayoutWithFilter,
      component: HotelDetailsView,
    })
  },
  {
    path: '/login',
    component: createComponent({
      layout: LayoutDefault,
      component: LoginView,
    })
  },
  {
    path: '/register',
    component: createComponent({
      layout: LayoutDefault,
      component: RegisterView,
    })
  },
  {
    path: '/user-profile',
    component: createComponent({
      layout: LayoutDefault,
      component: UserProfile,
    })
  },
  {
    path: '/mis-hoteles',
    component: createComponent({
      layout: LayoutDefault,
      component: HotelOwnerPanel,
    })
  },
  {
    path: '/mis-reservas',
    component: createComponent({
      layout: LayoutDefault,
      component: TemplateScreen1,
    })
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
