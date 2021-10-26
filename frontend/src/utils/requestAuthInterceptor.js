// To be Written

// Needs to be imported into the plugins/axios js file as a AxiosInstance default
import store from '../store'
import { API_URL } from '../utils/constants'

export default [
    (config) => {
        if (
        config.url.startsWith(API_URL) && !(config.url.includes('register') || config.url.includes('token') || config.url.includes('responses')) // || config.url.includes('surveys')
        ) {
            config.headers.Authorization = 'Bearer ' + store.getters['authentication/AuthenticationToken']
            // config.headers['Content-Type'] = 'multipart/form-data'
        }
        return config
    },
    error => Promise.reject(error)
]
