import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Home from '../views/Home.vue'
import Bills from '../views/Bills.vue'
import Settings from '../views/Settings.vue'
import Teachers from '../views/Teachers.vue'
import Services from '../views/Services.vue'
import Clients from '../views/Clients.vue'
import SignUp from '../views/SignUp.vue'
// import LogIn from '../views/LogIn.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path:'/bills',
    name:'Bills',
    component: Bills,
    meta: {
      requireLogin: true
    } 
  },
  {
    path: '/gym_settings',
    name: 'Settings',
    component: Settings,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: Teachers,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/services',
    name: 'Services',
    component: Services,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/clients',
    name: 'Clients',
    component: Clients,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  // {
  //   path: '/log-in',
  //   name: 'LogIn',
  //   component: LogIn
  // },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
