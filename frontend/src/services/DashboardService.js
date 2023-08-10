import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = (payload) => {
    const id = payload?.id
    const query = payload?.query
    let dashboardUrl = `${API_URL}/dashboards`
    if (id) dashboardUrl += `/${id}/`
    if (query) dashboardUrl += `${query}`
    return dashboardUrl
}

export default new BaseApiService(createUrl)
