import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ oId, eaId, query = '' }) => {
    const base = `${API_URL}/organisations/${oId}/esea-accounts/${eaId}/responses/check_certification_triggers`

    // let base = `${API_URL}/audit-account`
    // base = id ? `${base}/${id}/responses/check_certification_triggers` : base
    return `${base}/${query}`
}

export default new BaseApiService(createUrl)
