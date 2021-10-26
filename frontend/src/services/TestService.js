import { AxiosInstance } from '../plugins/axios'

export default {
    get () {
        return AxiosInstance.get('http://127.0.0.1:8000/organisations/')
    }
}
