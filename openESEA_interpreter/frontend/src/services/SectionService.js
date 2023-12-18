import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ mId, sId, id, query = '' }) => {
    console.log('type:', typeof (sId))
    let base = `${API_URL}/methods/${mId}/surveys/${sId}/sections`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
