import { AxiosInstance } from '../plugins/axios'
import store from '../store'

export default async ({ method = 'get', url, data }) => {
    try {
        console.log('Url: ', url)
        if (data) { console.log('Request Data: ', data) }
        const response = await AxiosInstance[method](url, data)
        return { response }
    } catch (error) {
        console.log('nnnnnnnn', error)
        if (error?.response?.status === 401 && store.state.authentication.accessToken) {
            await store.dispatch('authentication/refreshAccessToken')
            try {
                const response = await AxiosInstance[method](url, data)
                return { response }
            } catch (error) {
            }
        }
        return { error }
    }
}
