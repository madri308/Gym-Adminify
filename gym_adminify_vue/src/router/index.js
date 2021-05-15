import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'
import { toast } from "bulma-toast";

import Home from '../views/Home.vue'
import Bills from '../views/Bills.vue'
import Settings from '../views/Settings.vue'
import Teachers from '../views/Teachers.vue'
import Services from '../views/Services.vue'
import Clients from '../views/Clients.vue'
import SignUp from '../views/SignUp.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path:'/billsByMonth',
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
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if(!store.state.permsLoaded && to.name != 'Home'){
    toast({
      message: "Cargando permisos espere un momento", type: "is-info",
      dismissible: true, pauseOnHover: true,
      duration: 2000, position: "bottom-right",
    });
    next({ name: 'Home', query: { to: to.path } });
  }else if ((to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) || !hasAccess(to.name)) {
    toast({
      message: "No puede acceder a la direccion", type: "is-danger",
      dismissible: true, pauseOnHover: true,
      duration: 2000, position: "bottom-right",
    });
    next({ name: 'Home', query: { to: to.path } });
  } else {
    next()
  }
})

const hasAccess = function(name) {

  // const permissions = localStorage.getItem("userPermissions");
  const permissions = store.state.permissions

  switch (name) {
    case "Home":
      return true;
    case "Settings":
      return permissions.includes("gymSettings.view_gym")
    default:
      return true;
  }
  
}

export default router
