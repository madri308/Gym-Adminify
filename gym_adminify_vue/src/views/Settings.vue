<template>
  <div class="page-settings">
    <div class="columns is-multiline">

      <div class="column is-5">
        <section class="flex flex-wrap justify-center px-4 bg-white">
          <div class="max-w-lg w-full rounded-lg shadow-lg p-4">

            <h1 class="title">{{ gym.name }}</h1>
            <p>Costo de matricula: ₡{{ gym.tuitioncost }}</p>

            <h1 class="title mt-4">Configuracion General</h1>
            <p>Fecha inicio: {{ config.effectivedate }}</p>
            <p>Porcentaje de capacidad: {{ config.capacitypercentage }}</p>

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
                    <td>{{ item.dia }}</td>
                    <td>{{ item.inicio }}</td>
                    <td>{{ item.fin }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>
        </section>
      </div>

      <div class="column is-5">
        <section class="flex flex-wrap px-4 bg-white">

          <div class="max-w-lg w-full rounded-lg shadow-lg p-4">
            <h1 class="title">Room-1</h1>
            <p>Info del room</p>
          </div>
          
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

export default {
  name: "Settings",
  data() {
    return {
      gym: {},
      room: {},
      config: {},
    };
  },
  mounted() {
    this.getConfig();
    this.getGym(), this.getRoom();
  },
  methods: {
    async getConfig() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/gym-config/")
        .then((response) => {
          this.config = response.data;
        })
        .catch((error) => {
          console.log(error);
          toast({
            message: "Ocurrio un problema con los datos de: Configuracion",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async getGym() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/gym-info/")
        .then((response) => {
          this.gym = response.data;
          document.title = this.gym.name;
        })
        .catch((error) => {
          console.log(error);
          toast({
            message: "Ocurrio un problema con los datos de: Gimnasio",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
    async getRoom() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("/api/v1/room-info/")
        .then((response) => {
          this.room = response.data;
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Cuartos",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
