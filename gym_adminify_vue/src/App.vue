<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"
          ><strong>Gym-Adminify</strong></router-link
        >

        <a
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div
        class="navbar-menu"
        id="navbar-menu"
        v-bind:class="{ 'is-active': showMobileMenu }"
      >
        <div class="navbar-start">
          <template v-if="$store.state.isAuthenticated">
            <router-link to="/clientes" class="navbar-item">
              Clientes
            </router-link>
            <router-link to="/bills" class="navbar-item">
              Facturas
            </router-link>
            <router-link to="/teachers" class="navbar-item">
              Instructores
            </router-link>
          </template>

          <template v-else>
            <router-link to="/about" class="navbar-item">
              ¿Quienes somos?
            </router-link>
          </template>
          <router-link to="/services" class="navbar-item">
            Servicios
          </router-link>
          <router-link to="/activities" class="navbar-item">
            Actividades
          </router-link>
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.isAuthenticated">
              <div v-if="canViewConfig">
                <router-link to="/gym_settings" class="button is-success">
                  <span class="icon"><i class="fas fa-cog"></i></span>
                </router-link>
              </div>
              <button @click="logout()" class="button is-light">
                Salir
              </button>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <div  v-show='toggle' id="messageCovid" class="bg-indigo-600" >
      <div class="max-w-7xl mx-auto py-3 px-3 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between flex-wrap">
          <div class="w-0 flex-1 flex items-center">
            <span class="flex p-2 rounded-lg bg-indigo-800">
              <SpeakerphoneIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </span>
            <p class="ml-3 font-medium text-white">
              <span class="hidden md:inline">
                Debido a la situación del COVID-19, el aforo en las
                instalaciones varía dependiendo del tipo de actividad y de las
                restricciones establecidas por el ministerio de Salud de Costa
                Rica.
              </span>
            </p>
          </div>
          <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-3">
            <button @click='toggle = !toggle ' type="button" class="-mr-1 flex p-2 rounded-md transition hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
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
export default {
  data() {
    return {
      showMobileMenu: false,
      toggle: true,
      permissions: this.$store.state.permissions,
    };
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  computed:{
    canViewConfig(){
      // console.log(this.permissions.includes("gymSettings.view_gym"))
      // console.log(this.permissions)
      return this.$store.state.permissions.includes("gymSettings.view_gym");
    }
  },
  components: {
    SpeakerphoneIcon,
    XIcon,
  },
  methods:{
    logout() {
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        localStorage.removeItem("userid")
        // localStorage.removeItem("userPermissions")
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