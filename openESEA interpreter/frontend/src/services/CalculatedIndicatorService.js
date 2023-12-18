import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ oId, mId, id }) => {
    const base = `${API_URL}/organisations/${oId}/methods/${mId}/calculated-indicators/`
    return id ? `${base}id/` : base
}

export default new BaseApiService(createUrl)
