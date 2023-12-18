import { API_URL } from '../utils/constants'
import BaseApiService from './BaseApiService'

const createUrl = (payload) => {
    const dashboardSuggestionsUrl = `${API_URL}/dashboardsuggestions/`
    return dashboardSuggestionsUrl
}

export default new BaseApiService(createUrl)
