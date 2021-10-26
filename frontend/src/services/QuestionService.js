import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ mId, SuId, SeId, id }) => {
    const base = `${API_URL}/methods/${mId}/surveys/${SuId}/sections/${SeId}/questions/`
    return id ? `${base}${id}/` : base
}

export default new BaseApiService(createUrl)
