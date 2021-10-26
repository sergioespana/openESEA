import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ mId, id, query = '' }) => {
    console.log(query)
    let base = `${API_URL}/methods/${mId}/surveys`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
