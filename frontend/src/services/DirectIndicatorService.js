import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ mId, id }) => {
    const base = `${API_URL}/methods/${mId}/direct-indicators/`
    return id ? `${base}${id}/` : base
}

export default new BaseApiService(createUrl)
