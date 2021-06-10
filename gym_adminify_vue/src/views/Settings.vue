<template>
  <div class="page-settings min-h-screen">
    <div v-if="canChangeSettings">
      <button v-if="!isChanging" v-on:click="isChanging = !isChanging" class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-blue-500 rounded-full hover:bg-blue-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <i class="text-white fas fa-pencil-alt fa-lg"></i>
      </button>
      <button v-else v-on:click="changeSettings()" class="fixed z-50 bottom-10 right-10 w-12 h-12 bg-green-500 rounded-full hover:bg-green-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
        <i class="text-white far fa-save fa-lg"></i>
      </button>
    </div>
    <div class="columns is-multiline">
      <div class="column is-5">
        <div class="flex max-w-sm w-full bg-gray-200 shadow-md rounded-lg overflow-hidden mx-auto">
          <div class="w-4 bg-indigo-500"></div>
          <div class="px-4">
            <input :disabled="!isChanging" v-model="gym.name" class="title appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/>
            <span class="font-extrabold">Costo de matricula:</span>
            <input :disabled="!isChanging" v-model="gym.tuitioncost" class="appearance-none bg-transparent border-none w-min text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/>
          </div>
        </div>
        <div class="flex mt-4 max-w-sm w-full bg-gray-200 shadow-md rounded-lg overflow-hidden mx-auto">
          <div class="w-4 bg-blue-400"></div>
          <div class="px-4">
            <h1 class="title divide-y mt-4">Configuracion General</h1>
            <span class="font-extrabold">Fecha inicio:</span>
            <input :disabled="!isChanging" v-model="config.effectivedate" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/>
            <span class="font-extrabold">Porcentaje de capacidad:</span>
            <input :disabled="!isChanging" v-model="config.capacitypercentage" class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/>
          </div>
        </div>
        <div class="flex mt-4 max-w-sm w-full bg-gray-200 shadow-md rounded-lg overflow-hidden mx-auto">
          <div class="w-2 bg-green-400"></div>
          <div class="px-4">
            <h1 class="title mt-4">Horario General</h1>
            <div class="table-responsive">
              <table class="table-hover" v-if="config.timeperday">
                <thead>
                  <tr>
                    <th>Dia</th>
                    <th>Inicio</th>
                    <th>Fin</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in config.timeperday" :key="item">
                    <span class="px-2">{{ item.dia }}</span>
                    <td>
                      <input :disabled="!isChanging" v-model="item.inicio" type="time"/>
                    </td>
                    <td>
                      <input :disabled="!isChanging" v-model="item.fin" type="time"/>
                    </td>
                    <button v-if="isChanging" v-on:click="deleteDay(item)" type="button" class="rounded-md transition hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-white sm:-mr-2">
                      <i class="far fa-times-circle fa-sm"></i>
                    </button>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div></div>
        </div>
      </div>
      <div class="column is-5">
        <div class="flex max-w-sm w-full bg-white shadow-md rounded-lg overflow-hidden mx-auto">
          <div class="w-3 bg-yellow-400"></div>
          <div class="px-4">
            <input :disabled="!isChanging" v-model="room.name" class="title appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/>
            <span class="font-extrabold">Capacidad:</span>
            <input :disabled="!isChanging" v-model="room.capacity" class="appearance-none bg-transparent border-none w-min text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Fecha inicio" aria-label="Full name"/> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
import color from "../../node_modules/tailwindcss/colors";
let colors = {
  "red-100-accent": "#4b778d",
};
export default {
  name: "Settings",
  components: {
    color,
  },
  data() {
    return {
      gym: {},
      room: {},
      config: {},
      isChanging: false,
      permissions: this.$store.state.permissions,
    };
  },
  mounted() {
    this.getSettings();
  },
  computed: {
    canChangeSettings() {
      return (
        this.permissions.includes("gymSettings.change_gym") &&
        this.permissions.includes("gymSettings.change_room") &&
        this.permissions.includes("gymSettings.change_config")
      );
    },
  },
  methods: {
    deleteDay(item) {
      (item.fin = null), (item.inicio = null);
    },
    async getSettings() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/update-settings/")
        .then((response) => {
          this.config = response.data["config"];
          this.gym = response.data["gym"];
          this.room = response.data["room"];
          document.title = this.gym.name;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema obteniendo las configuraciones",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async changeSettings() {
      this.$store.commit("setIsLoading", true);
      const formData = {
        config: this.config,
        room: this.room,
        gym: this.gym,
      };
      await axios
        .put("/api/v1/update-settings/", formData)
        .then((response) => {
          toast({
            message: "Configuracion editada exitosamente",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "bottom-right",
          });
          this.isChanging = !this.isChanging;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema al editar la configuracion",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
