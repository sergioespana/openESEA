import apiCall from '../utils/api'

export default class BaseApiService {
    constructor (createUrl) {
        this.createUrl = createUrl
    }

    get (payload) {
        const url = this.createUrl(payload)
        return apiCall({ url })
    }

    post (payload) {
        const newPayload = { ...payload, id: undefined }
        const url = this.createUrl(newPayload)
        return apiCall({ method: 'post', url, data: payload.data })
    }

    put (payload) {
        console.log(payload)
        const url = this.createUrl(payload)
        return apiCall({ method: 'put', url, data: payload.data })
    }

    patch (payload) {
        const url = this.createUrl(payload)
        return apiCall({ method: 'patch', url, data: payload.data })
    }

    delete (payload) {
        const url = this.createUrl(payload)
        return apiCall({ method: 'delete', url })
    }
}
