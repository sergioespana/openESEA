import AuditAccountService from '@/services/AuditAccountService'

export default {
    namespaced: true,
    state: {
        indicators: [],
        selectedIndicators: [],
        indicator: {},
        error: undefined,
        debouncers: {},
        errors: {}
    },
    getters: {},
    mutations: {
        setIndicators (state, { data }) {
            state.indicators = data || {}
            state.debouncers = {}
            state.errors = {}
        },
        setSelectedIndicators (state, data) {
            state.selectedIndicators = data
        },
        setIndicator (state, { data }) {
            console.log('-->', data)
            state.indicator = data || {}
        },
        setError (state, { error, id }) {
            console.log(id, '--', error?.response?.data)
            if (id && error?.response?.data) {
                state.errors = { ...state.errors, [id]: error?.response?.data }
                return
            }
            state.error = error
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchIndicators ({ commit }, payload) {
            const { response, error } = await AuditAccountService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setIndicators', response)
        },
        async selectIndicators ({ commit }, { indicators }) {
            await commit('setSelectedIndicators', indicators)
        },
        setSelectedIndicator ({ state, commit }, { id } = {}) {
            console.log(id)
            const data = state.selectedIndicators.find(indicator => indicator.id === id)
            if (data && data.id === state.indicator.id) return
            commit('setIndicator', { data })
        }
    }
}
