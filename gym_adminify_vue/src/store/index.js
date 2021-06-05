import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    isLoading: false,
    permissions:[],
    permsLoaded: false,
  },
  mutations: {
    initializeStore(state){
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
        state.permissions = localStorage.getItem('UP')
        state.permsLoaded = true
      } else {
        state.token = ''
        state.isAuthenticated = false
        state.permsLoaded = false
        state.permissions = []
        state.token = ''
        state.isAuthenticated = false
      } 
    },
    setIsLoading(state,status){
      state.isLoading = status
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },  
    removePermissions(state) {
      state.permissions = []
      state.permsLoaded = false
    },
    removeToken(state) {
      localStorage.removeItem('UP')
      state.token = ''
      state.isAuthenticated = false
    },
    setPermissions(state,permissions) {
      localStorage.setItem('UP',permissions)
      state.permissions = permissions
      state.permsLoaded = true
    }, 
  },
  actions: {
  },
  modules: {
  }
})
