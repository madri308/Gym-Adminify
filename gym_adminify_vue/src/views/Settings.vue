<template>
  <div class="page-settings">
    <div class="columns is-multiline">
      <div class="column is-9">
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
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
    getConfig() {
      axios
        .get("/api/v1/gym-config/")
        .then((response) => {
          this.config = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getGym() {
      axios
        .get("/api/v1/gym-info/")
        .then((response) => {
          this.gym = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getRoom() {
      axios
        .get("/api/v1/room-info/")
        .then((response) => {
          this.room = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
