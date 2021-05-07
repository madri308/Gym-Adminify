<template>
  <div class="home">
    <div class="grid justify-around grid-cols-2">
      <div class="bg-gray-800 h-72 bg-opacity-50" >
        <div class="hero-body has-text-centered">
          <p class="text-white title mb-6 text-7xl">EL MEJOR GIMNASIO</p>
          <p class="text-white subtitle">Ahora desde tu ordenador</p>
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

export default {
  name: "Home",
  components: {
    Calendar
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
      errors: []
    };
  },
  mounted() {
      document.title = 'Log In | Djackets'
  },
  methods: {
      async submitForm() {
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
          })
          .catch(error => {
              if (error.response) {
                  for (const property in error.response.data) {
                      this.errors.push(`${property}: ${error.response.data[property]}`)
                  }
              } else {
                  this.errors.push('Something went wrong. Please try again')
                  
                  console.log(JSON.stringify(error))
              }
          })
      }
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
