import store from '../store'
import { API_URL } from '../utils/constants'
// import router from '../router'

export default [
    response => response, (error) => {
        console.log('ddd')
        if (error.response && error.response.status === 401 && store.state.authentication.authenticatedUser && error.config.url.startsWith(API_URL)) {
            console.log('Not authenticated')
            
            // store.dispatch('auth/removeToken')
            // router.push({ name: 'login', params: { nextUrl: router.currentRoute.fullPath } })
        }
        throw error
    }
]
