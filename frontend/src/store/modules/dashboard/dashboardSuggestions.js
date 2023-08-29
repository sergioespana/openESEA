import DashboardSuggestionsService from '../../../services/DashboardSuggestionsService.js'

export default {
    namespaced: true,
    state: {
        dashboardSuggestions: [],
        error: []
    },
    getters: {
        getDashboardSuggestions: state => state.dashboardSuggestions
    },
    mutations: {
        setDashboardSuggestions (state, { data }) {
            state.dashboardSuggestions = data || []
        },
        setError (state, { error }) {
            console.log('my error:', error?.response?.data)
            state.error = error?.response?.data || []
        }
    },
    actions: {
        async buildDashboardRLModel ({ commit }, payload) {
            const { response, error } = await DashboardSuggestionsService.post(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            console.log(response)
        },
        async updateDashboardRLModel ({ commit }, payload) {
            const { response, error } = await DashboardSuggestionsService.put(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            console.log(response)
        },
        async deleteDashboardRLModel ({ commit }, payload) {
            console.log('stopping rl model...')
            const { response, error } = await DashboardSuggestionsService.delete()
            console.log(response, error)
            if (error) {
                await commit('setError', { error })
                // return
            }
        },
        async fetchDashboardSuggestions ({ commit }, payload) {
            const { response, error } = await DashboardSuggestionsService.get()
            if (error) {
                await commit('setError', { error })
                return
            }
            await commit('setDashboardSuggestions', response)
        }
    }
}
