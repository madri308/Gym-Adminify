import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Bills from '../views/Bills.vue'
import Settings from '../views/Settings.vue'
import Teachers from '../views/Teachers.vue'
import Services from '../views/Services.vue'
import Clients from '../views/Clients.vue'

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
    path:'/billsByMonth',
    name:'Bills',
    component: Bills, 
  },
  {
    path: '/gym_settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: Teachers
  },
  {
    path: '/services',
    name: 'Services',
    component: Services
  },
  {
    path: '/clients',
    name: 'Clients',
    component: Clients
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
