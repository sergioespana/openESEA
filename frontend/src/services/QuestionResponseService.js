import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ oId, eaId, srId, id, query = '' }) => {
    console.log(query)
    let base = `${API_URL}/organisations/${oId}/esea-accounts/${eaId}/responses/${srId}/question-responses`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)