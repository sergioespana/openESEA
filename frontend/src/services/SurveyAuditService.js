import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ oId = 0, eaId = 0, id, query = '' }) => {
    console.log(query)
    let base = `${API_URL}/organisations/${oId}/esea-accounts/${eaId}/survey-audit`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
