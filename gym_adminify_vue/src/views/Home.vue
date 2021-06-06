<template>
  <div class="home">
    <div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4 space-x-40">
      <div class="bg-gray-800 h-72 md:w-auto sm:w-20 bg-opacity-50">
        <div class="hero-body has-text-centered">
          <p class="text-white text-7xl align-middle ">EL MEJOR GIMNASIO</p>
          <p class="text-white subtitle align-middle ">Ahora desde tu ordenador</p>
        </div>
      </div>
      <div>
        <template v-if="$store.state.isAuthenticated">
          <Calendar ref="calendar" locale="es" :min-page="firstPage" mode="range" :attributes="attributes" :update:to-page="printPage()">
          </Calendar>
        </template>
        <template v-else>
          <div class="h-96 w-80 page-log-in rounded-lg shadow-lg p-4">
            <h1 class="title">Inicio de Sesion</h1>
            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Correo</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>

                <div class="field">
                    <label>Contraseña</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>

                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button is-dark">Log in</button>
                    </div>
                </div>
                <hr>
            </form>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { Calendar } from "v-calendar";
import axios from 'axios'
import { UserIcon } from "@vue-hero-icons/solid"

export default {
  name: "Home",
  components: {
    Calendar,
    UserIcon
  },

  data() {
    var todos = [];
    return {
      userInfo:[],
      incId: todos.length,
      todos,
      username: '',
      password: '',
      errors: [],
      currentDate: new Date(),
      firstPage:null,
      colors:["red","green","blue","teal"],
    };
  },
  mounted() {
      document.title = 'Home | Gym-Adminify';
    
      const month = this.currentDate.getMonth()+1;
      const year = this.currentDate.getFullYear();
      this.firstPage = { month, year }
      this.getActivities()
  },
  methods: {
    printPage(){
      if(this.$refs.calendar != null){
        console.log(this.$refs.calendar.pages[0].key);
      }
    },
    normalizeInfo(data){
      for (var key in data) {
        if(key != 'id' && typeof key != 'number'){
          if(typeof data[key] == 'object'){
            // this.userInfo.push({"key":key, "value":null})
            this.normalizeInfo(data[key])
          }else{
            this.userInfo.push({"key":key, "value":data[key]})
          }
        }
      }
    },
    async submitForm() {
        this.$store.commit("setIsLoading", true);
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("token")

        const formData = {
            username: this.username,
            password: this.password
        }
        await axios
        .post("/api/v1/token/login/", formData)
        .then(response => {
            const token = response.data.auth_token
            this.$store.commit('setToken', token)
            axios.defaults.headers.common["Authorization"] = "Token " + token
            localStorage.setItem("token", token)
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)
                }
            } else {
                this.errors.push('Something went wrong. Please try again')
            }
        })
        localStorage.removeItem("userInfo")
        await axios
        .get("/api/v1/personInfo/")
        .then((response) => {
          this.normalizeInfo(response.data)
          this.$store.commit('setInfo', this.userInfo);
          // const toPath = this.$route.query.to || '/'
          // this.$router.push(toPath)
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos del usuario actual", type: "is-danger",
            dismissible: true, pauseOnHover: true,duration: 2000, position: "bottom-right",
          });
        });
        localStorage.removeItem("UP")
        await axios
        .get("/api/v1/permissions/")
        .then((response) => {
          this.$store.commit('setPermissions', response.data);
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Permisos", type: "is-danger",
            dismissible: true, pauseOnHover: true,duration: 2000, position: "bottom-right",
          });
        });
        location.reload();
        this.$store.commit("setIsLoading", false);
    },
    async getActivities(){
      this.$store.commit("setIsLoading", true);
      await axios
      .get("/api/v1/schedule-activities/")
      .then((response) => {
        this.todos = response.data;
      })
      .catch((error) => {
        toast({
          message: "Ocurrio un problema con los datos de: Actividades", type: "is-danger",
          dismissible: true, pauseOnHover: true,
          duration: 3000, position: "bottom-right",
        });
      });
      this.$store.commit("setIsLoading", false);
    }
  },
  computed: {
    attributes() {
      return [
        {
          contentStyle: {
            fontWeight: "700",
            fontSize: '.9rem',
          },
          dates: new Date(),
        },
        // Attributes for todos
        ...this.todos.map((todo) => ({
          // dates: new Date(todo.schedule.year,todo.schedule.month-1, todo.dayofweek),
          dates: {weekdays:todo.dayofweek, months:todo.schedule.month , years:todo.schedule.year},
          dot: {
            color: "red",
          },
          popover: {
            label: todo.service_name+" - "+todo.teacher_name+ " - " +(todo.startime) + "-" + (todo.endtime),
            visibility: "click",
          },
        })),
      ];
    },
  },
};
</script>
