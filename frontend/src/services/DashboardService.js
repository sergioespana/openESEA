import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ id, query = '' }) => {
    let base = `${API_URL}/dashboards`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
