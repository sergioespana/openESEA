import { AxiosInstance } from '../../plugins/axios'
// import { STATUS } from '../../utils/constants'
import UserService from '../../services/UserService'
import router from '../../router'

export default {
    namespaced: true,
    state: {
        accessToken: null,
        refreshToken: null,
        authenticatedUser: null,
        currentuser: 'Username here',
        password: null,
        errors: {}
    },
    mutations: {
        updateStorage (state, { access, refresh }) {
          state.accessToken = access
          state.refreshToken = refresh
        },
        destroyToken (state) {
            router.push({ name: 'login' })
            state.accessToken = null
            state.refreshToken = null
            state.authenticatedUser = null
            state.currentuser = null
        },
        UpdateCurrentUser (state, username) {
            state.currentuser = username
        },
        saveAuthenticatedUserDetails (state, { data }) {
          state.authenticatedUser = data[0]
        },
        setErrors (state, { errors }) {
          state.errors = errors
        },
        clearErrors (state) {
          state.errors = {}
        }
    },
    getters: {
        loggedIn (state) {
          return ((state.accessToken != null) & (state.authenticatedUser != null))
        },
        AuthenticationToken (state) {
          return state.accessToken
        }
      },

    actions: {
        async userRegister ({ commit, state }, newuser) {
          state.errors = {}
          await AxiosInstance.post('/account/register/', newuser)
          .then((response) => { router.push({ name: 'login' }) })
          .catch((error) => { commit('setErrors', { errors: error.response.data }) })
        },
        userLogout ({ commit, getters }) {
            if (getters.loggedIn) {
                commit('destroyToken')
            }
        },
        async userLogin ({ commit, dispatch }, usercredentials) {
          await AxiosInstance.post('/api-token/', {
            username: usercredentials.username,
            password: usercredentials.password
          })
          .then(async (response) => {
            await commit('updateStorage', { access: response.data.access, refresh: response.data.refresh })
            await dispatch('saveAuthenticatedUserDetails')
            commit('UpdateCurrentUser', usercredentials.username)
            dispatch('tokenExpirationTimer')
          })
        },
        async refreshAccessToken ({ commit, state }) {
          await AxiosInstance.post('api-refresh/', {
            refresh: state.refreshToken
          })
          .then((response) => {
            commit('updateStorage', { access: response.data.access, refresh: state.refreshToken })
          })
          .catch(err => {
            console.log(err)
            commit('destroyToken')
          })
        },
        tokenExpirationTimer ({ commit }) {
          var timeout
          clearTimeout(timeout)
          timeout = setTimeout(() => {
            commit('destroyToken')
          }, 30 * 60 * 1000)
        },
        async saveAuthenticatedUserDetails (context) {
          const { response, error } = await UserService.get({ query: '?currentuser=1' })
          if (error) {
            console.log(error)
            return
          }
          context.commit('saveAuthenticatedUserDetails', response)
        }
    }
}
