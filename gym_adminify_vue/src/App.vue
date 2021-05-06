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
          <router-link to="/clients" class="navbar-item">Clientes</router-link>
          <router-link to="/services" class="navbar-item"
            >Servicios</router-link
          >
          <router-link to="/activities" class="navbar-item"
            >Actividades</router-link
          >
          <router-link to="/bills" class="navbar-item">Facturas</router-link>
          <router-link to="/teachers" class="navbar-item"
            >Instructores</router-link
          >
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.isAuthenticated">
              <router-link to="/my-account" class="button is-light"
                >My account</router-link
              >
            </template>

            <template v-else>
              <router-link to="/log-in" class="button is-light"
                >Log in</router-link
              >
            </template>

            <router-link to="/gym_settings" class="button is-success">
              <span class="icon"><i class="fas fa-cog"></i></span>
            </router-link>
            <router-link to="/log-in" class="button is-light"
              >Salir</router-link
            >
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
            <button @click='toggle = !toggle '
              type="button"
              class="-mr-1 flex p-2 rounded-md transition hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2"
            >
              <span class="sr-only">Dismiss</span>
              <XIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      class="is-loading-bar has-text-centered"
      v-bind:class="{ 'is-loading': $store.state.isLoading }"
    >
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
export default {
  data() {
    return {
      showMobileMenu: false,
      toggle: true,
    };
  },
 
  components: {
    SpeakerphoneIcon,
    XIcon,
  },
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