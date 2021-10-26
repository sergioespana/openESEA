import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ nId, id, query = '' }) => {
    let base = `${API_URL}/networks/${nId}/campaigns`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
