<template>
  <div id="wrapper" >
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link @click="page=0" to="/" class="navbar-item" :class="page == 0? 'bg-black' : ''">
          <strong>Gym-Adminify</strong>
        </router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <!-- SI ESTA AUTENTIFICADO ES DECIR LOGEADO -->
          <template v-if="$store.state.isAuthenticated">
            <router-link @click="page=1" v-if="canViewClient" to="/clients" class="navbar-item" :class="page == 1? 'bg-black' : ''">
              Clientes
            </router-link>
            <nav :class="open ? 'navbar-open' : 'navbar-close'" class="navbar w-56 fixed bg-gray-900 top-20 left-0 h-auto">
              <ul>
                <div v-for="info in userInfo" :key="info" class="relative mt-2 mb-2 left-3">
                  <!-- <b>{{info.key}}: </b> -->
                  <li>‣ {{info.value}}</li>
                </div>
              </ul>
            </nav>
            <router-link @click="page=2" to="/billsByMonth" class="navbar-item" :class="page == 2? 'bg-black' : ''">
              Facturas
            </router-link>
            <router-link @click="page=3" to="/teachers" class="navbar-item" :class="page == 3? 'bg-black' : ''">
              Instructores
            </router-link>
          </template>
          <!-- SI NO ESTA LOGEADO -->
          <template v-else>
            <router-link @click="page=4" to="/about" class="navbar-item" :class="page == 4? 'bg-black' : ''">
              ¿Quienes somos?
            </router-link>
          </template>
          <!-- SIEMPRE SE PUEDEN VER -->
          <router-link @click="page=5" to="/services" class="navbar-item" :class="page == 5? 'bg-black' : ''">
            Servicios
          </router-link>
          <router-link @click="page=6" to="/activities" class="navbar-item" :class="page == 6? 'bg-black' : ''">
            Actividades
          </router-link>
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <!-- SI ESTA AUTENTIFICADO ES DECIR LOGEADO -->
            <template v-if="$store.state.isAuthenticated">
              <router-link v-if="canViewConfig" to="/gym_settings" @click="page=7" class="button is-light" :class="page == 7? 'is-success' : ''">
                <span class="icon"><i class="fas fa-info"></i></span>
              </router-link>
              <button @click='open = !open ' class="button is-light" :class="open ? 'is-success' : ''">
                <span class="icon"><i class="fas fa-user"></i></span>
              </button>
              <button @click="logout()" class="button is-light">
                Salir
              </button>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <div  v-show='messageToggle' id="messageCovid" class="bg-indigo-600" >
      <div class="max-w-7xl mx-auto py-3 px-3 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between flex-wrap">
          <div class="w-0 flex-1 flex items-center">
            <span class="flex p-2 rounded-lg bg-indigo-800">
              <SpeakerphoneIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </span>
            <p class="ml-3 font-medium text-white">
              <span class="md:inline sm:inline-flex">
                Debido a la situación del COVID-19, el aforo en las instalaciones varía dependiendo del tipo 
                de actividad y de las restricciones establecidas por el ministerio de Salud de Costa Rica.
              </span>
            </p>
          </div>
          <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-3">
            <button @click='messageToggle = !messageToggle ' type="button" class="-mr-1 flex p-2 rounded-md transition hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
              <span class="sr-only">Dismiss</span>
              <XIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>
    <div class="clear" :style="{ clear: 'left' }"></div>
    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>



<script>
import { SpeakerphoneIcon, XIcon } from "@heroicons/vue/outline";
import axios from 'axios'
import Disclosure from './components/Disclosure.vue';

export default {
  name: "app",
  data() {
    return {
      userInfo : this.$store.state.info,
      showMobileMenu: false,
      messageToggle: true,
      permissions: this.$store.state.permissions,
      open: false,
      page:0,
    };
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    this.page = 0
    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  computed:{
    canViewConfig(){
      return this.$store.state.permissions.includes("gymSettings.view_config");
    },
    canViewClient(){
      return this.$store.state.permissions.includes("gymClients.view_client");
    }
  },
  components: {
    SpeakerphoneIcon,
    XIcon,
    Disclosure,
  },
  methods:{
    logout() {
        this.page = -1
        this.userInfo = []
        localStorage.removeItem('userInfo')
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        localStorage.removeItem("userid")
        localStorage.removeItem("UP")
        this.$store.commit('removeToken')
        this.$store.commit('removePermissions')
        this.$router.push('/')
    },
  }
};
</script>

<style lang="scss">
@import "../node_modules/bulma";
.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
.navbar {
  transition: all 330ms ease-out;
}

.navbar-open {
  transform: translateX(0%);
}
.navbar-close {
  transform: translateX(-100%);
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  &.is-loading {
    height: 80px;
  }
}
</style>