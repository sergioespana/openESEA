import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = ({ oId, eaId, id, query = '' }) => {
    console.log(query)
    let base = `${API_URL}/organisations/${oId}/esea-accounts/${eaId}/responses`
    base = id ? `${base}/${id}` : base
    return `${base}/${query}`
}

// const createUrl = ({ mId, sId, OrganisationId = 0, id, query = '' }) => {
//     let base = `${API_URL}/methods/${mId}/surveys/${sId}/organisations/${OrganisationId}/responses`
//     base = id ? `${base}/${id}` : base
//     return `${base}/${query}`
// }

export default new BaseApiService(createUrl)
