<template>
  <div class="home">
    <div class="grid grid-cols-2 gap-4 space-x-40">
      <div class="bg-gray-800 h-72 bg-opacity-50">
        <div class="hero-body has-text-centered">
          <p class="text-white text-7xl align-middle ">EL MEJOR GIMNASIO</p>
          <p class="text-white subtitle align-middle ">Ahora desde tu ordenador</p>
        </div>
      </div>
      <div>
        <template v-if="$store.state.isAuthenticated">
          <Calendar :attributes="attributes">
            <template #day-popover>
              <div>
                Using my own content now
                <!-- {{ format(day.date, masks.dayPopover) }} -->
              </div>
              <div slot="add-todo" slot-scope="{ day }" class="add-todo">
                <a @click="addTodo(day)"> + Add Todo </a>
              </div>
            </template>
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
                <!-- Or <router-link to="/sign-up">click here</router-link> to sign up! -->
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
    const todos = [
      {
        id: 1,
        description: "Take Noah to basketball practice.",
        isComplete: false,
        dates: { weekdays: 6 }, // Every Friday
        color: "blue",
      },
    ];

    return {
      incId: todos.length,
      editId: 0,
      todos,
      username: '',
      password: '',
      errors: [],
    };
  },
  mounted() {
      document.title = 'Log In | Gym-Adminify'
  },
  methods: {
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
              const toPath = this.$route.query.to || '/'
              this.$router.push(toPath)

              this.getPermissions();
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
          this.$store.commit("setIsLoading", false);
      },
      getPermissions() {
        axios
        .get("/api/v1/permissions/")
        .then((response) => {
          this.$store.commit('setPermissions', response.data);
          // localStorage.setItem("userPermissions", response.data);
        })
        .catch((error) => {
          toast({
            message: "Ocurrio un problema con los datos de: Permisos", type: "is-danger",
            dismissible: true, pauseOnHover: true,
            duration: 2000, position: "bottom-right",
          });
        });
    },
  },
  computed: {
    attributes() {
      return [
        {
          contentStyle: {
            fontWeight: "700",
            color: "#66b3cc",
          },
          dates: new Date(),
        },
        // Attributes for todos
        ...this.todos.map((todo) => ({
          key: todo.id,
          dates: todo.dates,
          customData: todo,
          dot: {
            color: todo.color,
            class: todo.isComplete ? "opacity-75" : "",
          },
          popover: {
            label: todo.description,
            visibility: "click",
          },
          popover: true,
          customData: todo,
        })),
        {
          contentHoverStyle: {
            backgroundColor: "rgba(0, 0, 0, 0.1)",
            cursor: "pointer",
          },
          dates: {}, // All dates
          popover: {
            slot: "add-todo",
            visibility: "focus",
            hideIndicator: true,
          },
        },
      ];
    },
  },
};
</script>
