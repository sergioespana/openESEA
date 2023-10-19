import DashboardSuggestionsService from '../../../services/DashboardSuggestionsService.js'

export default {
    namespaced: true,
    state: {
        dashboardSuggestions: [],
        modelInstanceId: null,
        error: []
    },
    getters: {
        getDashboardSuggestions: state => state.dashboardSuggestions,
        getModelInstanceId: (state, getters) => () => state.modelInstanceId
    },
    mutations: {
        setDashboardSuggestions (state, { data }) {
            state.dashboardSuggestions = data || []
        },
        setModelInstanceId (state, modelInstanceId) {
            state.modelInstanceId = modelInstanceId
        },
        setError (state, { error }) {
            console.log('my error:', error?.response?.data)
            state.error = error?.response?.data || []
        }
    },
    actions: {
        async buildDashboardRLModel ({ commit, dispatch, getters }, payload) {
            const { response, error } = await DashboardSuggestionsService.post(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            const modelInstanceId = response.data.modelInstanceId
            commit('setModelInstanceId', modelInstanceId)
        },
        async updateDashboardRLModel ({ commit, dispatch, getters }, payload) {
            const dashboard = payload.data.dashboard
            const modelInstanceId = getters.getModelInstanceId()
            var newPayload = {}
            newPayload.data = {
                dashboard: dashboard,
                modelInstanceId: modelInstanceId
            }
            const { response, error } = await DashboardSuggestionsService.post(newPayload)
            if (error) {
                await commit('setError', { error })
                return
            }
            return response
        },
        async deleteDashboardRLModel ({ commit, dispatch, getters }, payload) {
            const modelInstanceId = getters.getModelInstanceId()
            var newPayload = {}
            newPayload.data = {
                modelInstanceId: modelInstanceId
            }
            const { response, error } = await DashboardSuggestionsService.delete(newPayload)
            if (error) {
                await commit('setError', { error })
                return
            }
            return response
        },
        async fetchDashboardSuggestions ({ commit, dispatch, getters }, payload) {
            const modelInstanceId = getters.getModelInstanceId()
            var newPayload = {}
            newPayload.data = {
                modelInstanceId: modelInstanceId
            }
            const { response, error } = await DashboardSuggestionsService.put(newPayload)
            console.log(response)
            if (error) {
                await commit('setError', { error })
                return
            }
            await commit('setDashboardSuggestions', response)
        }
    }
}
