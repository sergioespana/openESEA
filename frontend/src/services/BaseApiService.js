// All the different type of requests that are required for the backend
// Used in the ...Service.js files

import apiCall from '../utils/api'

export default class BaseApiService {
    // create right url function (based on service) for the api call
    constructor (createUrl) {
        this.createUrl = createUrl
    }

    get (payload) {
        const url = this.createUrl(payload)
        return apiCall({ url })
    }

    post (payload) {
        // no id needed for post request, so set to undefined
        const newPayload = { ...payload, id: undefined }
        // create url
        const url = this.createUrl(newPayload)
        // create api call
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
