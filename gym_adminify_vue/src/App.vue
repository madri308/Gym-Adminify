<template>
  <div id="wrapper" :style="{'background-image':'url(https://i.imgur.com/FTYWtID.jpg)', 'background-size': 'cover','background-position':'center','background-repeat':'no-repeat'}">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Gym-Adminify</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
        <div class="navbar-start">
          <router-link to="/clientes" class="navbar-item">Clientes</router-link>
          <router-link to="/servicios" class="navbar-item">Servicios</router-link>
          <router-link to="/actividades" class="navbar-item">Actividades</router-link>
          <router-link to="/facturas" class="navbar-item">Facturas</router-link>
          <router-link to="/instructores" class="navbar-item">Instructores</router-link>
        </div>
      </div>
      <div class="navbar-end">

        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.isAuthenticated">
              <router-link to="/my-account" class="button is-light">My account</router-link>
            </template>

            <template v-else>
              <router-link to="/log-in" class="button is-light">Log in</router-link>
            </template>

            <router-link to="/configuracion" class="button is-success">
              <span class="icon"><i class="fas fa-cog"></i></span>
            </router-link>
            <router-link to="/log-in" class="button is-light">Salir</router-link>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view/>
    </section>
    <div class="clear" :style="{'clear': 'both'}"></div>
    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>



<script>
export default {
  data() {
    return {
      showMobileMenu: false,
    }
  }
}
</script>
<style lang="scss">
@import '../node_modules/bulma';
</style>
