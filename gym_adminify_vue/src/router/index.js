import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Bills from '../views/Bills.vue'
import Settings from '../views/Settings.vue'
import Teachers from '../views/Teachers.vue'

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
    path: '/teachers/substitutes',
    name: 'TeachersSubstitutes',
    component: Teachers
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
