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
      } else {
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
      state.token = ''
      state.isAuthenticated = false
    },
    setPermissions(state,permissions) {
      state.permissions = permissions
      state.permsLoaded = true
    }, 
  },
  actions: {
  },
  modules: {
  }
})
