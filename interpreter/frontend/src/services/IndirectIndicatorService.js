import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ mId, id }) => {
    console.log(mId)
    const base = `${API_URL}/methods/${mId}/indirect-indicators/`
    return id ? `${base}${id}/` : base
}

export default new BaseApiService(createUrl)
