import { createRouter, createWebHistory } from 'vue-router';

import HotelDetailsView from './views/HotelDetailView.vue';
import HotelRoomsAndPrices from './views/HotelRoomsAndPrices.vue';
import UserProfile from './views/UserProfile.vue'
import UserList from './views/UserList.vue';
import HotelListScreen from './views/HotelListScreen.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import MisHoteles from './views/MisHoteles.vue'
import MyBookings from './views/MyBookings.vue'
import EditHotel from './views/EditHotel.vue'
import EmailPasswordReset from './views/EmailPasswordReset.vue'
import PasswordResetConfirm from './views/ResetPassword.vue'
import Home from './views/Home.vue'
import AboutUs from './views/AboutUs.vue';
import Contact from './views/Contact.vue';
import HotelOwners from './views/HotelOwners.vue';
import { h, type Component} from 'vue';
import LayoutDefault from './views/LayoutDefault.vue';
import LayoutWithFilter from './views/LayoutWithFilter.vue';
import LayoutDefaultWhite from './views/LayoutDefaultWhite.vue';
import { type RouteRecordRaw } from 'vue-router';
import api from '@/api';

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
  LOGGED_IN_ADMIN = 'logged_in_admin',

}

const ALLOW_ALL = [
  AuthRequirement.LOGGED_IN_CUSTOMER,
  AuthRequirement.LOGGED_IN_HOTEL_OWNER,
  AuthRequirement.LOGGED_IN_ADMIN,
  AuthRequirement.LOGGED_OUT,
  AuthRequirement.LOGGED_IN_ADMIN,
];

const ALLOW_LOGGED_IN = [
  AuthRequirement.LOGGED_IN_CUSTOMER,
  AuthRequirement.LOGGED_IN_HOTEL_OWNER,
  AuthRequirement.LOGGED_IN_ADMIN,
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
        if (new Set(allowedStates).size === new Set(ALLOW_ALL).size && [...new Set(allowedStates)].every(value => new Set(ALLOW_ALL).has(value))) {
          return true;
        }
        try {
          const response = await api.get("auth/user-info/").json<any>();
          const role = response.role;
          const state = role == 'customer' ? AuthRequirement.LOGGED_IN_CUSTOMER : role == 'admin' ? AuthRequirement.LOGGED_IN_ADMIN : role == 'hotel_owner' ? AuthRequirement.LOGGED_IN_HOTEL_OWNER : AuthRequirement.LOGGED_OUT;
          if (!allowedStates.includes(state)) {
            return '/';
          }
          if (route.meta.allowNotApproved === false && state === AuthRequirement.LOGGED_IN_HOTEL_OWNER) {
            if (response.is_approved === false) {
              return '/esperando-aprobacion';
            }
          }
          if (route.meta.allowApproved === false && state === AuthRequirement.LOGGED_IN_HOTEL_OWNER) {
            if (response.is_approved === true) {
              return '/mis-hoteles';
            }
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
    if (route.children && route.children.length > 0) {
      newRoute.children = transformRoutes(route.children);
    }
    return newRoute;
  });
}
import BookingReservationForm from './views/BookingReservationForm.vue';
import TermsAndConditions from './views/TermsAndConditions.vue';
import LayoutLogoNavBarOnly from './views/LayoutLogoNavBarOnly.vue';
import PendingApprovalVue from './views/PendingApproval.vue';



const routes = [
  {
    path: '/',
    component: Home,
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/admin/user-list',
    component: createComponent({ layout: LayoutDefault, component: UserList }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_ADMIN],
    }
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
    path: '/duenos-alojamientos',
    component: createComponent({ layout: LayoutDefault, component: HotelOwners }),
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
    component: createComponent({ layout: LayoutWithFilter, component: HotelDetailsView }),
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
      allowedAuthStates: ALLOW_LOGGED_IN,
      allowNotApproved: false,
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
      allowNotApproved: false,
    },
  },
  {
    path: '/email-password-reset',
    component: createComponent({ layout: LayoutDefault, component: EmailPasswordReset }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/auth/password-reset-confirm/:uidb64/:token',
    component: createComponent({ layout: LayoutLogoNavBarOnly, component: PasswordResetConfirm }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/mis-hoteles/edit/:id',
    component: createComponent({ layout: LayoutDefault, component: EditHotel }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_HOTEL_OWNER],
      allowNotApproved: false,
    },
  },
  {
    path: '/hotel/:hotelId/:roomId/confirmar-reserva',
    name: 'BookingReservation',
    component: createComponent({ layout: LayoutDefault, component: BookingReservationForm }),
    meta: {
      allowedAuthStates: ALLOW_LOGGED_IN,
    },
    props: (route) => ({
      id: route.params.id,
      room: route.query.room,
      quantity: route.query.quantity
    }),
  },
  {
    path: '/terminos-y-condiciones',
    name: 'TermsAndConditions',
    component: createComponent({ layout: LayoutDefault, component: TermsAndConditions }),
    meta: {
      allowedAuthStates: ALLOW_ALL,
    },
  },
  {
    path: '/esperando-aprobacion',
    name: 'EsperandoAprobacion',
    component: createComponent({ layout: LayoutDefaultWhite, component: PendingApprovalVue }),
    meta: {
      allowedAuthStates: [AuthRequirement.LOGGED_IN_HOTEL_OWNER],
      allowApproved: false,
    },
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes: transformRoutes(routes),
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
    return { top: 0 };
  }
});


router.beforeEach((to, from, next) => {
  // Keys of filters we want to preserve
  const preservedQueryKeys = ['filterCity', 'filterType', 'filterStartDate', 'filterEndDate']

  const preservedQuery = {}

  preservedQueryKeys.forEach((key) => {
    if (key in from.query && !(key in to.query)) {
      preservedQuery[key] = from.query[key]
    } else if (key in to.query) {
      preservedQuery[key] = to.query[key]
    }
  })

  const nextQuery = {
    ...to.query,
    ...preservedQuery,
  }

  // if is equal, no need to change `nextQuery`
  if (JSON.stringify(nextQuery) === JSON.stringify(to.query)) {
    next()
    return;
  }


  if (Object.keys(preservedQuery).length > 0) {
    next({
      ...to,
      query: {
        ...to.query,
        ...preservedQuery,
      },
    })
    return;
  } else {
    next()
    return;
  }
})

export default router;
