import { createRouter, createWebHistory } from 'vue-router';

import HotelDetailsView from './views/HotelDetailView.vue';
import UserProfile from './views/UserProfile.vue'
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import MisHoteles from './views/MisHoteles.vue'
import MyBookings from './views/MyBookings.vue'
import EditHotel from './views/EditHotel.vue'
import Home from './views/Home.vue'
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';
import { h, type Component} from 'vue';
import LayoutDefault from './views/LayoutDefault.vue';
import LayoutWithFilter from './views/LayoutWithFilter.vue';
import LayoutDefaultWhite from './views/LayoutDefaultWhite.vue';
import { type RouteRecordRaw } from 'vue-router';
import axios from 'axios';

type ComponentLike = Component | (() => Promise<Component>);

interface CreateComponentOptions {
  layout: ComponentLike;
  component: ComponentLike;
}

export function createComponent({ layout, component }: CreateComponentOptions): Component {
  return {
    render() {
      return h(layout, {}, {
        default: () => h(component),
      });
    },
  };
}

enum AuthRequirement {
  LOGGED_IN_CUSTOMER = 'logged_in_customer',
  LOGGED_IN_HOTEL_OWNER = 'logged_in_hotel_owner',
  LOGGED_OUT = 'logged_out',
}

const ALLOW_ALL = [
  AuthRequirement.LOGGED_IN_CUSTOMER,
  AuthRequirement.LOGGED_IN_HOTEL_OWNER,
  AuthRequirement.LOGGED_OUT,
];

const ALLOW_LOGGED_IN = [
  AuthRequirement.LOGGED_IN_CUSTOMER,
  AuthRequirement.LOGGED_IN_HOTEL_OWNER,
];

function transformRoutes(routes: RouteRecordRaw[]): RouteRecordRaw[] {
  return routes.map((route) => {
    const newRoute: RouteRecordRaw = { ...route };
    if (newRoute.meta && (newRoute.meta as any).allowedAuthStates) {
      if ((newRoute.meta as any).hasOwnProperty('allowedAuthStates')) {
        if (!Array.isArray((newRoute.meta as any).allowedAuthStates)) {
          throw new Error('allowedAuthStates must be an array, got: ' + (newRoute.meta as any).allowedAuthStates);
        }
      }
      const allowedStates = (newRoute.meta as any).allowedAuthStates as AuthRequirement[];
      newRoute.beforeEnter = async (to, from) => {
        try {
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/auth/user-info/`);
        const role = response.data.role;
        const state = role == 'customer' ? AuthRequirement.LOGGED_IN_CUSTOMER : role == 'hotel_owner' ? AuthRequirement.LOGGED_IN_HOTEL_OWNER : AuthRequirement.LOGGED_OUT;
        if (!allowedStates.includes(state)) {
           return '/';
        }
        return true;
        } catch (e) {
          if (allowedStates.includes(AuthRequirement.LOGGED_OUT)) {
            return true;
          } else {
            return '/login';
          }
        }
      };
    }

    // 3) Recursively handle any children
    if (route.children && route.children.length > 0) {
      newRoute.children = transformRoutes(route.children);
    }

    return newRoute;
  });
}
import BookingReservationForm from './views/BookingReservationForm.vue';


const routes = [
  {
    path: '/',
    component: Home,
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/sobre-nosotros',
    component: createComponent({ layout: LayoutDefault, component: AboutUs }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    }
  },
  {
    path: '/contacto',
    component: createComponent({ layout: LayoutDefault, component: Contact }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/hotels',
    component: createComponent({ layout: LayoutWithFilter, component: HotelListScreen }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/hotel/:id',
    name: 'HotelDetail',
    component: createComponent({ layout: LayoutDefaultWhite, component: HotelDetailsView }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/login',
    component: createComponent({ layout: LayoutDefault, component: LoginView }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_OUT],
    },
  },
  {
    path: '/register',
    component: createComponent({ layout: LayoutDefault, component: RegisterView }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_OUT],
    },
  },
  {
    path: '/user-profile',
    component: createComponent({ layout: LayoutDefault, component: UserProfile }),
    meta: {
      allowedAuthStates: ALLOW_LOGGED_IN, // TODO
    },
  },
  {
    path: '/mis-reservas',
    component: createComponent({ layout: LayoutDefault, component: MyBookings }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_CUSTOMER],
    },
  },
  {
    path: '/mis-hoteles',
    component: createComponent({ layout: LayoutDefault, component: MisHoteles }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_HOTEL_OWNER],
    },
  },
  {
    path: '/mis-hoteles/edit/:id',
    component: createComponent({ layout: LayoutDefault, component: EditHotel }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_HOTEL_OWNER],
    },
  },
  {
    path: '/hotel/reservation-form/:id',
    component: createComponent({ layout: LayoutDefault, component: BookingReservationForm }),
    meta: {
      allowedAuthStates: ALLOW_LOGGED_IN,
    },
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes: transformRoutes(routes),
});

export default router;
